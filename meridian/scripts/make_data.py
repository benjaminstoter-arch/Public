from pathlib import Path
import numpy as np, pandas as pd, json, gzip, csv
root=Path(__file__).resolve().parent.parent; data=root/'data';data.mkdir(parents=True,exist_ok=True)
rng=np.random.default_rng(20261027)
months=pd.period_range('2023-01','2026-09',freq='M')
w=np.array([{'2023':0.83,'2024':1.02,'2025':1.18,'2026':1.30}[str(p.year)]*(1.18 if p.month in (11,12) else 1.0)*(0.92 if p.month in (1,2) else 1) for p in months]); w=w/w.sum()
counts=np.floor(w*1_400_000).astype('int');counts[-1]+=1_400_000-counts.sum()
monthix=np.repeat(np.arange(len(months)),counts);rng.shuffle(monthix)
N=len(monthix);print('Building',N,'synthetic orders',flush=True)
channels=np.array(['Online','Stores','B2B']); regions=np.array(['United Kingdom','Germany','France','Netherlands']);cats=np.array(['Computing','Mobile','Audio','Gaming','Accessories'])
ci=rng.choice(3,N,p=[0.44,0.34,0.22]);ri=rng.choice(4,N,p=[0.42,0.28,0.18,0.12]);ki=rng.choice(5,N,p=[0.26,0.26,0.19,0.17,0.12]);day=rng.integers(1,29,N)
base=np.array([780,620,205,410,68]);units=rng.choice([1,2,3],N,p=[0.83,0.14,0.03]);discount=np.array([0.96,1.00,0.90])[ci];regionadj=np.array([1.06,1.02,0.97,1.04])[ri]
prc=base[ki]*np.exp(rng.normal(0,0.37,N))*discount*regionadj*units
sales=np.maximum(9,np.round(prc,2));cost=np.round(sales*(np.array([0.76,0.72,0.68,0.74,0.61])[ki]+rng.normal(0,0.025,N)).clip(0.40,0.90),2)
# Date strings ISO; 1.4m detailed rows compressed directly
mstrings=np.array([str(p) for p in months]); date=np.char.add(np.char.add(mstrings[monthix],'-'),np.char.zfill(day.astype(str),2))
df=pd.DataFrame({'OrderID':np.arange(1,N+1,dtype=np.int32),'OrderDate':date,'PeriodStart':np.char.add(mstrings[monthix],'-01'),'Channel':channels[ci],'Market':regions[ri],'Category':cats[ki],'Units':units,'RevenueUSD':sales,'COGSUSD':cost})
# A full compressed detail file, plus flat aggregates and a smaller fast-preview file
agg=df.groupby(['PeriodStart','Channel','Market','Category'],as_index=False,observed=True).agg(Orders=('OrderID','size'),Units=('Units','sum'),RevenueUSD=('RevenueUSD','sum'),COGSUSD=('COGSUSD','sum'))
agg['GrossProfitUSD']=(agg.RevenueUSD-agg.COGSUSD).round(2)
agg.to_csv(data/'FactSalesMonthly.csv',index=False,float_format='%.2f')
df.iloc[:25000].to_csv(data/'FactSales_Sample25000.csv',index=False,float_format='%.2f')
with gzip.open(data/'FactSales_1400000.csv.gz','wt',compresslevel=4,newline='') as gz: df.to_csv(gz,index=False,float_format='%.2f')
print('Detail compressed', round((data/'FactSales_1400000.csv.gz').stat().st_size/1e6,1),'MB',flush=True)
# Budget 2026 is intentionally ~10% above 2026 actual; B2B causes most of the gap
pp=[]
for mo in range(1,13):
    date=f'2026-{mo:02d}-01'; past=f'2025-{mo:02d}-01'
    target=agg[agg.PeriodStart==date] if mo<=9 else agg[agg.PeriodStart==past]
    for r in target.itertuples(index=False):
        base_rev=float(r.RevenueUSD)*(1 if mo<=9 else 1.17)
        gm=float(r.GrossProfitUSD)/float(r.RevenueUSD)
        # Channels: B2B has the sharpest gap; web and store closer to plan
        k={'Online':1.045,'Stores':1.065,'B2B':1.235}[r.Channel]
        bud=base_rev*k
        # seasonal forecast revisions, latest near actual YTD
        for vers,fact in [('Budget 2026',1),('Forecast Apr 2026',0.985),('Forecast Jul 2026',0.955),('Forecast Sep 2026',0.925)]:
            if vers!='Budget 2026' and mo<=9:
                # early months actualised and future months dampened
                v=base_rev*(1.01 if vers=='Forecast Apr 2026' else 1.005 if vers=='Forecast Jul 2026' else 1.0)
            else:v=bud*fact
            pp.append((date,r.Channel,r.Market,r.Category,vers,round(v,2),round(v*gm,2)))
