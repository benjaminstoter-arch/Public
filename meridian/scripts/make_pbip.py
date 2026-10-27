from pathlib import Path
import json,uuid,random,hashlib,textwrap
R=Path(__file__).resolve().parent.parent
name='Meridian_Commercial_Performance';P=R/'PowerBI';S=P/(name+'.SemanticModel');H=P/(name+'.Report');(S/'definition'/'tables').mkdir(parents=True,exist_ok=True);(H/'definition'/'pages').mkdir(parents=True,exist_ok=True)
def j(p,o):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(o,indent=2,ensure_ascii=False),encoding='utf8')
PBI='https://developer.microsoft.com/json-schemas/fabric/'
j(P/(name+'.pbip'),{'$schema':PBI+'pbip/pbipProperties/1.0.0/schema.json','version':'1.0','artifacts':[{'report':{'path':name+'.Report'}}],'settings':{'enableAutoRecovery':True}})
j(S/'definition.pbism',{'$schema':PBI+'item/semanticModel/definitionProperties/1.0.0/schema.json','version':'4.2','settings':{'qnaEnabled':False}})
(S/'definition'/'database.tmdl').write_text('database Meridian_Commercial_Performance\n\tcompatibilityLevel: 1606\n',encoding='utf8')
tables=['DimDate','DimChannel','DimMarket','DimCategory','DimPlanVersion','DimComparison','FactSalesMonthly','FactPlan']
model='model Model\n\tculture: en-US\n\tdefaultPowerBIDataSourceVersion: powerBI_V3\n\tsourceQueryCulture: en-US\n\n'+''.join('\tref table '+t+'\n' for t in tables)
(S/'definition'/'model.tmdl').write_text(model)
(S/'definition'/'expressions.tmdl').write_text('expression pDataRoot = "REPLACE_WITH_ABSOLUTE_DATA_PATH" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]\n',encoding='utf8')
cols={
'DimDate':[('Date','dateTime'),('PeriodStart','dateTime'),('Year','int64'),('Month','int64'),('YearMonth','string')],
'DimChannel':[('Channel','string')], 'DimMarket':[('Market','string')], 'DimCategory':[('Category','string')],
'DimPlanVersion':[('PlanVersion','string')], 'DimComparison':[('Comparison','string')],
'FactSalesMonthly':[('PeriodStart','dateTime'),('Channel','string'),('Market','string'),('Category','string'),('Orders','int64'),('Units','int64'),('RevenueUSD','double'),('COGSUSD','double'),('GrossProfitUSD','double')],
'FactPlan':[('PeriodStart','dateTime'),('Channel','string'),('Market','string'),('Category','string'),('PlanVersion','string'),('RevenueUSD','double'),('GrossProfitUSD','double')]}
measures=[
('Revenue AC',"SUM('FactSalesMonthly'[RevenueUSD])",'$#,##0;($#,##0)'),
('COGS AC',"SUM('FactSalesMonthly'[COGSUSD])",'$#,##0;($#,##0)'),
('Gross Profit AC',"SUM('FactSalesMonthly'[GrossProfitUSD])",'$#,##0;($#,##0)'),
('Gross Margin AC',"DIVIDE([Gross Profit AC],[Revenue AC])",'0.0%;(0.0%)'),
('Orders AC',"SUM('FactSalesMonthly'[Orders])",'#,##0'),
('Revenue PY',"CALCULATE([Revenue AC],DATEADD('DimDate'[Date],-1,YEAR))",'$#,##0;($#,##0)'),
('Revenue BU',"CALCULATE(SUM('FactPlan'[RevenueUSD]),'DimPlanVersion'[PlanVersion]=\"Budget 2026\")",'$#,##0;($#,##0)'),
('Revenue FC',"CALCULATE(SUM('FactPlan'[RevenueUSD]),'DimPlanVersion'[PlanVersion]=\"Forecast Sep 2026\")",'$#,##0;($#,##0)'),
('Revenue Compare',"SWITCH(SELECTEDVALUE('DimComparison'[Comparison],\"BU\"),\"PY\",[Revenue PY],\"BU\",[Revenue BU],\"FC\",[Revenue FC])",'$#,##0;($#,##0)'),
('Revenue Variance',"[Revenue AC]-[Revenue Compare]",'$#,##0;($#,##0)'),
('Revenue Variance %',"DIVIDE([Revenue Variance],[Revenue Compare])",'0.0%;(0.0%)'),
('Gross Profit BU',"CALCULATE(SUM('FactPlan'[GrossProfitUSD]),'DimPlanVersion'[PlanVersion]=\"Budget 2026\")",'$#,##0;($#,##0)'),
('Gross Profit FC',"CALCULATE(SUM('FactPlan'[GrossProfitUSD]),'DimPlanVersion'[PlanVersion]=\"Forecast Sep 2026\")",'$#,##0;($#,##0)'),
('Gross Profit PY',"CALCULATE([Gross Profit AC],DATEADD('DimDate'[Date],-1,YEAR))",'$#,##0;($#,##0)'),
('Gross Profit Compare',"SWITCH(SELECTEDVALUE('DimComparison'[Comparison],\"BU\"),\"PY\",[Gross Profit PY],\"BU\",[Gross Profit BU],\"FC\",[Gross Profit FC])",'$#,##0;($#,##0)'),
('Gross Profit Variance',"[Gross Profit AC]-[Gross Profit Compare]",'$#,##0;($#,##0)'),
]
for table,fields in cols.items():
    lines=['table '+table,'']
    for n,t in fields:
        lines+=['\t/// '+('Unique date for time intelligence' if table=='DimDate' and n=='Date' else n+' source field'), '\tcolumn '+n, '\t\tdataType: '+t,'\t\tsummarizeBy: none','\t\tsourceColumn: '+n,'']
    if table=='FactSalesMonthly':
        for n,expr,fmt in measures:
            lines+=['\t/// '+n+' in USD unless formatted as a ratio or count','\tmeasure '+("'"+n+"'")+' = '+expr,'\t\tformatString: '+fmt,'']
    # Convert ISO date strings to date types in Power Query; columns use dateTime in tabular model
    types=', '.join('{"'+n+'", '+('type date' if t=='dateTime' else 'Int64.Type' if t=='int64' else 'type number' if t=='double' else 'type text')+'}' for n,t in fields)
    m=['let','    Source = Csv.Document(File.Contents(pDataRoot & "\\\\'+table+'.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),','    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),','    Typed = Table.TransformColumnTypes(Headers, {'+types+'}, "en-US")','in','    Typed']
    if table=='FactSalesMonthly':m[1]=m[1].replace(table+'.csv','FactSalesMonthly.csv')
    lines+=['\tpartition '+table+' = m','\t\tmode: import','\t\tsource =']+['\t\t\t'+k for k in m]
    (S/'definition'/'tables'/(table+'.tmdl')).write_text('\n'.join(lines)+'\n',encoding='utf8')
