import io, csv
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title='NEÀPOLIS IMPACT', page_icon='◆', layout='wide', initial_sidebar_state='expanded')

st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:Inter,sans-serif}.block-container{max-width:1580px;padding-top:1.1rem;padding-bottom:2rem}
[data-testid="stAppViewContainer"]{background:#F5F7FA}[data-testid="stSidebar"]{background:#081321;border-right:1px solid #17283D}[data-testid="stSidebar"] *{color:#EAF0F7}
#MainMenu,footer,header{visibility:hidden}.hero{background:linear-gradient(120deg,#071426,#102A43 62%,#164E63);border-radius:22px;padding:30px 34px;color:white;box-shadow:0 16px 42px rgba(15,23,42,.13);margin-bottom:18px;position:relative;overflow:hidden}.hero:after{content:"";position:absolute;width:320px;height:320px;border-radius:50%;right:-100px;top:-160px;background:rgba(255,255,255,.045)}
.badge{display:inline-block;padding:6px 10px;border-radius:999px;background:#FFF1C9;color:#8A4A06;font-size:10px;font-weight:800;letter-spacing:.06em}.eyebrow{font-size:10px;letter-spacing:.19em;text-transform:uppercase;font-weight:800;color:#A7BCD3;margin-top:14px}.hero h1{font-size:38px;letter-spacing:-.045em;margin:7px 0 9px}.hero p{font-size:14px;color:#D3DEEA;max-width:1000px;margin:0;line-height:1.55}
.kpi{background:white;border:1px solid #DFE7EF;border-radius:17px;padding:15px 16px;min-height:112px;box-shadow:0 5px 18px rgba(15,23,42,.045)}.klabel{font-size:9.5px;font-weight:800;letter-spacing:.08em;color:#69778B;text-transform:uppercase}.kvalue{font-size:27px;font-weight:800;color:#0F172A;letter-spacing:-.045em;margin-top:8px}.ksub{font-size:10.5px;color:#758398;margin-top:4px}.section{font-size:20px;font-weight:800;letter-spacing:-.025em;color:#101827;margin:17px 0 3px}.sub{font-size:11.5px;color:#6B778A;margin-bottom:12px}
.menu-card{background:white;border:1px solid #DFE7EF;border-radius:17px;padding:17px;min-height:112px;box-shadow:0 4px 15px rgba(15,23,42,.035)}.menu-num{font-size:10px;font-weight:800;color:#0E7490;letter-spacing:.08em}.menu-title{font-size:15px;font-weight:800;color:#111827;margin:5px 0}.menu-copy{font-size:11px;color:#66758A;line-height:1.45}.accent-card{background:#0B1B2F;border:1px solid #183653;color:white;border-radius:18px;padding:18px;min-height:125px}.accent-card .menu-num{color:#67E8F9}.accent-card .menu-title{color:white}.accent-card .menu-copy{color:#BDD0E4}
.callout{background:#ECF5FF;border:1px solid #D3E8FF;color:#1E4F86;border-radius:14px;padding:13px 16px;font-size:12px;margin:9px 0 14px}.method{background:#0D1B2D;color:#D8E5F3;border-radius:17px;padding:18px 20px;font-size:11.5px;line-height:1.7}.method b{color:white}.traffic{background:white;border:1px solid #DFE7EF;border-radius:20px;padding:20px;text-align:center;box-shadow:0 8px 28px rgba(15,23,42,.06)}.dot{width:96px;height:96px;border-radius:50%;margin:8px auto 13px;box-shadow:0 0 0 10px #F1F5F9}.risk-score{font-size:44px;font-weight:800;letter-spacing:-.06em;color:#0F172A}.risk-word{font-size:13px;font-weight:800;letter-spacing:.12em}.info-box{background:white;border:1px solid #DFE7EF;border-radius:15px;padding:13px 15px;font-size:11px;color:#59677A}.group-title{font-size:11px;font-weight:800;letter-spacing:.11em;color:#64748B;text-transform:uppercase;margin:19px 0 8px}
div[data-testid="stDataFrame"]{background:white;border:1px solid #DFE7EF;border-radius:14px;padding:4px}[data-testid="stFileUploader"]{background:white;border:1px dashed #A9B8C8;border-radius:14px;padding:7px}.stExpander{background:white;border-radius:12px}
</style>''', unsafe_allow_html=True)

# ---------- RAW DEMO DATA: only source variables; no precomputed risk/status/KPI columns ----------
@st.cache_data
def make_demo():
    rng=np.random.default_rng(42)
    projects=pd.DataFrame([
        ['P01','Campus Europeu d’Emprenedoria Disruptiva',500000,'2026-01-15','2027-12-31','En execució'],
        ['P02','Urban Innovation Lab',320000,'2026-03-01','2027-08-31','En execució'],
        ['P03','Digital Talent VNG',260000,'2025-09-01','2026-12-31','En execució']
    ],columns=['Project_ID','Project','Budget','Start_date','End_date','Status'])
    wp_rows=[]
    wp_defs=[('WP1','Gestió i governança',.82,.80,60000,46800,1,4,0,18),('WP2','Selecció i baseline',1,1,45000,43200,0,0,0,90),('WP3','Acceleració',.76,.80,105000,75600,1,5,1,24),('WP4','Experimentació',.61,.78,115000,65550,3,7,2,12),('WP5','Mercat i internacionalització',.68,.70,75000,48000,1,2,1,35),('WP6','Impacte i retorn',.55,.60,65000,31200,2,4,1,28),('WP7','Comunicació i transferència',.58,.62,35000,18850,0,1,0,44)]
    for row in wp_defs: wp_rows.append(['P01',*row])
    for pid,scale in [('P02',.88),('P03',.94)]:
        for wp_id,name,prog,plan,bud,spent,risks,docs,deps,days in wp_defs[:5]:
            wp_rows.append([pid,wp_id,name,min(1,prog*scale+0.08),min(1,plan*scale+0.06),int(bud*.62),int(spent*.58),max(0,risks-1),max(0,docs-2),max(0,deps-1),days+18])
    wps=pd.DataFrame(wp_rows,columns=['Project_ID','WP','Name','Progress','Planned','Budget','Spent','Open_risks','Docs_pending','Dependencies','Days_to_next'])
    tasks=[]; tid=1
    for _,r in wps.iterrows():
        for j in range(1,6):
            planned=float(np.clip(r.Planned+rng.uniform(-.06,.05),0,1)); actual=float(np.clip(r.Progress+rng.uniform(-.10,.08),0,1))
            tasks.append([r.Project_ID,f'T-{tid:03d}',r.WP,f'Tasca {r.WP}.{j}',rng.choice(['PMO','WP Lead','Finance','Impact Lead','Partner']),planned,actual,rng.choice(['En curs','En curs','Completada','Pendent']),int(rng.integers(3,70))])
            tid+=1
    tasks=pd.DataFrame(tasks,columns=['Project_ID','Task_ID','WP','Task','Owner','Planned','Actual','Status','Days_to_deadline'])
    milestones=[]
    for _,r in wps.iterrows():
        n=4 if r.WP!='WP4' else 6
        for j in range(n): milestones.append([r.Project_ID,r.WP,f'M-{r.WP}-{j+1}',1 if j < round(n*float(r.Progress)) else 0,1 if (j < round(n*float(r.Progress)) and not(r.Project_ID=='P01' and r.WP in ['WP3','WP4'] and j==1)) else 0])
    milestones=pd.DataFrame(milestones,columns=['Project_ID','WP','Milestone_ID','Completed','On_time'])
    expenses=[]
    for _,r in wps.iterrows():
        for j in range(8): expenses.append([r.Project_ID,r.WP,f'E-{r.WP}-{j+1}',int(rng.integers(700,8000)),1 if not(r.Project_ID=='P01' and r.WP in ['WP1','WP3','WP4'] and j<2) else 0])
    expenses=pd.DataFrame(expenses,columns=['Project_ID','WP','Expense_ID','Amount','Evidence_complete'])
    names=[f'Nexa {i:02d}' for i in range(1,21)]; sectors=['AI & Data','Blue Economy','HealthTech','ClimateTech','CreativeTech','Smart City']
    startups=[]; metrics=[]
    jobs0=[3,4,2,5,4,3,2,4,3,5,2,4,3,4,2,3,4,3,3,3]; adds=[1,1,1,2,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1]
    invest=[150000,0,100000,250000,0,100000,50000,0,150000,0,100000,0,100000,0,50000,0,50000,0,0,0]
    clients=[5,4,3,5,4,3,4,2,5,4,4,3,4,3,3,2,3,2,2,2]
    for i,n in enumerate(names):
        startups.append(['P01',n,sectors[i%len(sectors)],['MVP','Early traction','Growth'][i%3],1 if i<19 else 0])
        rev0=int(rng.integers(55,190))*1000; growth=float(np.clip(rng.normal(.21,.08),.03,.42))
        metrics.append(['P01',n,jobs0[i],jobs0[i]+adds[i],rev0,int(rev0*(1+growth)),invest[i],clients[i],1 if i<10 else 0,1 if i<3 else 0,1 if i<14 else 0,1 if i<8 else 0,1 if i<7 else 0,1 if i<7 else 0,1 if i<11 else 0,1 if i<8 else 0,1 if i<3 else 0,[9000,7000,11000,6000,8500,5000,7500,4500,9500,6500,7000,5500,8000,4000,6500,5000,4500,3500,3000,3500][i],1 if i<12 else 0,1 if i<9 else 0,1 if i<13 else 0,1 if i<11 else 0,1 if i<12 else 0,1 if i<14 else 0])
    startups=pd.DataFrame(startups,columns=['Project_ID','Startup','Sector','Stage','Active'])
    startup_metrics=pd.DataFrame(metrics,columns=['Project_ID','Startup','Jobs_T0','Jobs_T3','Revenue_T0','Revenue_T3','Investment','New_clients','Pilot','Pilot_contract','Validated_model','New_market','International','Raised_investment','Local_jobs','Local_pilot','Local_adoption','Local_supplier_spend','Local_contract','Research_collab','Knowledge_action','Persistent_alliance','Rooted','Verified_return'])
    activity=pd.DataFrame([
        ['P01','Mentoring_hours',315],['P01','Workshops',16],['P01','Workshop_attendance_pct',88],['P01','T0_diagnostics',20],['P01','Pilots_started',10],['P01','Pilots_completed',6],['P01','Startup_company_connections',48],['P01','Investor_meetings',31],['P01','Scalability_plans',17],['P01','European_connections',22],
        ['P02','Mentoring_hours',190],['P02','Workshops',11],['P03','Mentoring_hours',220],['P03','Workshops',14]
    ],columns=['Project_ID','Metric','Value'])
    return {'Projects':projects,'Work_Packages':wps,'Tasks':tasks,'Milestones':milestones,'Expenses':expenses,'Startups':startups,'Startup_Metrics':startup_metrics,'Activity':activity}

REQUIRED={
'Projects':['Project_ID','Project','Budget','Start_date','End_date','Status'],
'Work_Packages':['Project_ID','WP','Name','Progress','Planned','Budget','Spent','Open_risks','Docs_pending','Dependencies','Days_to_next'],
'Tasks':['Project_ID','Task_ID','WP','Task','Owner','Planned','Actual','Status','Days_to_deadline'],
'Milestones':['Project_ID','WP','Milestone_ID','Completed','On_time'],
'Expenses':['Project_ID','WP','Expense_ID','Amount','Evidence_complete'],
'Startups':['Project_ID','Startup','Sector','Stage','Active'],
'Startup_Metrics':['Project_ID','Startup','Jobs_T0','Jobs_T3','Revenue_T0','Revenue_T3','Investment','New_clients','Pilot','Pilot_contract','Validated_model','New_market','International','Raised_investment','Local_jobs','Local_pilot','Local_adoption','Local_supplier_spend','Local_contract','Research_collab','Knowledge_action','Persistent_alliance','Rooted','Verified_return'],
'Activity':['Project_ID','Metric','Value']}

if 'raw' not in st.session_state:
    st.session_state.raw=make_demo(); st.session_state.mode='DEMO · DADES FICTÍCIES'

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
def kpi(label,value,sub=''):
    st.markdown(f'<div class="kpi"><div class="klabel">{label}</div><div class="kvalue">{value}</div><div class="ksub">{sub}</div></div>',unsafe_allow_html=True)
def section(title,sub=''):
    st.markdown(f'<div class="section">{title}</div><div class="sub">{sub}</div>',unsafe_allow_html=True)
def menu_card(num,title,copy,accent=False):
    cls='accent-card' if accent else 'menu-card'; st.markdown(f'<div class="{cls}"><div class="menu-num">{num}</div><div class="menu-title">{title}</div><div class="menu-copy">{copy}</div></div>',unsafe_allow_html=True)
def info_metric(title,text):
    with st.expander(f'ⓘ {title}'): st.caption(text)

def derive(raw):
    d={k:v.copy() for k,v in raw.items()}
    w=d['Work_Packages'].copy()
    for c in ['Progress','Planned','Budget','Spent','Open_risks','Docs_pending','Dependencies','Days_to_next']: w[c]=pd.to_numeric(w[c],errors='coerce').fillna(0)
    w['Schedule_gap']=(w.Planned-w.Progress).clip(lower=0); w['Budget_execution']=w.Spent/w.Budget.replace(0,np.nan)
    w['Risk_score']=(38*(w.Schedule_gap/.20).clip(0,1)+24*(w.Open_risks/3).clip(0,1)+18*(w.Docs_pending/7).clip(0,1)+10*(w.Dependencies/2).clip(0,1)+10*((30-w.Days_to_next)/30).clip(0,1)).fillna(0).round().astype(int)
    # forecast derived only from current raw drivers: deterioration if gap/risks/docs remain open
    pressure=(12*(w.Schedule_gap/.20).clip(0,1)+5*(w.Open_risks>0).astype(int)+4*(w.Docs_pending>0).astype(int)+3*(w.Dependencies>0).astype(int)-4*(w.Progress>=w.Planned).astype(int))
    w['Risk_30d']=(w.Risk_score+pressure).clip(0,100).round().astype(int)
    w['Risk_status']=np.select([w.Risk_30d>=70,w.Risk_30d>=40],['VERMELL','TARONJA'],default='VERD')
    d['WP_Derived']=w
    sm=d['Startup_Metrics'].copy(); sm['Revenue_growth']=sm.Revenue_T3/sm.Revenue_T0.replace(0,np.nan)-1; sm['Jobs_added']=sm.Jobs_T3-sm.Jobs_T0; d['Startup_Derived']=sm.merge(d['Startups'],on=['Project_ID','Startup'],how='left')
    return d

D=derive(st.session_state.raw); projects=D['Projects']

# ---------- SIDEBAR: persistent navigation + global filters ----------
st.sidebar.markdown('## NEÀPOLIS IMPACT'); st.sidebar.caption('Project & Impact Intelligence System'); st.sidebar.markdown(f'**{st.session_state.mode}**'); st.sidebar.divider()
page=st.sidebar.radio('MENÚ PRINCIPAL',['HOME','Seguiment del projecte','Activitat i lliurables','Resultats en startups','Impacte','Retorn territorial','Radar de riscos','Data Hub','Metodologia'],key='nav')
st.sidebar.divider(); st.sidebar.markdown('**Configuració de dades**')
proj_options=['PORTFOLI · Tots els projectes']+projects['Project'].tolist(); selected_project=st.sidebar.selectbox('Projecte',proj_options)
time_sel=st.sidebar.selectbox('Període',['T3 · +12 mesos','T2 · +6 mesos','T1 · final programa','T0 · baseline'])
all_startups=D['Startups']['Startup'].tolist(); startup_sel=st.sidebar.selectbox('Startup',['Totes']+all_startups)
sector_sel=st.sidebar.selectbox('Sector',['Tots']+sorted(D['Startups']['Sector'].unique().tolist()))
if st.sidebar.button('↺ Restaurar dades fictícies',use_container_width=True): st.session_state.raw=make_demo(); st.session_state.mode='DEMO · DADES FICTÍCIES'; st.rerun()

if selected_project.startswith('PORTFOLI'): pids=projects.Project_ID.tolist()
else: pids=projects.loc[projects.Project==selected_project,'Project_ID'].tolist()
wp=D['WP_Derived'][D['WP_Derived'].Project_ID.isin(pids)].copy(); tasks=D['Tasks'][D['Tasks'].Project_ID.isin(pids)].copy(); milestones=D['Milestones'][D['Milestones'].Project_ID.isin(pids)].copy(); expenses=D['Expenses'][D['Expenses'].Project_ID.isin(pids)].copy(); activity=D['Activity'][D['Activity'].Project_ID.isin(pids)].copy(); sd=D['Startup_Derived'][D['Startup_Derived'].Project_ID.isin(pids)].copy()
if startup_sel!='Totes': sd=sd[sd.Startup==startup_sel]
if sector_sel!='Tots': sd=sd[sd.Sector==sector_sel]

st.markdown(f'''<div class="hero"><span class="badge">{st.session_state.mode}</span><div class="eyebrow">Project & Impact Intelligence System</div><h1>NEÀPOLIS IMPACT</h1><p>Intel·ligència de gestió per anticipar desviacions, seguir resultats i convertir l'execució dels projectes europeus en impacte i retorn territorial mesurable.</p></div>''',unsafe_allow_html=True)

# ---------- shared calculations ----------
progress=float(wp.Progress.mean()) if len(wp) else 0; budget=float(wp.Spent.sum()/wp.Budget.sum()) if len(wp) and wp.Budget.sum() else 0
m_on=int(milestones.On_time.sum()) if len(milestones) else 0; m_total=len(milestones); docs_pending=int((expenses.Evidence_complete==0).sum()) if len(expenses) else 0
riskmax=int(wp.Risk_30d.max()) if len(wp) else 0; active=int(sd.Active.sum()) if len(sd) else 0; inv=float(sd.Investment.sum()) if len(sd) else 0

def status_color(score): return '#DC2626' if score>=70 else '#F59E0B' if score>=40 else '#16A34A'
def status_word(score): return 'ALT' if score>=70 else 'MODERAT' if score>=40 else 'CONTROLAT'

if page=='HOME':
    section('Visió de direcció','Els indicadors que permeten saber, en pocs segons, què està passant i on cal intervenir.')
    c=st.columns(7)
    vals=[('Salut del projecte',f'{progress:.0%}','Execució mitjana'),('Execució pressupostària',f'{budget:.0%}',f'{money(wp.Spent.sum())} / {money(wp.Budget.sum())}'),('Fites en termini',f'{m_on}/{m_total}','Puntualitat'),('Risc a 30 dies',f'{riskmax}/100',status_word(riskmax)),('Evidències pendents',str(docs_pending),'Despeses sense evidència'),('Startups actives',str(active),'Segons filtres'),('Inversió mobilitzada',money(inv),'Startups filtrades')]
    for col,v in zip(c,vals):
        with col:kpi(*v)
    e=st.columns(4)
    with e[0]: info_metric('Salut del projecte','Mitjana del progrés declarat dels Work Packages inclosos al filtre. Serveix com a lectura executiva; el detall es consulta a Seguiment del projecte.')
    with e[1]: info_metric('Risc a 30 dies','Score 0–100 calculat pel dashboard a partir de desviació temporal, riscos oberts, documentació pendent, dependències i proximitat de fites. No és una probabilitat.')
    with e[2]: info_metric('Evidències pendents','Nombre de registres de despesa que encara no tenen l’evidència documental marcada com a completa.')
    with e[3]: info_metric('Inversió mobilitzada','Suma de la inversió registrada per les startups seleccionades. És un outcome observat i no s’interpreta automàticament com a impacte atribuïble.')
    st.markdown('<div class="callout"><b>Lectura de direcció:</b> la HOME combina execució, risc, evidència, resultats empresarials i retorn. Els filtres del menú lateral recalculen la vista sobre els projectes i startups seleccionats.</div>',unsafe_allow_html=True)
    section('Mapa del sistema','Una navegació simple: de l’execució als resultats, i dels resultats a l’impacte i la decisió.')
    st.markdown('<div class="group-title">GESTIÓ I RESULTATS</div>',unsafe_allow_html=True)
    cols=st.columns(4)
    items=[('01','Seguiment del projecte','Calendari, pressupost, tasques, fites, documentació i responsabilitats.'),('02','Activitat i lliurables','Què ha produït directament la intervenció: mentoria, tallers, pilots i connexions.'),('03','Resultats en startups','Què ha canviat: clients, pilots, facturació, ocupació, inversió i mercats.'),('04','Lectura executiva','Visió integrada dels indicadors clau per facilitar decisions de direcció.')]
    for col,it in zip(cols,items):
        with col: menu_card(*it)
    with st.expander('ⓘ Què inclouen aquests quatre blocs?'): st.write('**Seguiment** controla l’execució. **Activitat i lliurables** mostra outputs. **Resultats en startups** mostra outcomes. La **lectura executiva** integra els senyals essencials per a direcció sense confondre activitat amb impacte.')
    st.markdown('<div class="group-title">VALOR PÚBLIC I TERRITORIAL</div>',unsafe_allow_html=True)
    cols=st.columns(2)
    with cols[0]: menu_card('05','Impacte','Canvis de major abast, contribució plausible, persistència i factors externs.',True)
    with cols[1]: menu_card('06','Retorn territorial','Economia, ocupació i talent, innovació i coneixement, i ecosistema.',True)
    with st.expander('ⓘ Diferència entre impacte i retorn territorial'): st.write('**Impacte** pregunta quin canvi de major abast observem i fins a quin punt és plausible que el projecte hi hagi contribuït. **Retorn territorial** identifica quina part del valor generat queda vinculada al territori mitjançant evidències verificables.')
    st.markdown('<div class="group-title">ANTICIPACIÓ, DADES I GOVERNANÇA</div>',unsafe_allow_html=True)
    cols=st.columns(3)
    with cols[0]: menu_card('07','Radar de riscos','Semàfor explicable, previsió a 30 dies i factors que exigeixen acció.',True)
    with cols[1]: menu_card('08','Data Hub','Carrega Excel/CSV, enganxa taules, valida dades i exporta el model.',False)
    with cols[2]: menu_card('09','Metodologia','Teoria del Canvi, definicions, governança de dades i criteris d’avaluació.',False)
    section('Prioritats ara','Els elements que demanen atenció segons les dades seleccionades.')
    priority=wp.sort_values('Risk_30d',ascending=False)[['Project_ID','WP','Name','Progress','Planned','Open_risks','Docs_pending','Days_to_next','Risk_30d','Risk_status']].head(6)
    st.dataframe(priority,hide_index=True,use_container_width=True,height=250)

elif page=='Seguiment del projecte':
    section('Seguiment del projecte','Control operatiu de calendari, pressupost, fites, documentació, tasques i responsables.')
    st.dataframe(wp[['Project_ID','WP','Name','Progress','Planned','Budget','Spent','Budget_execution','Open_risks','Docs_pending','Dependencies','Days_to_next']],hide_index=True,use_container_width=True,height=340)
    l,r=st.columns([1.25,1])
    with l:
        p=wp[['WP','Progress','Planned']].melt('WP',var_name='Sèrie',value_name='Valor'); fig=px.bar(p,x='WP',y='Valor',color='Sèrie',barmode='group',text_auto='.0%'); fig.update_layout(height=350,yaxis_tickformat='.0%',yaxis_range=[0,1.1],legend_title='',paper_bgcolor='white',plot_bgcolor='white'); st.plotly_chart(fig,use_container_width=True)
    with r:
        section('Control documental','Les alertes es calculen a partir dels registres de despesa, no d’una variable precalculada.')
        doc=expenses.groupby(['Project_ID','WP']).agg(Despeses=('Expense_ID','count'),Evidencies_completes=('Evidence_complete','sum'),Import=('Amount','sum')).reset_index(); doc['Pendents']=doc.Despeses-doc.Evidencies_completes; st.dataframe(doc,hide_index=True,use_container_width=True,height=280)
    section('Task tracker','PROJECTE → WP → TASCA → RESPONSABLE')
    st.dataframe(tasks,hide_index=True,use_container_width=True,height=360)

elif page=='Activitat i lliurables':
    section('Activitat i lliurables','Outputs: productes directes de la intervenció. Activitat no equival a impacte.')
    pivot=activity.pivot_table(index='Metric',values='Value',aggfunc='sum').reset_index(); st.dataframe(pivot,hide_index=True,use_container_width=True,height=330)
    fig=px.bar(pivot,x='Value',y='Metric',orientation='h',text_auto=True); fig.update_layout(height=420,xaxis_title='Valor',yaxis_title='',paper_bgcolor='white',plot_bgcolor='white'); st.plotly_chart(fig,use_container_width=True)
    info_metric('Per què els outputs no són impacte?','Hores de mentoria, tallers, pilots o reunions demostren què s’ha executat. L’impacte exigeix observar canvis de major abast i analitzar la contribució del projecte.')

elif page=='Resultats en startups':
    section('Resultats en startups','Outcomes calculats directament a partir dels registres individuals de Startup_Metrics.')
    n=max(len(sd),1); cards=[('Models validats',f'{sd.Validated_model.mean():.0%}' if len(sd) else '—','% startups'),('Amb nous clients',f'{(sd.New_clients>0).mean():.0%}' if len(sd) else '—','% startups'),('Amb pilots',f'{sd.Pilot.mean():.0%}' if len(sd) else '—','% startups'),('Inversió',money(sd.Investment.sum()),'Suma registres'),('Facturació',f'{sd.Revenue_growth.mean():+.0%}' if len(sd) else '—','Creixement mitjà'),('Ocupació',f'{int(sd.Jobs_T3.sum())} FTE' if len(sd) else '—',f'{int(sd.Jobs_T0.sum())} FTE a T0' if len(sd) else '')]
    cc=st.columns(6)
    for col,v in zip(cc,cards):
        with col:kpi(*v)
    st.dataframe(sd,hide_index=True,use_container_width=True,height=390)
    if len(sd):
        traj=pd.DataFrame({'Moment':['T0','T3'],'FTE':[sd.Jobs_T0.sum(),sd.Jobs_T3.sum()]}); fig=px.line(traj,x='Moment',y='FTE',markers=True,text='FTE'); fig.update_traces(textposition='top center'); fig.update_layout(height=300,paper_bgcolor='white',plot_bgcolor='white'); st.plotly_chart(fig,use_container_width=True)

elif page=='Impacte':
    section('Impacte','Canvis de major abast observats. El dashboard calcula resultats; l’atribució exigeix disseny d’avaluació.')
    st.markdown('<div class="callout"><b>RESULTAT OBSERVAT ≠ IMPACTE ATRIBUÏBLE.</b> Els indicadors següents són evidència per a l’anàlisi de contribució, no una atribució automàtica.</div>',unsafe_allow_html=True)
    if len(sd):
        impact_df=pd.DataFrame([
            ['Ocupació addicional',int(sd.Jobs_added.sum()),'FTE T3 − FTE T0'],['Inversió mobilitzada',float(sd.Investment.sum()),'€ acumulats'],['Solucions/pilots adoptats',int(sd.Local_adoption.sum()),'Nº amb evidència'],['Col·laboracions persistents',int(sd.Persistent_alliance.sum()),'Nº >12 mesos'],['Startups internacionalitzades',float(sd.International.mean()*100),'% startups'],['Continuïtat de pilots',float(sd.Pilot_contract.sum()/max(sd.Pilot.sum(),1)*100),'% pilots amb contracte']
        ],columns=['Indicador','Valor','Mesura']); st.dataframe(impact_df,hide_index=True,use_container_width=True,height=300)
    st.markdown('<div class="method"><b>Lectura metodològica</b><br>Combinar T0–T4, evidència documental, entrevistes i factors externs. Utilitzar anàlisi de contribució; incorporar contrafactual només quan el disseny, la mostra i la qualitat de les dades ho permetin.</div>',unsafe_allow_html=True)

elif page=='Retorn territorial':
    section('Retorn territorial','Valor verificable que queda vinculat al territori en quatre dimensions.')
    if len(sd):
        terr=pd.DataFrame([
            ['Economia','Despesa amb proveïdors locals',sd.Local_supplier_spend.sum(),'€'],['Economia','Contractes startup-empresa local',sd.Local_contract.sum(),'Nº'],['Ocupació i talent','Nous llocs de treball locals',sd.Local_jobs.sum(),'FTE'],['Innovació i coneixement','Pilots realitzats al territori',sd.Local_pilot.sum(),'Nº'],['Innovació i coneixement','Pilots adoptats localment',sd.Local_adoption.sum(),'Nº'],['Innovació i coneixement','Col·laboracions universitat/recerca',sd.Research_collab.sum(),'Nº'],['Ecosistema','Aliances persistents',sd.Persistent_alliance.sum(),'Nº'],['Ecosistema','Startups arrelades',sd.Rooted.sum(),'Nº'],['Ecosistema','Startups amb retorn verificable',sd.Verified_return.mean()*100,'%']
        ],columns=['Dimensió','Indicador','Valor','Unitat']); st.dataframe(terr,hide_index=True,use_container_width=True,height=350)
        counts=terr[terr.Unitat=='Nº']; fig=px.bar(counts,x='Valor',y='Indicador',color='Dimensió',orientation='h',text_auto=True); fig.update_layout(height=360,yaxis_title='',paper_bgcolor='white',plot_bgcolor='white'); st.plotly_chart(fig,use_container_width=True)
    info_metric('Per què no hi ha un índex únic de retorn?','No es ponderen arbitràriament ocupació, pilots, despesa o aliances. Cada dimensió conserva la seva unitat i evidència, evitant una puntuació sintètica difícil de justificar.')

elif page=='Radar de riscos':
    section('Radar de riscos i alerta primerenca','Anticipar, explicar i convertir el risc en una acció gestionable.')
    score=riskmax; color=status_color(score)
    a,b=st.columns([.65,1.7])
    with a:
        st.markdown(f'<div class="traffic"><div class="dot" style="background:{color}"></div><div class="risk-score">{score}/100</div><div class="risk-word" style="color:{color}">RISC {status_word(score)}</div><div class="ksub">Horitzó predictiu · +30 dies</div></div>',unsafe_allow_html=True)
        info_metric('Què significa el score?','És un índex de priorització 0–100, no una probabilitat. Es recalcula a partir de variables operatives del dataset carregat.')
    with b:
        st.markdown('<div class="method"><b>Motor explicable</b><br>38% desviació de calendari · 24% riscos oberts · 18% documentació pendent · 10% dependències · 10% proximitat de la següent fita.<br><br><b>Semàfor:</b> 0–39 verd · 40–69 taronja · 70–100 vermell.<br><br>El forecast a 30 dies afegeix pressió quan les causes obertes persisteixen. És una regla demostrativa transparent, no un model ML entrenat.</div>',unsafe_allow_html=True)
        st.dataframe(wp[['Project_ID','WP','Name','Risk_score','Risk_30d','Risk_status','Schedule_gap','Open_risks','Docs_pending','Dependencies','Days_to_next']].sort_values('Risk_30d',ascending=False),hide_index=True,use_container_width=True,height=310)
    selected=st.selectbox('Analitza el detall de',wp.WP.unique().tolist() if len(wp) else ['—']);
    if len(wp):
        w=wp[wp.WP==selected].sort_values('Risk_30d',ascending=False).iloc[0]
        factors=pd.DataFrame({'Factor':['Desviació calendari','Riscos oberts','Documentació pendent','Dependències','Proximitat fita'],'Punts':[38*min(max(w.Schedule_gap,0)/.20,1),24*min(w.Open_risks/3,1),18*min(w.Docs_pending/7,1),10*min(w.Dependencies/2,1),10*max((30-w.Days_to_next)/30,0)]})
        fig=px.bar(factors,x='Punts',y='Factor',orientation='h',text_auto='.0f'); fig.update_layout(height=330,xaxis_title='Contribució al risc',yaxis_title='',paper_bgcolor='white',plot_bgcolor='white'); st.plotly_chart(fig,use_container_width=True)
    section('De l’alerta a l’acció','DETECCIÓ → ALERTA → RESPONSABLE → ACCIÓ CORRECTORA → TERMINI → VERIFICACIÓ')
    alert_rows=[]
    for _,r in wp[wp.Risk_30d>=40].iterrows():
        cause='Desviació temporal' if r.Schedule_gap>=.08 else 'Riscos/documentació' if r.Open_risks+r.Docs_pending>0 else 'Proximitat de fita'
        action='Pla de recuperació i revisió setmanal' if r.Risk_30d>=70 else 'Revisar dependències i actualitzar forecast'
        alert_rows.append([r.Project_ID,r.WP,r.Risk_status,int(r.Risk_30d),cause,'WP Lead',action,max(int(r.Days_to_next),0),'Pendent verificació'])
    st.dataframe(pd.DataFrame(alert_rows,columns=['Projecte','WP','Semàfor','Score','Causa principal','Responsable','Acció correctora','Dies fins fita','Verificació']),hide_index=True,use_container_width=True,height=300)

elif page=='Data Hub':
    section('Data Hub','La capa de dades és substituïble. El dashboard calcula els indicadors i scores; l’Excel aporta dades font, no conclusions precalculades.')
    st.success('✓ En aquesta versió, **Risk_score, Risk_30d, Risk_status, Revenue_growth, Jobs_added i altres KPI derivats NO formen part de la plantilla d’entrada.** Es calculen dins de NEÀPOLIS IMPACT.')
    u1,u2,u3=st.tabs(['Pujar Excel / CSV','Copiar i enganxar','Explorar dades font'])
    with u1:
        st.download_button('⬇ Descarregar plantilla de dades font',excel_bytes(make_demo()),'NEAPOLIS_IMPACT_plantilla_dades_font.xlsx','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',use_container_width=True)
        st.caption('La plantilla conté només variables d’entrada. Pots substituir les files fictícies per dades pròpies mantenint noms de fulls i columnes.')
        up=st.file_uploader('Puja un Excel (.xlsx/.xlsm) o CSV',type=['xlsx','xlsm','csv'])
        if up is not None:
            try:
                candidate={}
                if up.name.lower().endswith('.csv'):
                    target=st.selectbox('A quin dataset correspon?',list(REQUIRED.keys())); candidate[target]=pd.read_csv(up)
                else:
                    book=pd.read_excel(up,sheet_name=None); candidate={k:v for k,v in book.items() if k in REQUIRED}; st.write('Fulls reconeguts:',', '.join(candidate.keys()) if candidate else 'cap')
                problems=[]
                for name,df in candidate.items():
                    miss=validate(name,df)
                    if miss: problems.append(f'{name}: falten {", ".join(miss)}')
                if problems: st.error('No es pot aplicar encara:\n- '+'\n- '.join(problems))
                elif candidate and st.button('Aplicar dades al dashboard',type='primary'):
                    merged=st.session_state.raw.copy(); merged.update(candidate); st.session_state.raw=merged; st.session_state.mode='DADES CARREGADES · SESSIÓ'; st.rerun()
            except Exception as e: st.error(f'No s’ha pogut llegir el fitxer: {e}')
    with u2:
        target=st.selectbox('Taula de dades font',list(REQUIRED.keys()),key='paste'); st.caption('Copia des d’Excel o Google Sheets incloent la fila de capçaleres.')
        txt=st.text_area('Enganxa la taula',height=220,placeholder='Project_ID\tWP\tName\tProgress\tPlanned...')
        if txt.strip():
            try:
                parsed=parse_paste(txt); st.dataframe(parsed,hide_index=True,use_container_width=True,height=230); miss=validate(target,parsed)
                if miss: st.warning('Falten columnes: '+', '.join(miss))
                elif st.button('Aplicar taula enganxada',type='primary'):
                    merged=st.session_state.raw.copy(); merged[target]=parsed; st.session_state.raw=merged; st.session_state.mode='DADES ENGANXADES · SESSIÓ'; st.rerun()
            except Exception as e: st.error(f'No s’ha pogut interpretar: {e}')
    with u3:
        which=st.selectbox('Dataset font',list(st.session_state.raw.keys())); st.dataframe(st.session_state.raw[which],hide_index=True,use_container_width=True,height=430)
        with st.expander('Veure variables calculades pel dashboard'):
            if which=='Work_Packages': st.dataframe(D['WP_Derived'],hide_index=True,use_container_width=True,height=330)
            elif which in ['Startups','Startup_Metrics']: st.dataframe(D['Startup_Derived'],hide_index=True,use_container_width=True,height=330)
            else: st.write('Aquest dataset s’utilitza com a font directa o per agregacions; no té una taula derivada específica.')
        st.download_button('⬇ Exportar dades font en Excel',excel_bytes(st.session_state.raw),'NEAPOLIS_IMPACT_dades_font.xlsx','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',use_container_width=True)

elif page=='Metodologia':
    section('Metodologia i governança','Com es transforma una dada font en informació per decidir.')
    st.markdown('<div class="method"><b>TEORIA DEL CANVI</b> → cadena causal → <b>DADES FONT</b> → càlcul d’indicadors → <b>QUADRE DE COMANDAMENT</b> → alerta → decisió/acció correctora → avaluació → aprenentatge.<br><br><b>Separació:</b> Inputs/activitats → Outputs → Outcomes → Impactes → Retorn territorial.<br><b>Temporalitat:</b> T0 baseline · T1 final programa · T2 +6 mesos · T3 +12 mesos · T4 +24 mesos.<br><b>Governança:</b> font, data owner, periodicitat, validació, traçabilitat, minimització de dades personals i supervisió humana.</div>',unsafe_allow_html=True)
    section('Càlcul del radar de riscos','Regles transparents i auditables')
    formula=pd.DataFrame([['Desviació de calendari','Planned − Progress','38%'],['Riscos oberts','Open_risks','24%'],['Documentació pendent','Docs_pending','18%'],['Dependències','Dependencies','10%'],['Proximitat de fita','Days_to_next','10%']],columns=['Factor','Dada font','Pes màxim']); st.dataframe(formula,hide_index=True,use_container_width=True)
    st.info('La ponderació és una proposta demostrativa que s’hauria de calibrar i validar amb dades històriques reals abans d’utilitzar-se com a model predictiu operatiu.')
