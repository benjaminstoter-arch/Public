/* Finance × AI CSV reporting engine. All amounts are integer pence; no external services. */
(function(root,factory){
  const api=factory();
  if(typeof module!=="undefined"&&module.exports)module.exports=api;
  else root.FPAEngine=api;
})(typeof globalThis!=="undefined"?globalThis:this,function(){
"use strict";
const COLUMNS=["month","line item","type","actual","budget","prior year"];
function csvRows(text){
  if(typeof text!=="string"||!text.trim())throw Error("File is empty.");
  text=text.replace(/^\uFEFF/,"");
  const rows=[];let row=[],cell="",quoted=false,afterQuote=false;
  for(let i=0;i<text.length;i++){
    const c=text[i];
    if(quoted){if(c==='"'){if(text[i+1]==='"'){cell+='"';i++;}else{quoted=false;afterQuote=true;}}else cell+=c;}
    else if(afterQuote){if(c===','){row.push(cell);cell="";afterQuote=false;}else if(c==='\n'||c==='\r'){row.push(cell);if(row.some(x=>x.trim()))rows.push(row);row=[];cell="";afterQuote=false;if(c==='\r'&&text[i+1]==='\n')i++;}else if(c!==' '&&c!=='\t')throw Error("Unexpected character after closing quote.");}
    else if(c==='"'){if(cell.trim())throw Error("Quotes must enclose the whole field.");cell="";quoted=true;}
    else if(c===','){row.push(cell);cell="";}
    else if(c==='\n'||c==='\r'){row.push(cell);if(row.some(x=>x.trim()))rows.push(row);row=[];cell="";if(c==='\r'&&text[i+1]==='\n')i++;}
    else cell+=c;
  }
  if(quoted)throw Error("Unclosed quote in CSV.");
  row.push(cell);if(row.some(x=>x.trim()))rows.push(row);
  return rows;
}
function typeOf(raw){
  const s=raw.trim().toLowerCase().replace(/\s+/g," ");
  if(["revenue","sales","income"].includes(s))return "Revenue";
  if(["direct cost","direct costs","cost of sales","cogs"].includes(s))return "Direct costs";
  if(["operating cost","operating costs","overhead","overheads","opex"].includes(s))return "Operating costs";
  throw Error('Invalid Type "'+raw+'". Use Revenue, Direct costs or Operating costs.');
}
function money(raw,n){
  const value=raw.trim().replace(/ /g,"");
  if(!/^(?:0|[1-9]\d*)(?:\.\d{1,2})?$/.test(value))throw Error("Row "+n+": invalid amount '"+raw+"'. Use positive GBP values such as 120000 or 120000.50, with costs shown as positive.");
  const pence=Math.round(Number(value)*100);
  if(!Number.isSafeInteger(pence))throw Error("Row "+n+": amount is too large.");
  return pence;
}
function parse(text){
  const raw=csvRows(text);
  if(raw.length<2)throw Error("Add a header and at least one data row.");
  if(raw.length>5001)throw Error("The maximum is 5,000 data rows.");
  const header=raw[0].map(s=>s.trim().toLowerCase().replace(/\s+/g," "));
  if(header.length!==6||new Set(header).size!==6||COLUMNS.some(c=>!header.includes(c)))throw Error("Required CSV headers: Month, Line item, Type, Actual, Budget, Prior year. Column order may vary.");
  const idx=COLUMNS.map(c=>header.indexOf(c));
  const records=[],seen=new Set(),types=new Map();
  for(let i=1;i<raw.length;i++){
    const cells=raw[i];const line=i+1;
    if(cells.length!==header.length)throw Error("Row "+line+": expected 6 columns, found "+cells.length+".");
    const [month,name,rawType,actual,budget,prior]=idx.map(j=>cells[j].trim());
    if(!/^20\d{2}-(0[1-9]|1[0-2])$/.test(month))throw Error("Row "+line+": month must be YYYY-MM, e.g. 2026-09.");
    if(!name||name.length>100)throw Error("Row "+line+": Line item must contain 1 to 100 characters.");
    let type;
    try{type=typeOf(rawType)}catch(e){throw Error("Row "+line+": "+e.message)}
    const key=[month,type.toLowerCase(),name.toLowerCase()].join("|");
    if(seen.has(key))throw Error("Row "+line+": duplicate Month, Type and Line item.");
    seen.add(key);
    const entry={month,name,type,actual:money(actual,line),budget:money(budget,line),prior:money(prior,line)};
    records.push(entry);
    if(!types.has(month))types.set(month,new Set());
    types.get(month).add(type);
  }
  for(const [month,found] of types){
    if(!found.has("Revenue"))throw Error(month+": add at least one Revenue line.");
    if(!found.has("Direct costs")&&!found.has("Operating costs"))throw Error(month+": add at least one cost line.");
  }
  return {records,months:[...types.keys()].sort().reverse(),rowCount:records.length};
}
function summation(rows,field){return rows.reduce((n,r)=>n+r[field],0)}
function analyse(data,month,thresholdPct=5,thresholdGBP=5000){
  if(!data.months.includes(month))throw Error("Month not found in this file.");
  if(!Number.isFinite(thresholdPct)||thresholdPct<0||!Number.isFinite(thresholdGBP)||thresholdGBP<0)throw Error("Variance thresholds must be zero or above.");
  const lines=data.records.filter(r=>r.month===month);
  const periods=["actual","budget","prior"];
  const totals={};
  for(const period of periods){
    const rev=summation(lines.filter(r=>r.type==="Revenue"),period);
    const direct=summation(lines.filter(r=>r.type==="Direct costs"),period);
    const opex=summation(lines.filter(r=>r.type==="Operating costs"),period);
    totals[period]={revenue:rev,direct,gross:rev-direct,opex,ebitda:rev-direct-opex};
  }
  const delta=(metric)=>totals.actual[metric]-totals.budget[metric];
  const bridge={revenue:delta("revenue"),direct:-delta("direct"),opex:-delta("opex"),ebitda:delta("ebitda")};
  const bridgeOk=bridge.revenue+bridge.direct+bridge.opex===bridge.ebitda;
  const flags=lines.map(r=>{
    const diff=r.actual-r.budget;
    const pct=r.budget===0?null:100*diff/Math.abs(r.budget);
    const adverse=r.type==="Revenue"?diff<0:diff>0;
    const material=Math.abs(diff)>=Math.round(thresholdGBP*100)&&(pct===null?Math.abs(diff)>0:Math.abs(pct)>=thresholdPct);
    return {...r,diff,pct,adverse,material};
  }).filter(r=>r.material).sort((a,b)=>Number(b.adverse)-Number(a.adverse)||Math.abs(b.diff)-Math.abs(a.diff));
  return {month,lines,totals,bridge,bridgeOk,flags,thresholdPct,thresholdGBP,rows:lines.length};
}
return {csvRows,parse,analyse,COLUMNS};
});
