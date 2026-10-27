from pathlib import Path
import csv,gzip,json,sys
import pandas as pd
ROOT=Path(__file__).resolve().parent.parent
D=ROOT/'data'
checks={}
full_sum=0; full_cost=0; count=0; seen=set()
with gzip.open(D/'FactSales_1400000.csv.gz','rt',newline='') as f:
    for r in csv.DictReader(f):
        oid=r['OrderID'];
        if oid in seen: raise AssertionError('Duplicate OrderID '+oid)
        seen.add(oid);count+=1
        # Round to cents using integer arithmetic to avoid floating point discrepancies.
        full_sum+=round(float(r['RevenueUSD'])*100)
        full_cost+=round(float(r['COGSUSD'])*100)
checks['unique detailed orders']= (count==1400000 and len(seen)==count)
a=pd.read_csv(D/'FactSalesMonthly.csv')
p=pd.read_csv(D/'FactPlan.csv')
actual_sum=round(float(a.RevenueUSD.sum())*100);cost_sum=round(float(a.COGSUSD.sum())*100)
checks['detail revenue equals monthly actual revenue, nearest cent']=abs(full_sum-actual_sum)<=2
checks['detail cost equals monthly actual cost, nearest cent']=abs(full_cost-cost_sum)<=2
checks['actual gross profit equals revenue less cost']=((a.GrossProfitUSD-(a.RevenueUSD-a.COGSUSD)).abs()<0.015).all()
checks['unique monthly actual business keys']=not a.duplicated(['PeriodStart','Channel','Market','Category']).any()
checks['unique plan business keys']=not p.duplicated(['PeriodStart','Channel','Market','Category','PlanVersion']).any()
checks['all expected plan versions']=set(p.PlanVersion)=={'Budget 2026','Forecast Apr 2026','Forecast Jul 2026','Forecast Sep 2026'}
checks['all plans are calendar 2026']=p.PeriodStart.astype(str).str.startswith('2026-').all()
checks['no negative or illogical actual revenue and costs']=((a.RevenueUSD>=a.COGSUSD)&(a.COGSUSD>=0)).all()
checks['one-to-one monthly segment and version coverage']=p.groupby(['PeriodStart','Channel','Market','Category']).PlanVersion.nunique().eq(4).all()
checks['no missing calendar dimension links']=set(a.PeriodStart).issubset(set(pd.read_csv(D/'DimDate.csv').Date))
for label,ok in checks.items():print(('PASS' if ok else 'FAIL')+' | '+label)
print('Detail sales: USD',format(full_sum/100,',.2f'))
print('Actual rows:',len(a),' | Plan rows:',len(p),' | Detailed orders:',count)
if not all(checks.values()):sys.exit('One or more tests failed')
print('ALL',len(checks),'VALIDATIONS PASS')