plan=pd.DataFrame(pp,columns=['PeriodStart','Channel','Market','Category','PlanVersion','RevenueUSD','GrossProfitUSD'])
plan.to_csv(data/'FactPlan.csv',index=False,float_format='%.2f')
for name,vals in [('DimChannel',channels),('DimMarket',regions),('DimCategory',cats)]:
    pd.DataFrame({name.replace('Dim',''):vals}).to_csv(data/f'{name}.csv',index=False)
pd.DataFrame({'PlanVersion':['Budget 2026','Forecast Apr 2026','Forecast Jul 2026','Forecast Sep 2026']}).to_csv(data/'DimPlanVersion.csv',index=False)
pd.DataFrame({'Comparison':['PY','BU','FC']}).to_csv(data/'DimComparison.csv',index=False)
dates=pd.date_range('2023-01-01','2026-12-31')
pd.DataFrame({'Date':dates.strftime('%Y-%m-%d'),'PeriodStart':dates.strftime('%Y-%m-01'),'Year':dates.year,'Month':dates.month,'YearMonth':dates.strftime('%Y-%m')}).to_csv(data/'DimDate.csv',index=False)
# Reduced metadata for JS dashboard, all values from grouped actual and scenarios
actual=[{'m':r.PeriodStart[:7],'ch':r.Channel,'geo':r.Market,'cat':r.Category,'rev':round(r.RevenueUSD,2),'gp':round(r.GrossProfitUSD,2),'orders':int(r.Orders)} for r in agg.itertuples(index=False)]
plans=[{'m':r.PeriodStart[:7],'ch':r.Channel,'geo':r.Market,'cat':r.Category,'v':r.PlanVersion,'rev':round(r.RevenueUSD,2),'gp':round(r.GrossProfitUSD,2)} for r in plan.itertuples(index=False)]
with open(data/'dashboard_data.json','w') as f:json.dump({'actual':actual,'plans':plans,'metadata':{'orders':N,'start':'2023-01','end':'2026-09','currency':'USD','synthetic':True,'scenario':'Meridian Electronics'}},f,separators=(',',':'))
# Hard accounting controls
assert len(df)==1400000
assert abs(df.RevenueUSD.sum()-agg.RevenueUSD.sum())<0.1
assert all(agg.RevenueUSD>=agg.COGSUSD)
assert set(plan.PlanVersion)=={'Budget 2026','Forecast Apr 2026','Forecast Jul 2026','Forecast Sep 2026'}
summary={'order_rows':N,'actual_revenue_usd':round(float(df.RevenueUSD.sum()),2),'actual_cogs_usd':round(float(df.COGSUSD.sum()),2),'plan_rows':len(plan),'monthly_aggregate_rows':len(agg),'tests':{'order_count':'PASS','revenue_reconciles':'PASS','gross_profit_non_negative':'PASS','forecast_versions':'PASS'}}
(data/'qa_results.json').write_text(json.dumps(summary,indent=2));print(summary,flush=True)
