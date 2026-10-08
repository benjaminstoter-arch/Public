"use strict";
const assert=require("node:assert/strict");
const engine=require("../fpa-core.js");
const sample=`Month,Line item,Type,Actual,Budget,Prior year
2026-09,Services,Revenue,110000,100000,90000
2026-09,Delivery,Direct costs,60000,55000,50000
2026-09,Payroll,Operating costs,30000,28000,27000`;
const d=engine.parse(sample),r=engine.analyse(d,"2026-09",5,1000);
assert.equal(r.totals.actual.ebitda,2000000);
assert.equal(r.totals.budget.ebitda,1700000);
assert.equal(r.bridge.ebitda,300000);
assert.equal(r.bridgeOk,true);
assert.equal(r.flags.length,3);
assert.equal(r.flags.filter(x=>x.adverse).length,2);
assert.equal(engine.csvRows('A,B\r\n"Smith, John","Line ""A"""')[1][0],"Smith, John");
assert.throws(()=>engine.parse(sample.replace("110000","abc")),/invalid amount/i);
assert.throws(()=>engine.parse(sample+"\n2026-09,Services,Revenue,10,10,10"),/duplicate/i);
assert.throws(()=>engine.parse(sample.replace("2026-09","2026-13")),/month must/i);
assert.throws(()=>engine.parse(sample.replace("Revenue","Unexpected")),/Invalid Type/);
console.log("PASS: 10 reporting engine checks");
