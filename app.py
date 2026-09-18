import io
import csv
from datetime import datetime
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="NEÀPOLIS IMPACT", page_icon="◆", layout="wide", initial_sidebar_state="expanded")

# -------------------- Visual system --------------------
st.markdown(r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {font-family:'Inter',sans-serif;}
[data-testid="stAppViewContainer"] {background:#F4F7FA;}
[data-testid="stSidebar"] {background:#08111F; border-right:1px solid #142238;}
[data-testid="stSidebar"] * {color:#E8EEF7;}
.block-container {padding-top:1.1rem; padding-bottom:2.2rem; max-width:1580px;}
#MainMenu, footer, header {visibility:hidden;}
.hero {background:linear-gradient(120deg,#08111F 0%,#10213B 60%,#17324C 100%); padding:25px 30px; border-radius:20px; color:white; margin-bottom:15px; box-shadow:0 12px 34px rgba(8,17,31,.13);}
.hero .eyebrow {font-size:10px; letter-spacing:.18em; font-weight:800; color:#91A6C2; text-transform:uppercase;}
.hero h1 {font-size:34px; line-height:1.05; margin:7px 0 8px; letter-spacing:-.04em;}
.hero p {font-size:13px; color:#C7D3E3; margin:0; max-width:1000px;}
.demo {display:inline-block;background:#FFF4D6;color:#8A4B08;padding:6px 10px;border-radius:999px;font-size:10px;font-weight:800;letter-spacing:.06em;margin-bottom:10px;}
.kpi {background:white; border:1px solid #DFE6EE; border-radius:16px; padding:15px 17px; min-height:112px; box-shadow:0 4px 16px rgba(15,23,42,.045);}
.kpi-label {font-size:10px; color:#697586; font-weight:800; text-transform:uppercase; letter-spacing:.075em;}
.kpi-value {font-size:25px; font-weight:800; letter-spacing:-.04em; margin-top:8px; color:#0F172A;}
.kpi-sub {font-size:10.5px; color:#748094; margin-top:5px;}
.section-title {font-size:19px; font-weight:800; letter-spacing:-.025em; color:#101827; margin:10px 0 2px;}
.section-sub {font-size:11.5px; color:#6B778A; margin-bottom:11px;}
.callout {background:#EDF5FF;border:1px solid #D5E7FF;border-radius:14px;padding:13px 16px;font-size:12px;color:#1E4F86;margin:8px 0 15px;}
.method {background:#0E1A2B;color:#D9E4F2;border-radius:16px;padding:17px 19px;font-size:11.5px;line-height:1.65;}
.method b {color:white;}
.traffic-wrap {background:white;border:1px solid #DFE6EE;border-radius:20px;padding:22px;box-shadow:0 8px 28px rgba(15,23,42,.07);}
.traffic-light {width:136px;background:#0B1220;border-radius:34px;padding:15px;margin:0 auto;box-shadow:inset 0 0 0 1px #334155,0 14px 28px rgba(15,23,42,.20);}
.light {width:88px;height:88px;border-radius:50%;margin:10px auto;border:6px solid #1F2937;opacity:.14;}
.light.red {background:#EF4444}.light.amber {background:#F59E0B}.light.green {background:#22C55E}.light.on {opacity:1;box-shadow:0 0 30px rgba(255,255,255,.22)}
.risk-number {font-size:52px;font-weight:800;letter-spacing:-.06em;text-align:center;color:#0F172A;line-height:1;margin-top:18px;}
.risk-label {font-size:12px;font-weight:800;text-align:center;text-transform:uppercase;letter-spacing:.10em;margin-top:8px;}
.chip {display:inline-block;border:1px solid #D8E1EB;background:#fff;border-radius:999px;padding:5px 9px;font-size:10px;font-weight:700;color:#445267;margin:2px 3px 2px 0;}
.level {background:#fff;border:1px solid #DFE6EE;border-radius:14px;padding:12px 14px;font-size:11px;color:#475569;min-height:78px}.level b{color:#0F172A;font-size:12px}
div[data-testid="stDataFrame"] {background:white;border-radius:14px;border:1px solid #DFE6EE;padding:5px;}
.stTabs [data-baseweb="tab-list"] {gap:4px; background:#E9EEF4; padding:5px; border-radius:12px; overflow-x:auto;}
.stTabs [data-baseweb="tab"] {height:38px;border-radius:9px;padding:0 12px;font-size:11.5px;font-weight:700;white-space:nowrap;}
.stTabs [aria-selected="true"] {background:white !important; box-shadow:0 1px 5px rgba(15,23,42,.10);}
[data-testid="stFileUploader"] {background:white;border:1px dashed #AAB8C8;border-radius:14px;padding:7px;}
</style>
""", unsafe_allow_html=True)

# -------------------- Data model --------------------
@st.cache_data
def demo_data(seed=23):
    rng=np.random.default_rng(seed)
    names=[f"Nexa {i:02d}" for i in range(1,21)]
    sectors=["AI & Data","Blue Economy","HealthTech","ClimateTech","CreativeTech","Smart City"]
    rows=[]
    # Force coherent aggregate outcomes close to the project specification.
    jobs0=[3,4,2,5,4,3,2,4,3,5,2,4,3,4,2,3,4,3,3,3]  # 66
    adds =[1,1,1,2,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1]  # +17
    for i,n in enumerate(names):
        rev0=int(rng.integers(55,190))*1000
        growth=float(np.clip(rng.normal(.21,.10),-.03,.45))
        rows.append({
            "Startup":n,"Sector":rng.choice(sectors),"Stage":rng.choice(["MVP","Early traction","Growth"]),
            "Active":1 if i<19 else 0,"Jobs_T0":jobs0[i],"Jobs_T3":jobs0[i]+adds[i],
            "Revenue_T0":rev0,"Revenue_T3":int(rev0*(1+growth)),"Investment":[150000,0,100000,250000,0,100000,50000,0,150000,0,100000,0,100000,0,50000,0,50000,0,0,0][i],
            "New_clients":[5,4,3,5,4,3,4,2,5,4,4,3,4,3,3,2,3,2,2,2][i],
            "Pilots":1 if i<10 else 0,"Pilot_contract":1 if i<3 else 0,"Validated_model":1 if i<14 else 0,
            "New_market":1 if i<8 else 0,"International":1 if i<7 else 0,"Raised_investment":1 if i<7 else 0,
            "Capability_T0":int(rng.integers(53,63)),"Capability_T1":int(rng.integers(69,79)),
            "Local_jobs":1 if i<11 else 0,"Local_pilots":1 if i<8 else 0,"Local_adoption":1 if i<3 else 0,
            "Local_supplier_spend":[9000,7000,11000,6000,8500,5000,7500,4500,9500,6500,7000,5500,8000,4000,6500,5000,4500,3500,3000,3500][i],
            "Local_contract":1 if i<12 else 0,"Research_collab":1 if i<9 else 0,"Knowledge_actions":1 if i<13 else 0,
            "Alliances":2 if i==0 else (1 if i<20 else 0),"Persistent_alliance":1 if i<11 else 0,
            "Rooted":1 if i<12 else 0,"Verified_return":1 if i<14 else 0,
            "Evidence":"CRM + seguiment + evidència documental"})
    su=pd.DataFrame(rows)
    su["Revenue_growth"]=su.Revenue_T3/su.Revenue_T0-1

    wp=pd.DataFrame([
        ["WP1","Gestió i governança",.82,.80,60000,46800,4,4,1,4,0,18],
        ["WP2","Selecció i baseline",1.00,1.00,45000,43200,3,3,0,0,0,90],
        ["WP3","Acceleració",.76,.80,105000,75600,5,4,1,5,1,24],
        ["WP4","Experimentació",.61,.78,115000,65550,6,4,3,7,2,12],
        ["WP5","Mercat i internacionalització",.68,.70,75000,48000,4,4,1,2,1,35],
        ["WP6","Impacte i retorn",.55,.60,65000,31200,4,3,2,4,1,28],
        ["WP7","Comunicació i transferència",.58,.62,35000,18850,3,3,0,1,0,44],
    ],columns=["WP","Name","Progress","Planned","Budget","Spent","Milestones","Milestones_on_time","Open_risks","Docs_pending","Dependencies","Days_to_next"])
    wp["Schedule_gap"]=(wp.Planned-wp.Progress).clip(lower=0)
    wp["Budget_ratio"]=wp.Spent/wp.Budget
    wp["Risk_score"]=(38*(wp.Schedule_gap/.20).clip(0,1)+24*(wp.Open_risks/3).clip(0,1)+18*(wp.Docs_pending/7).clip(0,1)+10*(wp.Dependencies/2).clip(0,1)+10*((30-wp.Days_to_next)/30).clip(0,1)).round().astype(int)
    wp["Risk_30d"]=(wp.Risk_score+[-3,-1,4,18,5,9,3]).clip(0,100)
    wp["Predicted_status"]=pd.cut(wp.Risk_30d,[-1,39,69,100],labels=["VERD","TARONJA","VERMELL"]).astype(str)

    tasks=[]
    tid=1
    for _,r in wp.iterrows():
        for j in range(1,7):
            actual=float(np.clip(r.Progress+rng.uniform(-.10,.10),0,1)); planned=float(np.clip(r.Planned+rng.uniform(-.05,.05),0,1))
            tasks.append([f"T-{tid:03d}",r.WP,f"Tasca {r.WP}.{j}",rng.choice(["PMO","Impact Lead","WP Lead","Finance","Partner"]),planned,actual,rng.choice(["En curs","En curs","Completada","Pendent"]),int(rng.integers(3,60))])
            tid+=1
    tasks=pd.DataFrame(tasks,columns=["Task_ID","WP","Task","Owner","Planned","Actual","Status","Days_to_deadline"])

    alerts=pd.DataFrame([
        ["ALT-014","WP4","Retard lliurable","D4.2 a 12 dies i 55% completat","Crítica","WP4 Lead","Pla de recuperació","28/09/2026","Oberta"],
        ["ALT-021","WP4","Pilot bloquejat","Acord amb empresa pendent","Alta","WP4 Lead","Escalar contacte","25/09/2026","Oberta"],
        ["ALT-023","WP1","Documentació pendent","4 registres requereixen evidència","Alta","Finance / PM","Completar expedients","24/09/2026","En curs"],
        ["ALT-026","WP3","Outcome sota trajectòria","Nous clients per sota trajectòria","Mitjana","WP3 Lead","Reforçar suport comercial","05/10/2026","Oberta"],
        ["ALT-031","WP6","Dada no actualitzada",">30 dies des de darrera validació","Mitjana","Data Owner","Actualitzar i validar","30/09/2026","Oberta"],
    ],columns=["ID","WP","Alert","Trigger","Severity","Owner","Action","Deadline","Status"])

    outputs=pd.DataFrame([
        ["Startups seleccionades","Nº",0,20,20,"Registre Campus"],["Startups actives","Nº",0,18,19,"Seguiment"],
        ["Taxa de finalització","%",0,90,95,"Seguiment"],["Hores de mentoria","Hores",0,400,315,"Registre mentors"],
        ["Tallers realitzats","Nº",0,20,16,"Activitats"],["Assistència als tallers","%",0,85,88,"Assistència"],
        ["Diagnòstics T0 completats","%",0,100,100,"Formulari T0"],["Pilots iniciats","Nº",0,12,10,"WP4"],
        ["Pilots completats","Nº",0,10,6,"WP4"],["Connexions startup-empresa","Nº",0,60,48,"CRM"],
        ["Reunions amb inversors","Nº",0,40,31,"CRM"],["Plans d'escalabilitat","Nº",0,20,17,"WP3"],
        ["Startups en Demo Day","Nº",0,20,np.nan,"Demo Day"],["Connexions europees","Nº",0,30,22,"Partners / CRM"]
    ],columns=["Indicator","Unit","Baseline","Target","Actual","Source"])

    outcomes=pd.DataFrame([
        ["Models de negoci validats","%",30,80,72,"Seguiment startup"],["Startups amb nous clients","%",20,65,58,"Enquesta + evidència"],
        ["Nous clients captats","Nº",12,80,61,"CRM / startup"],["Startups amb pilot empresarial","%",10,60,50,"Convenis / pilots"],
        ["Pilots convertits en contracte","%",0,30,25,"Contractes"],["Startups amb nous mercats","%",15,50,42,"Seguiment"],
        ["Startups amb activitat internacional","%",10,40,35,"Seguiment"],["Inversió privada mobilitzada","€",0,1500000,1100000,"Evidència startup"],
        ["Startups que capten inversió","%",0,40,35,"Evidència"],["Creixement mitjà facturació","%",0,25,21,"Dades empreses"],
        ["Ocupació en startups","FTE",67,90,84,"Seguiment"],["Supervivència empresarial","%",100,90,np.nan,"Seguiment T4"],
        ["Col·laboracions empresarials noves","Nº",0,35,29,"CRM"],["Índex de capacitats empresarials","0-100",58,75,73,"Qüestionari T0-T1"]
    ],columns=["Indicator","Unit","Baseline","Target","Actual","Source"])

    impact=pd.DataFrame([
        ["Ocupació addicional","FTE T3 − FTE T0",67,23,17,"Analitzar contribució"],["Startups consolidades","% actives T4",np.nan,90,np.nan,"Longitudinal"],
        ["Creixement agregat facturació","% T0-T4",0,30,np.nan,"Factors externs"],["Inversió mobilitzada","€ acumulats",0,1500000,1100000,"No atribució automàtica"],
        ["Solucions innovadores adoptades","Nº",0,10,7,"Evidència d'adopció"],["Col·laboracions persistents","Nº actives >12 mesos",0,20,14,"Seguiment"],
        ["Startups internacionalitzades","%",10,40,35,"Seguiment"],["Continuïtat dels pilots","%",0,50,45,"T2/T3"],
        ["Efecte percebut del Campus","Evidència qualitativa",np.nan,np.nan,np.nan,"Entrevistes"],["Factors externs identificats","Nº + valoració",np.nan,100,np.nan,"Avaluació"]
    ],columns=["Indicator","Measure","Baseline","Target","Actual","Consideration"])

    territorial=pd.DataFrame([
        ["Ocupació i talent","Nous llocs de treball locals","FTE nous vinculats al territori",0,15,11],
        ["Ocupació i talent","% nova ocupació vinculada al territori","FTE locals / nous FTE",0,60,65],
        ["Ocupació i talent","Talent atret/retingut","Nº professionals",0,20,16],
        ["Economia","Startups implantades/vinculades","Nº",0,8,6],
        ["Economia","Despesa amb proveïdors locals","€",0,150000,118000],
        ["Economia","Contractes startup-empresa local","Nº",0,15,12],
        ["Innovació i coneixement","Pilots realitzats al territori","Nº",0,10,8],
        ["Innovació i coneixement","Pilots adoptats localment","Nº",0,5,3],
        ["Innovació i coneixement","Col·laboracions universitat/recerca","Nº",0,12,9],
        ["Innovació i coneixement","Accions de transferència","Nº",0,15,13],
        ["Ecosistema","Noves aliances territorials","Nº",0,25,21],
        ["Ecosistema","Aliances persistents >12 mesos","Nº",0,15,11],
        ["Economia","Inversió vinculada a startups arrelades","€",0,750000,610000],
        ["Ecosistema","Startups vinculades al territori T4","%",0,60,np.nan],
        ["Ecosistema","Startups amb ≥1 retorn verificable","%",0,75,70],
    ],columns=["Dimension","Indicator","Calculation","Baseline","Target","Actual"])
    return {"Startups":su,"Work_Packages":wp,"Tasks":tasks,"Alerts":alerts,"Outputs":outputs,"Outcomes":outcomes,"Impact":impact,"Territorial_Return":territorial}

EXPECTED={
    "Startups":["Startup","Sector","Jobs_T0","Jobs_T3","Revenue_T0","Revenue_T3","Investment"],
    "Work_Packages":["WP","Name","Progress","Planned","Budget","Spent","Open_risks","Docs_pending","Dependencies","Days_to_next"],
    "Tasks":["Task_ID","WP","Task","Owner","Planned","Actual","Status","Days_to_deadline"],
    "Alerts":["ID","WP","Alert","Trigger","Severity","Owner","Action","Deadline","Status"],
    "Outputs":["Indicator","Unit","Baseline","Target","Actual","Source"],
    "Outcomes":["Indicator","Unit","Baseline","Target","Actual","Source"],
    "Impact":["Indicator","Measure","Baseline","Target","Actual","Consideration"],
    "Territorial_Return":["Dimension","Indicator","Calculation","Baseline","Target","Actual"]
}

if "datasets" not in st.session_state:
    st.session_state.datasets=demo_data()
    st.session_state.data_mode="DEMO · DADES SINTÈTIQUES"

# -------------------- Data utilities --------------------
def refresh_derived(d):
    if "Startups" in d:
        x=d["Startups"].copy()
        if {"Revenue_T0","Revenue_T3"}.issubset(x.columns):
            x["Revenue_growth"]=(pd.to_numeric(x.Revenue_T3,errors="coerce")/pd.to_numeric(x.Revenue_T0,errors="coerce")-1)
        d["Startups"]=x
    if "Work_Packages" in d:
        x=d["Work_Packages"].copy()
        numeric=["Progress","Planned","Budget","Spent","Open_risks","Docs_pending","Dependencies","Days_to_next"]
        for c in numeric:
            if c in x: x[c]=pd.to_numeric(x[c],errors="coerce")
        if set(numeric).issubset(x.columns):
            x["Schedule_gap"]=(x.Planned-x.Progress).clip(lower=0)
            x["Budget_ratio"]=x.Spent/x.Budget.replace(0,np.nan)
            x["Risk_score"]=(38*(x.Schedule_gap/.20).clip(0,1)+24*(x.Open_risks/3).clip(0,1)+18*(x.Docs_pending/7).clip(0,1)+10*(x.Dependencies/2).clip(0,1)+10*((30-x.Days_to_next)/30).clip(0,1)).fillna(0).round().astype(int)
            if "Risk_30d" not in x: x["Risk_30d"]=x.Risk_score
            x["Predicted_status"]=pd.cut(pd.to_numeric(x.Risk_30d,errors="coerce").fillna(x.Risk_score),[-1,39,69,100],labels=["VERD","TARONJA","VERMELL"]).astype(str)
        d["Work_Packages"]=x
    return d

def validate(name,df):
    missing=[c for c in EXPECTED.get(name,[]) if c not in df.columns]
    return missing

def excel_bytes(datasets):
    out=io.BytesIO()
    with pd.ExcelWriter(out,engine="xlsxwriter") as w:
        for name,df in datasets.items():
            safe=name[:31]
            df.to_excel(w,sheet_name=safe,index=False)
            ws=w.sheets[safe]; ws.freeze_panes(1,0); ws.autofilter(0,0,len(df),max(0,len(df.columns)-1))
            for i,c in enumerate(df.columns): ws.set_column(i,i,min(max(len(str(c))+3,12),28))
    return out.getvalue()

def template_bytes(): return excel_bytes(demo_data())

def parse_paste(txt):
    txt=txt.strip()
    if not txt: return None
    try:
        dialect=csv.Sniffer().sniff(txt[:3000],delimiters="\t,;")
        sep=dialect.delimiter
    except Exception: sep="\t"
    return pd.read_csv(io.StringIO(txt),sep=sep)

def money(v):
    if pd.isna(v): return "—"
    if abs(v)>=1_000_000:return f"{v/1_000_000:.1f} M€".replace('.',',')
    if abs(v)>=1000:return f"{v/1000:.0f} k€"
    return f"{v:.0f} €"

def kpi(label,value,sub=""):
    st.markdown(f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-sub">{sub}</div></div>',unsafe_allow_html=True)

def section(title,sub=""):
    st.markdown(f'<div class="section-title">{title}</div><div class="section-sub">{sub}</div>',unsafe_allow_html=True)

def traffic(score):
    status="VERMELL" if score>=70 else "TARONJA" if score>=40 else "VERD"
    label={"VERMELL":"RISC ALT","TARONJA":"RISC MODERAT","VERD":"RISC CONTROLAT"}[status]
    return f'''<div class="traffic-wrap"><div class="traffic-light"><div class="light red {'on' if status=='VERMELL' else ''}"></div><div class="light amber {'on' if status=='TARONJA' else ''}"></div><div class="light green {'on' if status=='VERD' else ''}"></div></div><div class="risk-number">{score}%</div><div class="risk-label">{label}</div><div style="font-size:10.5px;color:#748094;text-align:center;margin-top:8px">Score explicable de risc de desviació a 30 dies</div></div>'''

def metric_table(df):
    cfg={}
    if "Actual" in df.columns: cfg["Actual"]=st.column_config.NumberColumn("Actual")
    return st.dataframe(df,hide_index=True,use_container_width=True,height=min(440,48+35*len(df)),column_config=cfg)

D=refresh_derived(st.session_state.datasets)
su=D.get("Startups",pd.DataFrame()); wp=D.get("Work_Packages",pd.DataFrame()); tasks=D.get("Tasks",pd.DataFrame()); alerts=D.get("Alerts",pd.DataFrame())
outputs=D.get("Outputs",pd.DataFrame()); outcomes=D.get("Outcomes",pd.DataFrame()); impact=D.get("Impact",pd.DataFrame()); territorial=D.get("Territorial_Return",pd.DataFrame())

# -------------------- Sidebar --------------------
st.sidebar.markdown("## NEÀPOLIS IMPACT")
st.sidebar.caption("Project & Impact Intelligence System")
st.sidebar.markdown(f"**{st.session_state.data_mode}**")
st.sidebar.divider()
project=st.sidebar.selectbox("Projecte",["Campus Europeu d'Emprenedoria Disruptiva"])
timepoint=st.sidebar.selectbox("Tall temporal",["T3 · +12 mesos","T2 · +6 mesos","T1 · final programa","T0 · baseline"])
startup_filter=st.sidebar.selectbox("Startup",["Totes"]+(su.Startup.tolist() if "Startup" in su else []))
st.sidebar.divider()
st.sidebar.markdown("**Cadena de valor**")
st.sidebar.caption("Execució → Outputs → Outcomes → Impacte → Retorn territorial")
st.sidebar.divider()
if st.sidebar.button("↺ Restaurar dades demo",use_container_width=True):
    st.session_state.datasets=demo_data(); st.session_state.data_mode="DEMO · DADES SINTÈTIQUES"; st.rerun()

st.markdown(f'''<div class="hero"><div class="demo">{st.session_state.data_mode}</div><div class="eyebrow">Project & Impact Intelligence System</div><h1>NEÀPOLIS IMPACT</h1><p>Quadre de comandament per connectar execució, alerta primerenca, resultats, impacte i retorn territorial en projectes europeus.</p></div>''',unsafe_allow_html=True)

# -------------------- Navigation --------------------
tabs=st.tabs(["01 · Executive","02 · Execució","03 · Outputs","04 · Outcomes","05 · Impacte","06 · Retorn territorial","07 · Predictive Control","08 · Data Hub","09 · Metodologia"])

with tabs[0]:
    progress=float(wp.Progress.mean()) if "Progress" in wp else 0
    budget=float(wp.Spent.sum()/wp.Budget.sum()) if {"Spent","Budget"}.issubset(wp) else 0
    milestones=int(wp.Milestones_on_time.sum()) if "Milestones_on_time" in wp else 0; mt=int(wp.Milestones.sum()) if "Milestones" in wp else 0
    risk=int(wp.Risk_30d.max()) if "Risk_30d" in wp else 0
    c=st.columns(6)
    with c[0]: kpi("Salut del projecte",f"{progress:.0%}","Execució mitjana")
    with c[1]: kpi("Pressupost",f"{budget:.0%}",f"{money(wp.Spent.sum())} / {money(wp.Budget.sum())}")
    with c[2]: kpi("Fites en termini",f"{milestones}/{mt}","Puntualitat acumulada")
    with c[3]: kpi("Risc predictiu",f"{risk}%","Màxim a 30 dies")
    with c[4]: kpi("Startups actives",f"{int(su.Active.sum())}/{len(su)}" if "Active" in su else "—","Cohort")
    with c[5]: kpi("Inversió",money(su.Investment.sum()) if "Investment" in su else "—","Mobilitzada")
    st.markdown('<div class="callout"><b>Lectura executiva:</b> el sistema combina control operatiu, resultats i impacte. La priorització no acaba en l’alerta: identifica responsable, acció correctora, termini i verificació.</div>',unsafe_allow_html=True)
    l,r=st.columns([1.35,1])
    with l:
        section("Rendiment del projecte","Progrés real vs planificat per Work Package")
        p=wp[["WP","Progress","Planned"]].melt("WP",var_name="Sèrie",value_name="Valor")
        fig=px.bar(p,x="WP",y="Valor",color="Sèrie",barmode="group",text_auto=".0%")
        fig.update_layout(height=370,yaxis_tickformat=".0%",yaxis_range=[0,1.1],legend_title="",margin=dict(l=10,r=10,t=10,b=10),paper_bgcolor="white",plot_bgcolor="white")
        st.plotly_chart(fig,use_container_width=True)
    with r:
        section("Top alertes","Elements que requereixen decisió")
        st.dataframe(alerts[[c for c in ["Severity","WP","Alert","Owner","Deadline"] if c in alerts]],hide_index=True,use_container_width=True,height=370)
    section("Arquitectura de valor","Cinc nivells, una mateixa capa de dades")
    cols=st.columns(5)
    labels=[("1 · EXECUCIÓ","Estem executant correctament i a temps?"),("2 · OUTPUTS","Què ha produït directament la intervenció?"),("3 · OUTCOMES","Què ha canviat en les startups?"),("4 · IMPACTE","Quin canvi de major abast observem?"),("5 · RETORN","Quin valor queda vinculat al territori?")]
    for col,(a,b) in zip(cols,labels):
        with col: st.markdown(f'<div class="level"><b>{a}</b><br>{b}</div>',unsafe_allow_html=True)

with tabs[1]:
    section("Nivell 1 · Execució i control","Project Management: calendari, pressupost, documentació, riscos i responsabilitats")
    ctrl=wp.copy(); ctrl["Progress_%"]=(ctrl.Progress*100).round().astype(int); ctrl["Planned_%"]=(ctrl.Planned*100).round().astype(int); ctrl["Budget_execution_%"]=(ctrl.Budget_ratio*100).round().astype(int)
    st.dataframe(ctrl[[c for c in ["WP","Name","Progress_%","Planned_%","Budget","Spent","Budget_execution_%","Milestones","Milestones_on_time","Open_risks","Docs_pending","Dependencies","Days_to_next","Risk_score","Predicted_status"] if c in ctrl]],hide_index=True,use_container_width=True,height=330,column_config={"Risk_score":st.column_config.ProgressColumn("Risc",min_value=0,max_value=100,format="%d%%")})
    l,r=st.columns(2)
    with l:
        section("Task tracker","Drill-down: PROJECT → WP → TASK")
        f=st.selectbox("Filtra Work Package",["Tots"]+wp.WP.tolist(),key="taskfilter"); tt=tasks if f=="Tots" else tasks[tasks.WP==f]
        st.dataframe(tt,hide_index=True,use_container_width=True,height=350,column_config={"Planned":st.column_config.ProgressColumn("Planificat", min_value=0, max_value=1, format="%.0%%"),"Actual":st.column_config.ProgressColumn("Real", min_value=0, max_value=1, format="%.0%%")})
    with r:
        section("Corrective Action Log","DETECCIÓ → ALERTA → RESPONSABLE → ACCIÓ → TERMINI → VERIFICACIÓ")
        st.dataframe(alerts,hide_index=True,use_container_width=True,height=350)

with tabs[2]:
    section("Nivell 2 · Outputs","Què ha produït directament la intervenció? Activitat no és encara impacte.")
    metric_table(outputs)
    if not outputs.empty:
        x=outputs.dropna(subset=["Actual","Target"]).copy(); x=x[x.Unit!="€"]
        fig=px.bar(x,x="Indicator",y=["Actual","Target"],barmode="group")
        fig.update_layout(height=390,xaxis_title="",yaxis_title="Valor",legend_title="",margin=dict(l=10,r=10,t=10,b=120),paper_bgcolor="white",plot_bgcolor="white")
        st.plotly_chart(fig,use_container_width=True)
    st.info("Una execució elevada (hores de mentoria, tallers o connexions) no demostra per si mateixa que s'hagi produït un canvi en les startups.")

with tabs[3]:
    section("Nivell 3 · Outcomes","Canvis observats en les startups després de la intervenció")
    cards=[("Models validats","72%","Target 80%"),("Nous clients","58%","Target 65%"),("Amb pilots","50%","Target 60%"),("Inversió","1,1 M€","Target 1,5 M€"),("Facturació","+21%","Target +25%"),("Ocupació","84 FTE","67 FTE a T0")]
    cc=st.columns(6)
    for col,(a,b,csub) in zip(cc,cards):
        with col:kpi(a,b,csub)
    metric_table(outcomes)
    section("Trajectòria T0 → T4","Visualització longitudinal demostrativa dels KPI estrella")
    traj=pd.DataFrame({"Moment":["T0","T1","T2","T3","T4 target"],"Models validats":[30,45,60,72,80],"Nous clients":[20,31,45,58,65],"Pilots":[10,20,35,50,60],"Internacionalització":[10,17,25,35,40]})
    fig=px.line(traj,x="Moment",y=["Models validats","Nous clients","Pilots","Internacionalització"],markers=True)
    fig.update_layout(height=390,yaxis_title="% startups",legend_title="",margin=dict(l=10,r=10,t=10,b=10),paper_bgcolor="white",plot_bgcolor="white")
    st.plotly_chart(fig,use_container_width=True)
    section("Base analítica de startups","Els outcomes es poden auditar fins al registre individual")
    data=su if startup_filter=="Totes" else su[su.Startup==startup_filter]
    st.dataframe(data,hide_index=True,use_container_width=True,height=330)

with tabs[4]:
    section("Nivell 4 · Impacte","Canvi de major abast i anàlisi de la contribució del projecte")
    st.markdown('<div class="callout"><b>RESULTAT OBSERVAT ≠ IMPACTE ATRIBUÏBLE.</b> El dashboard separa evidència observada, contribució plausible i factors externs.</div>',unsafe_allow_html=True)
    metric_table(impact)
    l,r=st.columns([1,1])
    with l:
        section("Ocupació","Evolució agregada T0–T3")
        j0=int(su.Jobs_T0.sum()); j3=int(su.Jobs_T3.sum())
        fig=px.bar(pd.DataFrame({"Moment":["T0","T3"],"FTE":[j0,j3]}),x="Moment",y="FTE",text_auto=True)
        fig.update_layout(height=330,margin=dict(l=10,r=10,t=10,b=10),paper_bgcolor="white",plot_bgcolor="white")
        st.plotly_chart(fig,use_container_width=True)
    with r:
        section("Evidència d'impacte","Triangulació proposada")
        st.markdown('<div class="method"><b>Quantitativa</b> · T0–T4, CRM, facturació, ocupació, inversió, contractes.<br><b>Qualitativa</b> · entrevistes, percepció del canvi, mecanismes i factors externs.<br><b>Avaluació</b> · anàlisi de contribució; contrafactual només quan el disseny i les dades ho permetin.<br><b>Traçabilitat</b> · cada KPI manté font, període i evidència.</div>',unsafe_allow_html=True)

with tabs[5]:
    section("Nivell 5 · Retorn territorial","Retorn mesurable vinculat al territori, sense construir un índex sintètic arbitrari")
    dims=["Economia","Ocupació i talent","Innovació i coneixement","Ecosistema"]
    cols=st.columns(4)
    for col,dim in zip(cols,dims):
        dd=territorial[territorial.Dimension==dim]; achieved=(dd.Actual/dd.Target.replace(0,np.nan)*100).replace([np.inf,-np.inf],np.nan).mean()
        with col:kpi(dim,f"{achieved:.0f}%" if pd.notna(achieved) else "—","Assoliment mitjà dels KPI amb dada")
    metric_table(territorial)
    section("Actual vs target","Comparació per indicador")
    t=territorial.dropna(subset=["Actual","Target"]).copy(); t["Assoliment_%"]=(t.Actual/t.Target.replace(0,np.nan)*100).clip(0,150)
    fig=px.bar(t,x="Assoliment_%",y="Indicator",color="Dimension",orientation="h",text_auto=".0f")
    fig.add_vline(x=100,line_dash="dash",annotation_text="Target")
    fig.update_layout(height=520,xaxis_title="% del target",yaxis_title="",legend_title="",margin=dict(l=10,r=10,t=10,b=10),paper_bgcolor="white",plot_bgcolor="white")
    st.plotly_chart(fig,use_container_width=True)

with tabs[6]:
    section("Predictive Control Center","Semàfor de risc gran, explicable i orientat a decisió")
    score=int(wp.Risk_30d.max()) if "Risk_30d" in wp else int(wp.Risk_score.max())
    a,b=st.columns([.72,1.7])
    with a: st.markdown(traffic(score),unsafe_allow_html=True)
    with b:
        st.markdown('<div class="method"><b>Motor predictiu demostratiu</b><br>El score combina regles transparents: desviació de calendari <b>38%</b>, riscos oberts <b>24%</b>, documentació pendent <b>18%</b>, dependències <b>10%</b> i proximitat de la fita <b>10%</b>.<br><br><b>Llindars:</b> 0–39 verd · 40–69 taronja · 70–100 vermell.<br><br><b>No és un model ML entrenat.</b> És una analítica predictiva basada en regles explicables. Amb històric suficient, es podria validar un model estadístic/ML mantenint supervisió humana.</div>',unsafe_allow_html=True)
        section("Risc actual → previsió 30 dies","Priorització per Work Package")
        risk=wp[["WP","Name","Risk_score","Risk_30d","Predicted_status","Schedule_gap","Open_risks","Docs_pending","Dependencies","Days_to_next"]]
        st.dataframe(risk,hide_index=True,use_container_width=True,height=280,column_config={"Risk_score":st.column_config.ProgressColumn("Actual", min_value=0, max_value=100, format="%d%%"),"Risk_30d":st.column_config.ProgressColumn("+30 dies", min_value=0, max_value=100, format="%d%%")})
    l,r=st.columns([1.2,1])
    with l:
        rr=wp[["WP","Risk_score","Risk_30d"]].melt("WP",var_name="Moment",value_name="Risk")
        fig=px.bar(rr,x="WP",y="Risk",color="Moment",barmode="group",text_auto=True)
        fig.add_hrect(y0=70,y1=100,opacity=.08,line_width=0); fig.add_hrect(y0=40,y1=70,opacity=.06,line_width=0)
        fig.update_layout(height=390,yaxis_range=[0,100],yaxis_title="Score de risc",legend_title="",margin=dict(l=10,r=10,t=10,b=10),paper_bgcolor="white",plot_bgcolor="white")
        st.plotly_chart(fig,use_container_width=True)
    with r:
        selected=st.selectbox("Explica el risc de",wp.WP.tolist(),index=min(3,len(wp)-1),key="riskwp"); w=wp[wp.WP==selected].iloc[0]
        factors=pd.DataFrame({"Factor":["Desviació calendari","Riscos oberts","Documentació pendent","Dependències","Proximitat fita"],"Punts":[38*min(max(w.Schedule_gap,0)/.20,1),24*min(w.Open_risks/3,1),18*min(w.Docs_pending/7,1),10*min(w.Dependencies/2,1),10*max((30-w.Days_to_next)/30,0)]})
        fig=px.bar(factors,x="Punts",y="Factor",orientation="h",text_auto=".0f")
        fig.update_layout(height=390,xaxis_title="Contribució al risc",yaxis_title="",margin=dict(l=10,r=10,t=10,b=10),paper_bgcolor="white",plot_bgcolor="white")
        st.plotly_chart(fig,use_container_width=True)
    section("Early Warning System","L'alerta només té valor si desencadena una acció gestionable")
    st.dataframe(alerts,hide_index=True,use_container_width=True,height=330)

with tabs[7]:
    section("Data Hub","Consultar, editar, importar i exportar la capa de dades del sistema")
    st.markdown("Pots treballar amb les **dades demo**, carregar un **Excel/CSV propi** o **copiar i enganxar una taula**. Les dades carregades només viuen en la sessió actual de l'app.")
    u1,u2,u3=st.tabs(["📂 Pujar Excel / CSV","📋 Copiar i enganxar","🔎 Explorar i exportar"])
    with u1:
        st.download_button("⬇ Descarregar plantilla Excel",template_bytes(),"NEAPOLIS_IMPACT_plantilla.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",use_container_width=True)
        st.caption("La plantilla conté 8 fulls amb els noms i columnes que espera el dashboard. Pots substituir les files demo per dades pròpies.")
        up=st.file_uploader("Puja un .xlsx, .xlsm o .csv",type=["xlsx","xlsm","csv"])
        if up is not None:
            try:
                candidate={}
                if up.name.lower().endswith(".csv"):
                    target=st.selectbox("A quin dataset correspon el CSV?",list(EXPECTED.keys()))
                    candidate[target]=pd.read_csv(up)
                else:
                    book=pd.read_excel(up,sheet_name=None)
                    candidate={k:v for k,v in book.items() if k in EXPECTED}
                    st.write("Fulls reconeguts:",", ".join(candidate.keys()) if candidate else "cap")
                problems=[]
                for name,df in candidate.items():
                    miss=validate(name,df)
                    if miss: problems.append(f"{name}: falten {', '.join(miss)}")
                if problems:
                    st.error("No es pot aplicar encara:\n- "+"\n- ".join(problems))
                elif candidate and st.button("Aplicar dades carregades",type="primary"):
                    merged=st.session_state.datasets.copy(); merged.update(candidate); st.session_state.datasets=refresh_derived(merged); st.session_state.data_mode="DADES CARREGADES · SESSIÓ"; st.success("Dades aplicades al dashboard."); st.rerun()
            except Exception as e: st.error(f"No s'ha pogut llegir el fitxer: {e}")
    with u2:
        target=st.selectbox("Taula que vols substituir",list(EXPECTED.keys()),key="paste_target")
        st.caption("Copia directament des d'Excel o Google Sheets incloent la fila de capçaleres. També accepta CSV amb comes o punt i coma.")
        txt=st.text_area("Enganxa aquí la taula",height=220,placeholder="Startup\tSector\tJobs_T0\tJobs_T3\tRevenue_T0\tRevenue_T3\tInvestment\n...")
        parsed=None
        if txt.strip():
            try:
                parsed=parse_paste(txt); st.dataframe(parsed,hide_index=True,use_container_width=True,height=250)
                miss=validate(target,parsed)
                if miss: st.warning("Columnes obligatòries que falten: "+", ".join(miss))
                elif st.button("Aplicar taula enganxada",type="primary"):
                    merged=st.session_state.datasets.copy(); merged[target]=parsed; st.session_state.datasets=refresh_derived(merged); st.session_state.data_mode="DADES ENGANXADES · SESSIÓ"; st.rerun()
            except Exception as e: st.error(f"No s'ha pogut interpretar la taula: {e}")
    with u3:
        which=st.selectbox("Dataset",list(D.keys()),key="explore")
        st.dataframe(D[which],hide_index=True,use_container_width=True,height=480)
        st.download_button("⬇ Descarregar tot el model en Excel",excel_bytes(D),"NEAPOLIS_IMPACT_data.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",use_container_width=True)
        st.download_button(f"⬇ Descarregar {which} en CSV",D[which].to_csv(index=False).encode("utf-8-sig"),f"{which}.csv","text/csv",use_container_width=True)

with tabs[8]:
    section("Metodologia i governança","De la Teoria del Canvi a la decisió basada en evidència")
    st.markdown('<div class="method"><b>TEORIA DEL CANVI</b> → cadena causal → <b>INDICADORS</b> → dades → <b>NEÀPOLIS IMPACT</b> → alertes → decisió/acció correctora → avaluació → aprenentatge.<br><br><b>Separació analítica:</b> Inputs/activitats → Outputs → Outcomes → Impactes → Retorn territorial.<br><b>Temporalitat:</b> T0 baseline · T1 final programa · T2 +6 mesos · T3 +12 mesos · T4 +24 mesos.<br><b>Governança de dades:</b> font, data owner, periodicitat, validació, traçabilitat, minimització de dades personals i supervisió humana.<br><b>Analítica predictiva:</b> primer regles explicables i llindars; només evolucionar a models estadístics/ML quan hi hagi volum, qualitat i històric suficients.</div>',unsafe_allow_html=True)
    st.markdown("#### Diccionari funcional")
    dictionary=pd.DataFrame([
        ["Execució","Project management","Tasques, fites, lliurables, pressupost, evidències, riscos"],
        ["Outputs","Productes directes","Startups, mentoria, tallers, pilots, connexions"],
        ["Outcomes","Canvi en participants","Clients, models validats, mercats, inversió, facturació, ocupació"],
        ["Impacte","Canvi de major abast","Consolidació, ocupació addicional, adopció, persistència"],
        ["Retorn territorial","Valor vinculat al territori","Economia, ocupació/talent, innovació/coneixement, ecosistema"],
        ["Early Warning","Anticipació","Risc → responsable → acció → termini → verificació"]],columns=["Capa","Pregunta","Exemples"])
    st.dataframe(dictionary,hide_index=True,use_container_width=True)
    st.info("Prototip funcional. Quan s'utilitzen dades demo, tots els valors són sintètics i no representen resultats reals de Neàpolis.")
