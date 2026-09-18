import io, csv
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title='NEÀPOLIS IMPACT', page_icon='◆', layout='wide', initial_sidebar_state='expanded')

st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:Inter,sans-serif}.block-container{max-width:1580px;padding-top:1rem;padding-bottom:2rem}
[data-testid="stAppViewContainer"]{background:#F4F7FA}[data-testid="stSidebar"]{background:#071321;border-right:1px solid #183047}[data-testid="stSidebar"] *{color:#EAF0F7}
#MainMenu,footer,header{visibility:hidden}.hero{background:linear-gradient(118deg,#061426 0%,#0D2B45 62%,#0D6671 100%);border-radius:24px;padding:30px 36px;color:white;box-shadow:0 18px 45px rgba(15,23,42,.15);margin-bottom:18px;position:relative;overflow:hidden}.hero:after{content:"";position:absolute;width:330px;height:330px;border-radius:50%;right:-105px;top:-170px;background:rgba(255,255,255,.055)}
.badge{display:inline-block;padding:7px 11px;border-radius:999px;background:#FFF0C2;color:#8A4A06;font-size:10px;font-weight:800;letter-spacing:.07em}.eyebrow{font-size:10px;letter-spacing:.20em;text-transform:uppercase;font-weight:800;color:#A9C2D8;margin-top:15px}.hero h1{font-size:39px;letter-spacing:-.045em;margin:8px 0 9px}.hero p{font-size:14px;color:#D6E3EE;max-width:1040px;margin:0;line-height:1.55}
.kpi{background:white;border:1px solid #DDE7EF;border-radius:18px;padding:15px 16px;min-height:112px;box-shadow:0 6px 20px rgba(15,23,42,.045)}.klabel{font-size:9.5px;font-weight:800;letter-spacing:.08em;color:#69778B;text-transform:uppercase}.kvalue{font-size:27px;font-weight:800;color:#0F172A;letter-spacing:-.045em;margin-top:8px}.ksub{font-size:10.5px;color:#758398;margin-top:4px}.section{font-size:21px;font-weight:800;letter-spacing:-.025em;color:#101827;margin:18px 0 3px}.sub{font-size:11.5px;color:#6B778A;margin-bottom:12px}
.callout{background:#EAF5FF;border:1px solid #CFE6FB;color:#194E7E;border-radius:14px;padding:13px 16px;font-size:12px;margin:9px 0 14px}.datebar{background:white;border:1px solid #DCE6EE;border-radius:18px;padding:16px 18px;box-shadow:0 5px 18px rgba(15,23,42,.04);margin-bottom:14px}.riskpanel{background:#0A1728;border:1px solid #1A3855;border-radius:22px;padding:22px 26px;color:white;box-shadow:0 12px 34px rgba(15,23,42,.13)}.lights{display:flex;gap:15px;align-items:center;margin:12px 0}.light{width:54px;height:54px;border-radius:50%;opacity:.18;border:5px solid rgba(255,255,255,.12)}.light.on{opacity:1;box-shadow:0 0 0 8px rgba(255,255,255,.05),0 0 28px currentColor}.risk-big{font-size:34px;font-weight:800;letter-spacing:-.04em}.risk-caption{color:#BBD0E2;font-size:12px;line-height:1.55}.menu-card{background:white;border:1px solid #DFE7EF;border-radius:17px;padding:17px;min-height:112px;box-shadow:0 4px 15px rgba(15,23,42,.035)}.menu-title{font-size:15px;font-weight:800;color:#111827}.menu-copy{font-size:11px;color:#66758A;line-height:1.45;margin-top:5px}.group-title{font-size:11px;font-weight:800;letter-spacing:.11em;color:#64748B;text-transform:uppercase;margin:19px 0 8px}.method{background:#0D1B2D;color:#D8E5F3;border-radius:17px;padding:18px 20px;font-size:11.5px;line-height:1.7}.method b{color:white}.status-good{color:#15803D;font-weight:800}.status-warn{color:#B45309;font-weight:800}.status-bad{color:#B91C1C;font-weight:800}
div[data-testid="stDataFrame"]{background:white;border:1px solid #DFE7EF;border-radius:14px;padding:4px}[data-testid="stFileUploader"]{background:white;border:1px dashed #A9B8C8;border-radius:14px;padding:7px}.stExpander{background:white;border-radius:12px}
</style>''', unsafe_allow_html=True)

# ---------- DEMO: only primary/source data ----------
@st.cache_data
def make_demo():
    rng=np.random.default_rng(12)
    projects=pd.DataFrame([
        ['P01','Campus Europeu d’Emprenedoria Disruptiva',500000,'2026-01-15','2027-12-31','En execució'],
        ['P02','Urban Innovation Lab',320000,'2026-03-01','2027-08-31','En execució'],
        ['P03','Digital Talent VNG',260000,'2025-09-01','2026-12-31','En execució']
    ],columns=['Project_ID','Project','Budget','Start_date','End_date','Status'])
    wps=[]
    defs=[('WP1','Gestió i governança','PMO',60000),('WP2','Selecció i baseline','WP Lead',45000),('WP3','Acceleració','WP Lead',105000),('WP4','Experimentació','WP4 Lead',115000),('WP5','Mercat i internacionalització','WP Lead',75000),('WP6','Impacte i retorn','Impact Lead',65000),('WP7','Comunicació i transferència','Comms Lead',35000)]
    for wp,n,o,b in defs:wps.append(['P01',wp,n,o,b,'2026-01-15','2027-12-31'])
    for pid in ['P02','P03']:
        for wp,n,o,b in defs[:5]: wps.append([pid,wp,n,o,int(b*.62),'2026-03-01' if pid=='P02' else '2025-09-01','2027-08-31' if pid=='P02' else '2026-12-31'])
    wps=pd.DataFrame(wps,columns=['Project_ID','WP','Name','Owner','Budget','Start_date','End_date'])

    # Deliverables are the source of planned/real progress. Weight sums to 100 per WP.
    deliverables=[]
    base_due=[date(2026,3,15),date(2026,6,30),date(2026,9,30),date(2026,12,20),date(2027,5,31),date(2027,10,31)]
    weights=[15,15,20,20,15,15]
    for _,r in wps.iterrows():
        shift={'WP1':0,'WP2':-25,'WP3':20,'WP4':35,'WP5':55,'WP6':75,'WP7':95}.get(r.WP,0)
        for j,(bd,w) in enumerate(zip(base_due,weights),1):
            due=bd+timedelta(days=shift)
            # demo completion pattern; WP4 intentionally problematic
            actual=None
            if r.Project_ID=='P01':
                if due <= date(2026,8,25): actual=due+timedelta(days=int(rng.integers(-5,7)))
                elif r.WP in ['WP1','WP3','WP5'] and due<=date(2026,9,10): actual=due+timedelta(days=int(rng.integers(0,8)))
                if r.WP=='WP4' and j==2: actual=due+timedelta(days=18)
            else:
                if due <= date(2026,9,5): actual=due+timedelta(days=int(rng.integers(-4,10)))
            deliverables.append([r.Project_ID,r.WP,f'D-{r.WP}-{j}',f'Lliurable {r.WP}.{j}',due.isoformat(),actual.isoformat() if actual else '',w,r.Owner])
    deliverables=pd.DataFrame(deliverables,columns=['Project_ID','WP','Deliverable_ID','Deliverable','Due_date','Actual_date','Weight','Owner'])

    milestones=[]
    for _,r in wps.iterrows():
        for j in range(1,5):
            due=date(2026,2,28)+timedelta(days=85*j+({'WP4':25,'WP6':45}.get(r.WP,0)))
            actual=''
            if due<=date(2026,8,20): actual=(due+timedelta(days=(12 if r.Project_ID=='P01' and r.WP=='WP4' and j==2 else int(rng.integers(-3,5))))).isoformat()
            milestones.append([r.Project_ID,r.WP,f'M-{r.WP}-{j}',f'Fita {r.WP}.{j}',due.isoformat(),actual,r.Owner])
    milestones=pd.DataFrame(milestones,columns=['Project_ID','WP','Milestone_ID','Milestone','Due_date','Actual_date','Owner'])

    tasks=[]; tid=1
    for _,r in wps.iterrows():
        for j in range(1,7):
            s=date(2026,1,15)+timedelta(days=(j-1)*65+({'WP4':35,'WP5':50}.get(r.WP,0)))
            e=s+timedelta(days=50)
            ae=''
            if e<=date(2026,8,30) and not(r.Project_ID=='P01' and r.WP=='WP4' and j in [3,4]): ae=(e+timedelta(days=int(rng.integers(-4,10)))).isoformat()
            tasks.append([r.Project_ID,f'T-{tid:03d}',r.WP,f'Tasca {r.WP}.{j}',r.Owner,s.isoformat(),e.isoformat(),ae,'T-'+str(tid-1).zfill(3) if j>1 else ''])
            tid+=1
    tasks=pd.DataFrame(tasks,columns=['Project_ID','Task_ID','WP','Task','Owner','Start_date','Due_date','Actual_date','Dependency_ID'])

    expenses=[]; eid=1
    for _,r in wps.iterrows():
        for j in range(1,9):
            dt=date(2026,2,1)+timedelta(days=j*28+({'WP4':15,'WP6':35}.get(r.WP,0)))
            amount=int(rng.integers(1800,9000)); evidence=0 if (r.Project_ID=='P01' and r.WP in ['WP1','WP4'] and j in [5,6,7]) else 1
            expenses.append([r.Project_ID,f'E-{eid:03d}',r.WP,dt.isoformat(),amount,evidence]) ; eid+=1
    expenses=pd.DataFrame(expenses,columns=['Project_ID','Expense_ID','WP','Date','Amount','Evidence_complete'])

    risks=pd.DataFrame([
        ['P01','R01','WP4','Dependència externa pilot','2026-07-10','',3,3,'WP4 Lead','Escalar acord amb empresa'],
        ['P01','R02','WP4','Retard en validació tècnica','2026-08-01','',3,2,'WP4 Lead','Pla de recuperació'],
        ['P01','R03','WP3','Outcome comercial sota trajectòria','2026-08-20','',2,2,'WP3 Lead','Reforçar suport comercial'],
        ['P01','R04','WP1','Evidències de despesa incompletes','2026-09-01','',2,3,'Finance / PM','Completar expedients'],
        ['P01','R05','WP6','Actualització de dades pendent','2026-08-15','2026-09-05',2,2,'Data Owner','Validar càrrega']
    ],columns=['Project_ID','Risk_ID','WP','Risk','Open_date','Close_date','Probability','Impact','Owner','Mitigation'])

    names=[f'Nexa {i:02d}' for i in range(1,21)]; sectors=['AI & Data','Blue Economy','HealthTech','ClimateTech','CreativeTech','Smart City']
    startups=pd.DataFrame([['P01',n,sectors[i%6],['MVP','Early traction','Growth'][i%3],'2026-02-15'] for i,n in enumerate(names)],columns=['Project_ID','Startup','Sector','Stage','Entry_date'])
    sm=[]
    for i,n in enumerate(names):
        jobs0=[3,4,2,5,4,3,2,4,3,5,2,4,3,4,2,3,4,3,3,3][i]; add=[1,1,1,2,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1][i]
        rev0=int(rng.integers(55,190))*1000; rev3=int(rev0*(1+float(np.clip(rng.normal(.21,.08),.03,.42))))
        inv=[150000,0,100000,250000,0,100000,50000,0,150000,0,100000,0,100000,0,50000,0,50000,0,0,0][i]
        for dt,phase,jobs,rev,invest in [('2026-02-15','T0',jobs0,rev0,0),('2026-06-30','T1',jobs0, int(rev0*1.06),0),('2026-09-15','T2',jobs0+max(0,add-1),int(rev0*1.13),int(inv*.45)),('2026-12-15','T3',jobs0+add,rev3,inv)]:
            sm.append(['P01',n,dt,phase,jobs,rev,invest, max(0,int((i%5)+1 if phase!='T0' else 0)),1 if phase in ['T2','T3'] and i<10 else 0,1 if phase=='T3' and i<14 else 0,1 if phase=='T3' and i<11 else 0,1 if phase=='T3' and i<8 else 0,1 if phase=='T3' and i<12 else 0])
    startup_metrics=pd.DataFrame(sm,columns=['Project_ID','Startup','Measurement_date','Phase','Jobs','Revenue','Investment','New_clients','Pilot','Validated_model','Local_jobs_created','Local_pilot','Verified_return'])

    activity=[]
    for dt,m,v in [('2026-03-15','Mentoring_hours',80),('2026-04-30','Mentoring_hours',75),('2026-06-15','Mentoring_hours',80),('2026-08-31','Mentoring_hours',80),('2026-03-20','Workshops',4),('2026-05-20','Workshops',4),('2026-07-20','Workshops',4),('2026-09-10','Workshops',4),('2026-04-15','Startup_company_connections',12),('2026-06-30','Startup_company_connections',16),('2026-09-15','Startup_company_connections',20),('2026-06-30','Investor_meetings',14),('2026-09-15','Investor_meetings',17)]: activity.append(['P01',dt,m,v])
    activity=pd.DataFrame(activity,columns=['Project_ID','Date','Metric','Value'])
    return {'Projects':projects,'Work_Packages':wps,'Deliverables':deliverables,'Milestones':milestones,'Tasks':tasks,'Expenses':expenses,'Risks':risks,'Startups':startups,'Startup_Metrics':startup_metrics,'Activity':activity}

REQUIRED={
'Projects':['Project_ID','Project','Budget','Start_date','End_date','Status'],
'Work_Packages':['Project_ID','WP','Name','Owner','Budget','Start_date','End_date'],
'Deliverables':['Project_ID','WP','Deliverable_ID','Deliverable','Due_date','Actual_date','Weight','Owner'],
'Milestones':['Project_ID','WP','Milestone_ID','Milestone','Due_date','Actual_date','Owner'],
'Tasks':['Project_ID','Task_ID','WP','Task','Owner','Start_date','Due_date','Actual_date','Dependency_ID'],
'Expenses':['Project_ID','Expense_ID','WP','Date','Amount','Evidence_complete'],
'Risks':['Project_ID','Risk_ID','WP','Risk','Open_date','Close_date','Probability','Impact','Owner','Mitigation'],
'Startups':['Project_ID','Startup','Sector','Stage','Entry_date'],
'Startup_Metrics':['Project_ID','Startup','Measurement_date','Phase','Jobs','Revenue','Investment','New_clients','Pilot','Validated_model','Local_jobs_created','Local_pilot','Verified_return'],
'Activity':['Project_ID','Date','Metric','Value']}

if 'raw' not in st.session_state: st.session_state.raw=make_demo(); st.session_state.mode='DEMO · DADES FICTÍCIES'
if 'nav' not in st.session_state: st.session_state.nav='HOME'

def validate(name,df): return [c for c in REQUIRED.get(name,[]) if c not in df.columns]
def excel_bytes(d):
    out=io.BytesIO()
    with pd.ExcelWriter(out,engine='xlsxwriter') as w:
        for name,df in d.items():
            df.to_excel(w,sheet_name=name[:31],index=False); ws=w.sheets[name[:31]]; ws.freeze_panes(1,0); ws.autofilter(0,0,len(df),len(df.columns)-1)
            for i,c in enumerate(df.columns): ws.set_column(i,i,min(max(len(str(c))+3,12),28))
    return out.getvalue()
def parse_paste(txt):
    try: sep=csv.Sniffer().sniff(txt[:3000],delimiters='\t,;').delimiter
    except: sep='\t'
    return pd.read_csv(io.StringIO(txt.strip()),sep=sep)
def money(v):
    if pd.isna(v): return '—'
    if abs(v)>=1e6:return f'{v/1e6:.1f} M€'.replace('.',',')
    if abs(v)>=1000:return f'{v/1000:.0f} k€'
    return f'{v:.0f} €'
def kpi(label,value,sub=''): st.markdown(f'<div class="kpi"><div class="klabel">{label}</div><div class="kvalue">{value}</div><div class="ksub">{sub}</div></div>',unsafe_allow_html=True)
def section(title,sub=''): st.markdown(f'<div class="section">{title}</div><div class="sub">{sub}</div>',unsafe_allow_html=True)
def todate(s): return pd.to_datetime(s,errors='coerce')

def derive(raw, as_of):
    d={k:v.copy() for k,v in raw.items()}; cutoff=pd.Timestamp(as_of)
    dl=d['Deliverables'].copy(); dl['Due_date']=todate(dl.Due_date); dl['Actual_date']=todate(dl.Actual_date); dl['Weight']=pd.to_numeric(dl.Weight,errors='coerce').fillna(0)
    dl['Planned_done']=(dl.Due_date<=cutoff).astype(int); dl['Real_done']=((dl.Actual_date.notna())&(dl.Actual_date<=cutoff)).astype(int)
    dl['Overdue']=((dl.Due_date<cutoff)&(dl.Real_done==0)).astype(int); dl['Delay_days']=np.where(dl.Actual_date.notna(),(dl.Actual_date-dl.Due_date).dt.days,(cutoff-dl.Due_date).dt.days); dl['Delay_days']=pd.Series(dl['Delay_days']).clip(lower=0)
    agg=dl.groupby(['Project_ID','WP']).apply(lambda g: pd.Series({'Planned_progress':(g.Weight*g.Planned_done).sum()/max(g.Weight.sum(),1),'Real_progress':(g.Weight*g.Real_done).sum()/max(g.Weight.sum(),1),'Overdue_deliverables':int(g.Overdue.sum()),'Next_due_days':int(max(0,(g.loc[g.Due_date>=cutoff,'Due_date'].min()-cutoff).days)) if (g.Due_date>=cutoff).any() else 999}),include_groups=False).reset_index()
    w=d['Work_Packages'].copy().merge(agg,on=['Project_ID','WP'],how='left'); w[['Planned_progress','Real_progress']]=w[['Planned_progress','Real_progress']].fillna(0); w['Schedule_gap']=(w.Planned_progress-w.Real_progress).clip(lower=0)
    exp=d['Expenses'].copy(); exp['Date']=todate(exp.Date); exp['Amount']=pd.to_numeric(exp.Amount,errors='coerce').fillna(0); exp['Evidence_complete']=pd.to_numeric(exp.Evidence_complete,errors='coerce').fillna(0); expc=exp[exp.Date<=cutoff]
    spend=expc.groupby(['Project_ID','WP']).Amount.sum().rename('Spent').reset_index(); docs=expc[expc.Evidence_complete==0].groupby(['Project_ID','WP']).size().rename('Docs_pending').reset_index(); w=w.merge(spend,on=['Project_ID','WP'],how='left').merge(docs,on=['Project_ID','WP'],how='left'); w[['Spent','Docs_pending']]=w[['Spent','Docs_pending']].fillna(0); w['Budget_execution']=w.Spent/pd.to_numeric(w.Budget,errors='coerce').replace(0,np.nan)
    rr=d['Risks'].copy(); rr['Open_date']=todate(rr.Open_date); rr['Close_date']=todate(rr.Close_date); rr['Probability']=pd.to_numeric(rr.Probability,errors='coerce').fillna(0); rr['Impact']=pd.to_numeric(rr.Impact,errors='coerce').fillna(0); rr['Open_asof']=((rr.Open_date<=cutoff)&((rr.Close_date.isna())|(rr.Close_date>cutoff))).astype(int)
    openr=rr[rr.Open_asof==1].groupby(['Project_ID','WP']).size().rename('Open_risks').reset_index(); w=w.merge(openr,on=['Project_ID','WP'],how='left'); w['Open_risks']=w.Open_risks.fillna(0)
    tasks=d['Tasks'].copy(); tasks['Start_date']=todate(tasks.Start_date); tasks['Due_date']=todate(tasks.Due_date); tasks['Actual_date']=todate(tasks.Actual_date); tasks['Overdue']=((tasks.Due_date<cutoff)&((tasks.Actual_date.isna())|(tasks.Actual_date>cutoff))).astype(int); dep=tasks[(tasks.Overdue==1)&tasks.Dependency_ID.astype(str).ne('')].groupby(['Project_ID','WP']).size().rename('Dependencies').reset_index(); w=w.merge(dep,on=['Project_ID','WP'],how='left'); w['Dependencies']=w.Dependencies.fillna(0)
    w['Risk_score']=(38*(w.Schedule_gap/.20).clip(0,1)+24*(w.Open_risks/3).clip(0,1)+18*(w.Docs_pending/5).clip(0,1)+10*(w.Dependencies/2).clip(0,1)+10*((30-w.Next_due_days)/30).clip(0,1)).fillna(0).round().astype(int)
    w['Risk_status']=pd.cut(w.Risk_score,[-1,39,69,100],labels=['CONTROLAT','MODERAT','ALT']).astype(str)
    ms=d['Milestones'].copy(); ms['Due_date']=todate(ms.Due_date); ms['Actual_date']=todate(ms.Actual_date); ms['Due_asof']=(ms.Due_date<=cutoff); ms['On_time_asof']=ms.Due_asof & ms.Actual_date.notna() & (ms.Actual_date<=ms.Due_date)
    sm=d['Startup_Metrics'].copy(); sm['Measurement_date']=todate(sm.Measurement_date); sm=sm[sm.Measurement_date<=cutoff].sort_values('Measurement_date'); latest=sm.groupby(['Project_ID','Startup'],as_index=False).tail(1) if len(sm) else sm
    act=d['Activity'].copy(); act['Date']=todate(act.Date); act=act[act.Date<=cutoff]
    return {'wps':w,'deliverables':dl,'expenses':expc,'risks':rr,'tasks':tasks,'milestones':ms,'startup_latest':latest,'startup_history':sm,'activity':act}

# ---------- Sidebar / filters ----------
raw=st.session_state.raw
with st.sidebar:
    st.markdown('### NEÀPOLIS IMPACT'); st.caption('Project & Impact Intelligence System'); st.markdown(f'**{st.session_state.mode}**'); st.divider()
    navs=['HOME','Seguiment del projecte','Activitat i lliurables','Resultats en startups','Impacte','Retorn territorial','Radar de riscos','Data Hub','Metodologia']
    st.session_state.nav=st.radio('Menú',navs,index=navs.index(st.session_state.nav) if st.session_state.nav in navs else 0)
    st.divider(); st.caption('Els indicadors es recalculen a partir de dades font i de la data d’anàlisi.')

projects=raw['Projects'].copy(); project_map=dict(zip(projects.Project,projects.Project_ID))
# global date bar
st.markdown(f'''<div class="hero"><span class="badge">{st.session_state.mode}</span><div class="eyebrow">PROJECT & IMPACT INTELLIGENCE SYSTEM</div><h1>NEÀPOLIS IMPACT</h1><p>Control, anticipació i impacte en una sola vista: de l’execució calendaritzada a les decisions, els resultats i el retorn territorial.</p></div>''',unsafe_allow_html=True)

c1,c2,c3,c4=st.columns([1.8,1.1,1.2,1.2])
with c1: project_name=st.selectbox('Projecte',projects.Project.tolist(),index=0); pid=project_map[project_name]
with c2:
    mode_date=st.radio('Data d’anàlisi',['Avui','Personalitzada'],horizontal=True)
with c3:
    today=date.today()
    as_of=today if mode_date=='Avui' else st.date_input('Selecciona data',value=date(2026,9,18),min_value=date(2025,1,1),max_value=date(2028,12,31))
with c4:
    sectors=['Tots']+sorted(raw['Startups'].loc[raw['Startups'].Project_ID==pid,'Sector'].dropna().unique().tolist()); sector=st.selectbox('Sector startup',sectors)

D=derive(raw,as_of); w=D['wps']; w=w[w.Project_ID==pid].copy(); dl=D['deliverables']; dl=dl[dl.Project_ID==pid]; ms=D['milestones']; ms=ms[ms.Project_ID==pid]; ex=D['expenses']; ex=ex[ex.Project_ID==pid]; risks=D['risks']; risks=risks[risks.Project_ID==pid]; tasks=D['tasks']; tasks=tasks[tasks.Project_ID==pid]
latest=D['startup_latest']; latest=latest[latest.Project_ID==pid] if len(latest) else latest
if sector!='Tots' and len(latest):
    allowed=raw['Startups'][(raw['Startups'].Project_ID==pid)&(raw['Startups'].Sector==sector)].Startup; latest=latest[latest.Startup.isin(allowed)]

real=float(w.Real_progress.mean()) if len(w) else 0; planned=float(w.Planned_progress.mean()) if len(w) else 0; maxrisk=int(w.Risk_score.max()) if len(w) else 0; riskword='ALT' if maxrisk>=70 else ('MODERAT' if maxrisk>=40 else 'CONTROLAT'); riskcolor='#EF4444' if maxrisk>=70 else ('#F59E0B' if maxrisk>=40 else '#22C55E')

if st.session_state.nav=='HOME':
    section('HOME · Visió de direcció',f'Fotografia del projecte a {pd.Timestamp(as_of).strftime("%d/%m/%Y")}. Canvia la data i tot el quadre es recalcula.')
    left,right=st.columns([1.25,2.25])
    with left:
        st.markdown(f'''<div class="riskpanel"><div style="font-size:10px;letter-spacing:.12em;color:#9FB8CF;font-weight:800">SEMAFOR EXECUTIU · +30 DIES</div><div class="lights"><div class="light {'on' if riskword=='CONTROLAT' else ''}" style="background:#22C55E;color:#22C55E"></div><div class="light {'on' if riskword=='MODERAT' else ''}" style="background:#F59E0B;color:#F59E0B"></div><div class="light {'on' if riskword=='ALT' else ''}" style="background:#EF4444;color:#EF4444"></div></div><div class="risk-big" style="color:{riskcolor}">RISC {riskword} · {maxrisk}/100</div><div class="risk-caption">Score explicable calculat a partir de desviació de calendari, lliurables vençuts, riscos oberts, evidències pendents, dependències i proximitat de fites. No és una probabilitat.</div></div>''',unsafe_allow_html=True)
        if st.button('Obrir Radar de riscos →',use_container_width=True): st.session_state.nav='Radar de riscos'; st.rerun()
    with right:
        cols=st.columns(3)
        with cols[0]: kpi('Progrés real',f'{real:.0%}',f'Planificat {planned:.0%}')
        with cols[1]: kpi('Desviació temporal',f'{(real-planned)*100:+.0f} pp','Real vs planificat')
        with cols[2]: kpi('Execució pressupostària',f'{ex.Amount.sum()/pd.to_numeric(w.Budget).sum():.0%}' if pd.to_numeric(w.Budget).sum() else '—',f'{money(ex.Amount.sum())} executats')
        cols=st.columns(3)
        due=int(ms.Due_asof.sum()); on=int(ms.On_time_asof.sum())
        with cols[0]: kpi('Fites en termini',f'{on}/{due}' if due else '—','Fins a la data d’anàlisi')
        with cols[1]: kpi('Lliurables vençuts',int(dl.Overdue.sum()),'Pendents després del venciment')
        with cols[2]: kpi('Evidències pendents',int((ex.Evidence_complete==0).sum()),'Despeses sense evidència completa')
    st.markdown('<div class="callout"><b>Lectura temporal:</b> NEÀPOLIS IMPACT no rep un percentatge de progrés manual. El calcula a partir dels lliurables ponderats i les seves dates previstes/reals. La data d’anàlisi permet reconstruir la fotografia del projecte en qualsevol moment.</div>',unsafe_allow_html=True)
    section('Trajectòria del projecte','Progrés planificat vs progrés real calculat des dels lliurables.')
    # monthly reconstruction
    p=projects[projects.Project_ID==pid].iloc[0]; start=pd.to_datetime(p.Start_date).date(); end=min(pd.Timestamp(as_of).date(),pd.to_datetime(p.End_date).date()); dates=pd.date_range(start,end,freq='MS').tolist()+[pd.Timestamp(as_of)]; dates=sorted(set(dates))
    hist=[]
    for dt in dates:
        dd=derive(raw,dt.date())['wps']; dd=dd[dd.Project_ID==pid]; hist.append([dt,100*dd.Planned_progress.mean(),100*dd.Real_progress.mean()])
    h=pd.DataFrame(hist,columns=['Data','Planificat','Real']); fig=go.Figure(); fig.add_trace(go.Scatter(x=h.Data,y=h.Planificat,name='Planificat',mode='lines+markers')); fig.add_trace(go.Scatter(x=h.Data,y=h.Real,name='Real',mode='lines+markers')); fig.update_layout(height=330,margin=dict(l=10,r=10,t=15,b=10),yaxis_title='Progrés %',legend_orientation='h'); st.plotly_chart(fig,use_container_width=True)
    section('Accés ràpid','Obre les vistes de treball sense perdre la fotografia temporal seleccionada.')
    items=[('Seguiment del projecte','Calendari, WP, lliurables, fites i tasques.'),('Activitat i lliurables','Outputs acumulats fins a la data seleccionada.'),('Resultats en startups','Última mesura disponible per startup.'),('Impacte','Canvis de major abast i evidència.'),('Retorn territorial','Valor vinculat al territori.'),('Radar de riscos','Semàfor, causes i accions correctores.'),('Data Hub','Carrega Excel/CSV o enganxa dades font.'),('Metodologia','Regles de càlcul, governança i traçabilitat.')]
    for row in [items[:4],items[4:]]:
        cc=st.columns(len(row))
        for col,(title,copy) in zip(cc,row):
            with col:
                st.markdown(f'<div class="menu-card"><div class="menu-title">{title}</div><div class="menu-copy">{copy}</div></div>',unsafe_allow_html=True)
                if st.button('Obrir →',key='home_'+title,use_container_width=True): st.session_state.nav=title; st.rerun()

elif st.session_state.nav=='Seguiment del projecte':
    section('Seguiment del projecte','PROJECT → WP → LLIURABLE / FITA / TASCA. El progrés es calcula, no s’introdueix.')
    view=w[['WP','Name','Owner','Planned_progress','Real_progress','Schedule_gap','Overdue_deliverables','Spent','Budget','Docs_pending','Open_risks','Risk_score']].copy(); view['Planned_progress']*=100; view['Real_progress']*=100; view['Schedule_gap']*=100
    st.dataframe(view,use_container_width=True,hide_index=True,height=320)
    wp=st.selectbox('Work Package',w.WP.tolist()); ww=w[w.WP==wp].iloc[0]
    a,b,c,d=st.columns(4)
    with a:kpi('Planificat',f'{ww.Planned_progress:.0%}')
    with b:kpi('Real',f'{ww.Real_progress:.0%}')
    with c:kpi('Desviació',f'{(ww.Real_progress-ww.Planned_progress)*100:+.0f} pp')
    with d:kpi('Risc',f'{ww.Risk_score}/100',ww.Risk_status)
    tab1,tab2,tab3=st.tabs(['Lliurables','Fites','Tasques'])
    with tab1: st.dataframe(dl[dl.WP==wp][['Deliverable_ID','Deliverable','Due_date','Actual_date','Weight','Owner','Planned_done','Real_done','Overdue','Delay_days']],use_container_width=True,hide_index=True)
    with tab2: st.dataframe(ms[ms.WP==wp][['Milestone_ID','Milestone','Due_date','Actual_date','Owner','Due_asof','On_time_asof']],use_container_width=True,hide_index=True)
    with tab3: st.dataframe(tasks[tasks.WP==wp][['Task_ID','Task','Owner','Start_date','Due_date','Actual_date','Dependency_ID','Overdue']],use_container_width=True,hide_index=True)

elif st.session_state.nav=='Activitat i lliurables':
    section('Activitat i outputs','Només es comptabilitzen registres amb data igual o anterior a la fotografia seleccionada.')
    act=D['activity']; act=act[act.Project_ID==pid]; summary=act.groupby('Metric',as_index=False).Value.sum(); st.dataframe(summary,use_container_width=True,hide_index=True)
    if len(summary): st.plotly_chart(px.bar(summary,x='Metric',y='Value',title='Outputs acumulats'),use_container_width=True)

elif st.session_state.nav=='Resultats en startups':
    section('Resultats en startups','Per cada startup s’utilitza l’última mesura disponible fins a la data d’anàlisi.')
    if len(latest):
        a,b,c,d=st.columns(4)
        with a:kpi('Startups amb dades',len(latest))
        with b:kpi('Ocupació',int(latest.Jobs.sum()),'FTE última mesura')
        with c:kpi('Inversió',money(latest.Investment.sum()))
        with d:kpi('Models validats',f'{latest.Validated_model.mean():.0%}')
        st.dataframe(latest,use_container_width=True,hide_index=True,height=430)
    else: st.info('No hi ha mesures disponibles fins a aquesta data.')

elif st.session_state.nav=='Impacte':
    section('Impacte','Canvi observat amb prudència metodològica: RESULTAT OBSERVAT ≠ IMPACTE ATRIBUÏBLE.')
    hist=D['startup_history']; hist=hist[hist.Project_ID==pid]
    if len(hist):
        t0=hist[hist.Phase=='T0'].groupby('Startup').first(); lt=hist.sort_values('Measurement_date').groupby('Startup').last(); common=t0.index.intersection(lt.index); jobs_add=(lt.loc[common,'Jobs']-t0.loc[common,'Jobs']).sum(); rev0=t0.loc[common,'Revenue'].sum(); rev=lt.loc[common,'Revenue'].sum(); growth=(rev/rev0-1) if rev0 else np.nan
        a,b,c=st.columns(3)
        with a:kpi('Ocupació addicional',f'+{int(jobs_add)} FTE','T0 → última mesura')
        with b:kpi('Creixement facturació',f'{growth:+.0%}' if pd.notna(growth) else '—')
        with c:kpi('Inversió mobilitzada',money(lt.Investment.sum()))
        st.markdown('<div class="callout"><b>Nota:</b> aquests són canvis observats. L’atribució causal requereix un disseny d’avaluació específic o, si no és viable, anàlisi de contribució.</div>',unsafe_allow_html=True)

elif st.session_state.nav=='Retorn territorial':
    section('Retorn territorial','Indicadors de valor territorial disponibles fins a la data seleccionada.')
    if len(latest):
        a,b,c=st.columns(3)
        with a:kpi('Nous llocs locals',int(latest.Local_jobs_created.sum()))
        with b:kpi('Pilots locals',int(latest.Local_pilot.sum()))
        with c:kpi('Retorn verificable',f'{latest.Verified_return.mean():.0%}')
        st.dataframe(latest[['Startup','Measurement_date','Local_jobs_created','Local_pilot','Verified_return']],use_container_width=True,hide_index=True)

elif st.session_state.nav=='Radar de riscos':
    section('Radar de riscos','De la desviació detectada a una decisió concreta.')
    st.markdown(f'''<div class="riskpanel"><div style="font-size:10px;letter-spacing:.12em;color:#9FB8CF;font-weight:800">SEMAFOR · FOTO {pd.Timestamp(as_of).strftime('%d/%m/%Y')}</div><div class="lights"><div class="light {'on' if riskword=='CONTROLAT' else ''}" style="background:#22C55E;color:#22C55E"></div><div class="light {'on' if riskword=='MODERAT' else ''}" style="background:#F59E0B;color:#F59E0B"></div><div class="light {'on' if riskword=='ALT' else ''}" style="background:#EF4444;color:#EF4444"></div></div><div class="risk-big" style="color:{riskcolor}">RISC {riskword} · {maxrisk}/100</div><div class="risk-caption">Priorització explicable. El score no és una probabilitat.</div></div>''',unsafe_allow_html=True)
    rw=w.sort_values('Risk_score',ascending=False); st.dataframe(rw[['WP','Name','Real_progress','Planned_progress','Overdue_deliverables','Open_risks','Docs_pending','Dependencies','Next_due_days','Risk_score','Risk_status']],use_container_width=True,hide_index=True)
    wp=st.selectbox('Analitzar WP',rw.WP.tolist()); r=rw[rw.WP==wp].iloc[0]
    factors=pd.DataFrame({'Factor':['Desviació calendari','Riscos oberts','Evidències pendents','Dependències','Proximitat venciment'],'Punts':[38*min(r.Schedule_gap/.20,1),24*min(r.Open_risks/3,1),18*min(r.Docs_pending/5,1),10*min(r.Dependencies/2,1),10*max(0,min((30-r.Next_due_days)/30,1))]})
    st.plotly_chart(px.bar(factors,x='Punts',y='Factor',orientation='h',title=f'Què explica el risc de {wp}?'),use_container_width=True)
    openrisk=risks[(risks.WP==wp)&(risks.Open_asof==1)][['Risk_ID','Risk','Probability','Impact','Owner','Mitigation']]; st.dataframe(openrisk,use_container_width=True,hide_index=True)

elif st.session_state.nav=='Data Hub':
    section('Data Hub','El sistema rep dades font. Progrés, desviacions, semàfors i KPI derivats es calculen dins del dashboard.')
    t1,t2,t3=st.tabs(['Pujar Excel / CSV','Copiar i enganxar','Explorar dades font'])
    with t1:
        st.download_button('Descarregar plantilla Excel',excel_bytes(make_demo()),file_name='NEAPOLIS_IMPACT_plantilla_V6.xlsx',mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        up=st.file_uploader('Puja un Excel amb les fulles de la plantilla o un CSV d’una taula',type=['xlsx','xlsm','csv'])
        if up:
            if up.name.lower().endswith(('.xlsx','.xlsm')):
                xls=pd.ExcelFile(up); new={}
                for sh in xls.sheet_names:
                    df=pd.read_excel(xls,sheet_name=sh); missing=validate(sh,df)
                    if sh in REQUIRED and not missing:new[sh]=df
                    elif sh in REQUIRED:st.error(f'{sh}: falten columnes {missing}')
                if set(REQUIRED).issubset(new):
                    if st.button('Aplicar Excel complet'): st.session_state.raw=new; st.session_state.mode='DADES CARREGADES'; st.rerun()
                else: st.warning('Per substituir el model complet, l’Excel ha de contenir totes les fulles requerides.')
            else: st.info('Per CSV utilitza “Copiar i enganxar” o selecciona una taula i mantén exactament les columnes de la plantilla.')
    with t2:
        table=st.selectbox('Taula a substituir',list(REQUIRED.keys())); txt=st.text_area('Enganxa aquí les files copiades des d’Excel/Sheets',height=180)
        if txt.strip():
            try:
                df=parse_paste(txt); st.dataframe(df.head(20),use_container_width=True); miss=validate(table,df)
                if miss: st.error(f'Falten columnes: {miss}')
                elif st.button('Aplicar taula enganxada'):
                    st.session_state.raw[table]=df; st.session_state.mode='DADES CARREGADES'; st.rerun()
            except Exception as e: st.error(f'No s’ha pogut interpretar la taula: {e}')
    with t3:
        table=st.selectbox('Explora taula font',list(raw.keys()),key='explore'); st.dataframe(raw[table],use_container_width=True,hide_index=True,height=430); st.download_button('Descarregar model font complet',excel_bytes(raw),file_name='NEAPOLIS_IMPACT_dades_font.xlsx',mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        with st.expander('Veure què calcula el dashboard'):
            st.write('**No s’introdueixen manualment:** Planned_progress, Real_progress, Schedule_gap, Overdue_deliverables, Spent, Docs_pending, Open_risks, Dependencies, Risk_score, Risk_status, KPI agregats i fotografia temporal.')

else:
    section('Metodologia','Arquitectura temporal, càlculs i governança.')
    st.markdown('''<div class="method"><b>DADES FONT</b> → Projectes · WP · lliurables · fites · tasques · despeses · riscos · startups · mesures · activitats<br><br><b>DATA D’ANÀLISI</b> → Avui o qualsevol data històrica seleccionada<br><br><b>MOTOR DE CÀLCUL</b> → progrés planificat + progrés real + desviació + pressupost + evidències + riscos + dependències + KPI<br><br><b>EARLY WARNING</b> → score explicable 0–100 → semàfor → responsable → mitigació<br><br><b>IMPACTE</b> → resultat observat ≠ impacte atribuïble. La causalitat requereix disseny d’avaluació.</div>''',unsafe_allow_html=True)
    st.markdown('**Progrés planificat:** suma dels pesos dels lliurables amb data prevista ≤ data d’anàlisi / pes total del WP.')
    st.markdown('**Progrés real:** suma dels pesos dels lliurables completats realment ≤ data d’anàlisi / pes total del WP.')
    st.markdown('**Desviació temporal:** progrés real − progrés planificat. Un valor negatiu indica retard respecte la trajectòria.')