rels=[]
for fac in ['FactSalesMonthly','FactPlan']:
    for column,dim,target in [('PeriodStart','DimDate','Date'),('Channel','DimChannel','Channel'),('Market','DimMarket','Market'),('Category','DimCategory','Category')]:
        rels+=['relationship '+str(uuid.uuid4()),'\tfromColumn: '+fac+'.'+column,'\ttoColumn: '+dim+'.'+target,'']
rels+=['relationship '+str(uuid.uuid4()),'\tfromColumn: FactPlan.PlanVersion','\ttoColumn: DimPlanVersion.PlanVersion','']
(S/'definition'/'relationships.tmdl').write_text('\n'.join(rels),encoding='utf8')
for folder,typ in [(S,'SemanticModel'),(H,'Report')]:j(folder/'.platform',{'$schema':PBI+'gitIntegration/platformProperties/2.0.0/schema.json','metadata':{'type':typ,'displayName':'Ben Stoter | Meridian Commercial Performance'},'config':{'version':'2.0','logicalId':str(uuid.uuid4())}})
j(H/'definition.pbir',{'$schema':PBI+'item/report/definitionProperties/2.0.0/schema.json','version':'4.0','datasetReference':{'byPath':{'path':'../'+name+'.SemanticModel'}}})
j(H/'definition'/'version.json',{'$schema':PBI+'item/report/definition/versionMetadata/1.0.0/schema.json','version':'2.0.0'})
# Self-contained Ben Stoter theme; can also be imported manually in Power BI Desktop.
theme={'name':'Ben Stoter | Gold and Taupe','dataColors':['#BB974B','#ACA18B','#414141','#D6C8B1','#76847C','#B95D56','#477D70','#5D6059'],'background':'#FAF9F6','foreground':'#414141','tableAccent':'#BB974B','textClasses':{'title':{'fontFace':'Georgia','fontSize':14,'color':'#414141'},'label':{'fontFace':'Arial','fontSize':10,'color':'#414141'}}}
j(R/'Ben_Stoter_Meridian_PowerBI_Theme.json',theme);j(H/'StaticResources'/'RegisteredResources'/'Ben_Stoter_Meridian_Theme.json',theme)
j(H/'definition'/'report.json',{'$schema':PBI+'item/report/definition/report/3.2.0/schema.json','themeCollection':{'customTheme':{'name':'Ben_Stoter_Meridian_Theme.json','reportVersionAtImport':{'visual':'2.7.0','report':'3.2.0','page':'2.1.0'},'type':'RegisteredResources'}},'filterConfig':{'filters':[]},'settings':{'useEnhancedTooltips':True,'useStylableVisualContainerHeader':True,'defaultDrillFilterOtherVisuals':True},'resourcePackages':[{'name':'RegisteredResources','type':'RegisteredResources','items':[{'name':'Ben_Stoter_Meridian_Theme.json','path':'Ben_Stoter_Meridian_Theme.json','type':'CustomTheme'}]}]})
# Native PBIR visual definitions. The HTML preview is the visually QA-tested reference for final alignment.
def slug(*parts):return hashlib.md5('|'.join(parts).encode()).hexdigest()[:20]
def meas(n):return {'field':{'Measure':{'Expression':{'SourceRef':{'Entity':'FactSalesMonthly'}},'Property':n}},'queryRef':'FactSalesMonthly.'+n,'nativeQueryRef':n}
def col(t,n):return {'field':{'Column':{'Expression':{'SourceRef':{'Entity':t}},'Property':n}},'queryRef':t+'.'+n,'nativeQueryRef':n}
def visual(page,vname,visualtype,x,y,w,h,roles):
    obj={'$schema':PBI+'item/report/definition/visualContainer/2.7.0/schema.json','name':slug(page,vname),'position':{'x':x,'y':y,'z':0,'height':h,'width':w,'tabOrder':0},'visual':{'visualType':visualtype,'query':{'queryState':{a:{'projections':b} for a,b in roles.items()}},'drillFilterOtherVisuals':True}}
    j(H/'definition'/'pages'/slug('page',page)/'visuals'/slug(page,vname)/'visual.json',obj)
pageids=[]
config=[('Executive overview','DimChannel','Channel'),('Channel performance','DimChannel','Channel'),('Product contribution','DimCategory','Category'),('Geographic analysis','DimMarket','Market'),('Monthly development','DimDate','YearMonth'),('Planning & versions','DimPlanVersion','PlanVersion')]
for pn,table,colname in config:
    id=slug('page',pn);pageids.append(id);p=H/'definition'/'pages'/id
    j(p/'page.json',{'$schema':PBI+'item/report/definition/page/2.1.0/schema.json','name':id,'displayName':pn,'displayOption':'FitToPage','height':720,'width':1280})
    visual(pn,'Revenue AC','cardVisual',30,34,270,115,{'Data':[meas('Revenue AC')]})
    visual(pn,'Revenue Compare','cardVisual',323,34,270,115,{'Data':[meas('Revenue Compare')]})
    visual(pn,'Variance','cardVisual',616,34,270,115,{'Data':[meas('Revenue Variance %')]})
    visual(pn,'Gross Profit','cardVisual',908,34,340,115,{'Data':[meas('Gross Profit AC')]})
    visual(pn,'Monthly revenue','clusteredColumnChart',30,175,785,330,{'Category':[col('DimDate','YearMonth')],'Y':[meas('Revenue AC'),meas('Revenue Compare')]})
    visual(pn,'Segment comparison','clusteredBarChart',837,175,410,330,{'Category':[col(table,colname)],'Y':[meas('Revenue AC'),meas('Revenue Compare')]})
    visual(pn,'AC and Variance','lineChart',30,520,785,170,{'Category':[col('DimDate','YearMonth')],'Y':[meas('Revenue AC'),meas('Revenue Compare')]})
    visual(pn,'Comparison','slicer',840,533,188,145,{'Values':[col('DimComparison','Comparison')]})
    visual(pn,'Year','slicer',1055,533,188,145,{'Values':[col('DimDate','Year')]})
j(H/'definition'/'pages'/'pages.json',{'$schema':PBI+'item/report/definition/pagesMetadata/1.0.0/schema.json','pageOrder':pageids,'activePageName':pageids[0]})
# Installer patches a parameter to local absolute data directory. Use monthly aggregates for quick test.
installer='''from pathlib import Path
import sys
root=Path(__file__).resolve().parent.parent
model=root/'PowerBI'/'Meridian_Commercial_Performance.SemanticModel'/'definition'/'expressions.tmdl'
data=str((root/'data').resolve()).replace('"','')
model.write_text('expression pDataRoot = "'+data+'" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]\\n',encoding='utf8')
print('Configured Power BI data root:',data)
print('Now open PowerBI/Meridian_Commercial_Performance.pbip in Power BI Desktop (Windows).')
'''
(R/'scripts').mkdir(exist_ok=True);(R/'scripts'/'configure_project.py').write_text(installer,encoding='utf8')
(R/'.gitignore').write_text('**/.pbi/localSettings.json\n**/.pbi/cache.abf\n**/.DS_Store\n')
print('Project files:',sum(1 for p in P.rglob('*') if p.is_file()))
