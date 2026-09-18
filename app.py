import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta

st.set_page_config(page_title="NEÀPOLIS IMPACT", page_icon="◼", layout="wide", initial_sidebar_state="expanded")

# ---------- Premium visual layer ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {font-family:'Inter',sans-serif;}
[data-testid="stAppViewContainer"] {background:#F6F7F9;}
[data-testid="stSidebar"] {background:#0B1220; border-right:1px solid #172033;}
[data-testid="stSidebar"] * {color:#E5E7EB;}
.block-container {padding-top:1.25rem; padding-bottom:2rem; max-width:1500px;}
#MainMenu, footer, header {visibility:hidden;}
.hero {background:linear-gradient(120deg,#0B1220 0%,#172033 60%,#26344C 100%); padding:26px 30px; border-radius:18px; color:white; margin-bottom:18px; box-shadow:0 10px 35px rgba(15,23,42,.10);}
.eyebrow {font-size:11px; letter-spacing:.16em; font-weight:800; color:#9CA3AF; text-transform:uppercase;}
.hero h1 {font-size:34px; line-height:1.05; margin:6px 0 8px 0; letter-spacing:-.04em;}
.hero p {font-size:14px; color:#CBD5E1; margin:0; max-width:900px;}
.kpi {background:white; border:1px solid #E5E7EB; border-radius:15px; padding:17px 18px 15px; min-height:112px; box-shadow:0 3px 14px rgba(15,23,42,.04);}
.kpi-label {font-size:11px; color:#6B7280; font-weight:700; text-transform:uppercase; letter-spacing:.06em;}
.kpi-value {font-size:27px; font-weight:800; letter-spacing:-.04em; margin-top:8px; color:#111827;}
.kpi-sub {font-size:11px; color:#6B7280; margin-top:4px;}
.section-title {font-size:19px; font-weight:800; letter-spacing:-.025em; color:#111827; margin:8px 0 2px;}
.section-sub {font-size:12px; color:#6B7280; margin-bottom:12px;}
.badge {display:inline-block; padding:5px 9px; border-radius:999px; font-size:10px; font-weight:800; letter-spacing:.05em;}
.badge-demo {background:#FEF3C7;color:#92400E;}
.callout {background:#EEF2FF;border:1px solid #DDE3FF;border-radius:14px;padding:14px 16px;font-size:12px;color:#3730A3;margin:8px 0 15px;}
[data-testid="stMetric"] {background:white;border:1px solid #E5E7EB;padding:14px;border-radius:14px;box-shadow:0 3px 14px rgba(15,23,42,.04);}
div[data-testid="stDataFrame"] {background:white;border-radius:14px;border:1px solid #E5E7EB;padding:5px;}
.stTabs [data-baseweb="tab-list"] {gap:7px; background:#ECEFF3; padding:5px; border-radius:12px;}
.stTabs [data-baseweb="tab"] {height:38px;border-radius:9px;padding:0 15px;font-size:12px;font-weight:700;}
.stTabs [aria-selected="true"] {background:white !important; box-shadow:0 1px 4px rgba(15,23,42,.08);}
hr {border:none;border-top:1px solid #E5E7EB;margin:1rem 0;}
</style>
""", unsafe_allow_html=True)

# ---------- Synthetic model ----------
@st.cache_data
def build_data(seed=42):
    rng=np.random.default_rng(seed)
    startups=[f"Startup {i:02d}" for i in range(1,21)]
    sectors=["AI & Data","Blue Economy","HealthTech","ClimateTech","CreativeTech","Smart City"]
    stages=["Prototype","MVP","Early traction","Growth"]
    rows=[]
    for i,s in enumerate(startups):
        jobs0=int(rng.integers(2,6)); jobs3=jobs0+int(rng.integers(0,4))
        rev0=int(rng.integers(35,210))*1000
        growth=float(rng.uniform(.05,.46)); rev3=int(rev0*(1+growth))
        investment=int(rng.choice([0,0,50000,100000,150000,250000,400000]))
        local_jobs=max(0,jobs3-jobs0-int(rng.integers(0,2)))
        rows.append([s,rng.choice(sectors),rng.choice(stages),jobs0,jobs3,rev0,rev3,investment,
                     int(rng.integers(0,6)),int(rng.integers(0,3)),int(rng.integers(0,2)),local_jobs,
                     int(rng.integers(0,2)),int(rng.integers(0,3)),int(rng.integers(0,2)),int(rng.integers(55,82))])
    su=pd.DataFrame(rows,columns=["Startup","Sector","Stage","Jobs_T0","Jobs_T3","Revenue_T0","Revenue_T3","Investment","New_clients","Pilots","Local_pilots","Local_jobs","Local_supplier","Alliances","Validated_model","Capability_T1"])
    su["Revenue_growth"]=(su.Revenue_T3/su.Revenue_T0-1)
    su["New_market"]=(rng.random(len(su))<.45).astype(int)
    su["Active"]=(rng.random(len(su))<.95).astype(int)
    su["Capability_T0"]=rng.integers(48,65,len(su))

    wps=[
        ("WP1","Gestió i governança",.82,60000),("WP2","Selecció i baseline",1.00,45000),
        ("WP3","Acceleració",.76,105000),("WP4","Experimentació",.61,115000),
        ("WP5","Mercat i internacionalització",.68,75000),("WP6","Impacte i retorn",.55,65000),
        ("WP7","Comunicació i transferència",.58,35000)]
    wp=pd.DataFrame(wps,columns=["WP","Name","Progress","Budget"])
    wp["Planned"]=[.80,1,.80,.78,.70,.60,.62]
    wp["Spent"]=(wp.Budget*np.array([.78,.96,.72,.57,.64,.48,.53])).astype(int)
    wp["Milestones"]=[4,3,5,6,4,4,3]
    wp["Milestones_on_time"]=[4,3,4,4,4,3,3]
    wp["Open_risks"]=[1,0,1,3,1,2,0]

    alerts=pd.DataFrame([
        ["ALT-014","WP4","Lliurable D4.2 en risc", "Crítica","12 dies fins al termini · 55% completat","WP4 Lead","Pla de recuperació","Oberta"],
        ["ALT-018","WP6","Seguiment T2 incomplet", "Mitjana","4 startups pendents de validació","Impact Lead","Completar evidències","En curs"],
        ["ALT-021","WP4","Pilot bloquejat", "Alta","Acord amb empresa pendent","WP4 Lead","Escalar contacte","Oberta"],
        ["ALT-023","WP1","Evidència documental pendent", "Alta","7 registres requereixen documentació","Finance","Completar expedients","En curs"],
        ["ALT-026","WP5","Outcome sota trajectòria", "Mitjana","Nous mercats: 35% vs target 40%","WP5 Lead","Reforç comercial","Oberta"],
    ],columns=["ID","WP","Alert","Severity","Trigger","Owner","Action","Status"])
    return su,wp,alerts

su,wp,alerts=build_data()

# Force coherent demo headline figures
su.loc[:13,"Validated_model"]=1
su.loc[:10,"Local_jobs"]=1

# ---------- Helpers ----------
def money(v):
    if abs(v)>=1_000_000: return f"{v/1_000_000:.1f} M€".replace('.',',')
    return f"{v/1000:.0f} k€"

def kpi(label,value,sub=""):
    st.markdown(f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-sub">{sub}</div></div>',unsafe_allow_html=True)

def section(title,sub=""):
    st.markdown(f'<div class="section-title">{title}</div><div class="section-sub">{sub}</div>',unsafe_allow_html=True)

def status_color(x):
    return "#16A34A" if x>=.9 else "#D97706" if x>=.7 else "#DC2626"

# ---------- Sidebar ----------
st.sidebar.markdown("## NEÀPOLIS **IMPACT**")
st.sidebar.caption("Project & Impact Intelligence")
st.sidebar.markdown("---")
project=st.sidebar.selectbox("Projecte",["Campus Europeu d’Emprenedoria Innovadora"])
period=st.sidebar.selectbox("Tall temporal",["T3 · +12 mesos","T2 · +6 mesos","T1 · Final programa","T0 · Baseline"])
startup_filter=st.sidebar.selectbox("Drill-down startup",["Totes"]+su.Startup.tolist())
st.sidebar.markdown("---")
st.sidebar.markdown("**Cadena de valor**")
st.sidebar.caption("Execució → Outputs → Outcomes → Impacte → Retorn territorial")
st.sidebar.markdown("---")
st.sidebar.caption("DEMO · Dades 100% sintètiques")

st.markdown("""
<div class="hero">
  <span class="badge badge-demo">DEMO · SYNTHETIC DATA</span>
  <div class="eyebrow" style="margin-top:14px">PROJECT & IMPACT INTELLIGENCE SYSTEM</div>
  <h1>NEÀPOLIS IMPACT</h1>
  <p>Quadre de comandament per connectar execució, alerta primerenca, resultats, impacte i retorn territorial en projectes europeus.</p>
</div>
""",unsafe_allow_html=True)

# headline calculations
budget=wp.Budget.sum(); spent=wp.Spent.sum(); project_progress=np.average(wp.Progress,weights=wp.Budget)
ms=int(wp.Milestones.sum()); ms_ok=int(wp.Milestones_on_time.sum())
critical=(alerts.Severity.isin(["Crítica","Alta"])).sum()
investment=su.Investment.sum(); jobs0=su.Jobs_T0.sum(); jobs3=su.Jobs_T3.sum()

c=st.columns(6)
with c[0]: kpi("Project health",f"{project_progress:.0%}","Execució ponderada")
with c[1]: kpi("Pressupost",f"{spent/budget:.0%}",f"{money(spent)} / {money(budget)}")
with c[2]: kpi("Fites en termini",f"{ms_ok}/{ms}",f"{ms_ok/ms:.0%} puntualitat")
with c[3]: kpi("Alertes prioritàries",str(critical),"Crítiques + altes")
with c[4]: kpi("Startups actives",f"{su.Active.sum()}/20","Cohort pilot")
with c[5]: kpi("Inversió mobilitzada",money(investment),"Dada sintètica acumulada")

st.markdown('<div class="callout"><b>Lectura executiva:</b> el projecte manté una execució global estable, però WP4 concentra el principal risc operatiu. El sistema prioritza la intervenció abans del venciment del lliurable i connecta el seguiment amb els outcomes i el retorn territorial.</div>',unsafe_allow_html=True)

tab1,tab2,tab3,tab4,tab5=st.tabs(["Executive Overview","Project Control","Impact Intelligence","Territorial Return","Methodology"])

with tab1:
    left,right=st.columns([1.25,1])
    with left:
        section("Project performance","Progrés real vs planificat per Work Package")
        plot=wp.melt(id_vars=["WP","Name"],value_vars=["Progress","Planned"],var_name="Serie",value_name="Value")
        fig=px.bar(plot,x="WP",y="Value",color="Serie",barmode="group",hover_data=["Name"],text_auto=".0%")
        fig.update_layout(height=330,margin=dict(l=10,r=10,t=10,b=10),yaxis_tickformat=".0%",legend_title="",paper_bgcolor="white",plot_bgcolor="white")
        st.plotly_chart(fig,use_container_width=True)
    with right:
        section("Early Warning","Alertes que requereixen decisió")
        st.dataframe(alerts[["Severity","WP","Alert","Owner","Status"]],hide_index=True,use_container_width=True,height=330)
    section("Outcome pulse","Indicadors de canvi de la cohort")
    q=st.columns(5)
    with q[0]: kpi("Models validats",f"{su.Validated_model.mean():.0%}","Outcome")
    with q[1]: kpi("Nous clients",f"{(su.New_clients>0).mean():.0%}","Startups amb ≥1")
    with q[2]: kpi("Pilots",str(su.Pilots.sum()),"Experimentació")
    with q[3]: kpi("Ocupació",f"+{jobs3-jobs0}",f"{jobs0} → {jobs3} FTE")
    with q[4]: kpi("Facturació",f"+{su.Revenue_growth.mean():.0%}","Variació mitjana T0–T3")

with tab2:
    section("Work Package Control","Cronograma, pressupost, fites i risc en una única vista")
    ctrl=wp.copy()
    ctrl["Progress"]=ctrl.Progress.map(lambda x:f"{x:.0%}")
    ctrl["Planned"]=ctrl.Planned.map(lambda x:f"{x:.0%}")
    ctrl["Budget"]=ctrl.Budget.map(money); ctrl["Spent"]=ctrl.Spent.map(money)
    st.dataframe(ctrl,hide_index=True,use_container_width=True)
    a,b=st.columns([1,1])
    with a:
        section("Budget control","Despesa executada per WP")
        fig=go.Figure()
        fig.add_bar(x=wp.WP,y=wp.Budget,name="Pressupost")
        fig.add_bar(x=wp.WP,y=wp.Spent,name="Executat")
        fig.update_layout(barmode="group",height=320,margin=dict(l=10,r=10,t=10,b=10),legend_title="",paper_bgcolor="white",plot_bgcolor="white")
        st.plotly_chart(fig,use_container_width=True)
    with b:
        section("Risk concentration","Riscos oberts per paquet de treball")
        fig=px.bar(wp,x="WP",y="Open_risks",text_auto=True,hover_data=["Name"])
        fig.update_layout(height=320,margin=dict(l=10,r=10,t=10,b=10),paper_bgcolor="white",plot_bgcolor="white")
        st.plotly_chart(fig,use_container_width=True)
    section("Corrective Action Log","DETECCIÓ → ALERTA → RESPONSABLE → ACCIÓ → TERMINI → VERIFICACIÓ")
    action=alerts.copy(); action["Deadline"]=["28/09","30/09","25/09","24/09","05/10"]
    st.dataframe(action[["ID","WP","Alert","Trigger","Owner","Action","Deadline","Status"]],hide_index=True,use_container_width=True)

with tab3:
    data=su if startup_filter=="Totes" else su[su.Startup==startup_filter]
    section("Impact Intelligence","De l'activitat al canvi observat: T0 → T3")
    c=st.columns(5)
    with c[0]: kpi("Cohort",str(len(data)),"Startups seleccionades")
    with c[1]: kpi("Models validats",f"{data.Validated_model.mean():.0%}","Outcome")
    with c[2]: kpi("Inversió",money(data.Investment.sum()),"Mobilitzada")
    with c[3]: kpi("Ocupació",f"+{data.Jobs_T3.sum()-data.Jobs_T0.sum()}","FTE T0 → T3")
    with c[4]: kpi("Facturació",f"+{data.Revenue_growth.mean():.0%}","Creixement mitjà")
    l,r=st.columns([1.2,1])
    with l:
        section("Employment evolution","Comparació per startup")
        emp=data[["Startup","Jobs_T0","Jobs_T3"]].melt(id_vars="Startup",var_name="Moment",value_name="FTE")
        fig=px.bar(emp,x="Startup",y="FTE",color="Moment",barmode="group")
        fig.update_layout(height=360,margin=dict(l=10,r=10,t=10,b=70),paper_bgcolor="white",plot_bgcolor="white")
        st.plotly_chart(fig,use_container_width=True)
    with r:
        section("Outcome funnel","Conversió de la intervenció")
        vals=[20,int(su.Active.sum()),int((su.Pilots>0).sum()),int((su.New_clients>0).sum()),int(su.Validated_model.sum())]
        fig=go.Figure(go.Funnel(y=["Seleccionades","Actives","Amb pilot","Amb nous clients","Model validat"],x=vals,textinfo="value+percent initial"))
        fig.update_layout(height=360,margin=dict(l=10,r=10,t=10,b=10),paper_bgcolor="white")
        st.plotly_chart(fig,use_container_width=True)
    st.caption("Nota metodològica: RESULTAT OBSERVAT ≠ IMPACTE ATRIBUÏBLE. En cohorts petites es proposa anàlisi de contribució i seguiment longitudinal T0–T4.")

with tab4:
    section("Territorial Return","Valor generat que manté una vinculació verificable amb el territori")
    local_jobs=int(su.Local_jobs.sum()); local_pilots=int(su.Local_pilots.sum()); alliances=int(su.Alliances.sum()); suppliers=int(su.Local_supplier.sum())
    c=st.columns(4)
    with c[0]: kpi("Economia",money(suppliers*14500),"Despesa local estimada demo")
    with c[1]: kpi("Ocupació & talent",f"+{local_jobs} FTE","Nous llocs locals")
    with c[2]: kpi("Innovació",str(local_pilots),"Pilots al territori")
    with c[3]: kpi("Ecosistema",str(alliances),"Noves aliances")
    dims=pd.DataFrame({"Dimensió":["Economia","Ocupació i talent","Innovació i coneixement","Ecosistema"],"Actual":[70,73,80,84],"Target":[80,80,85,85]})
    l,r=st.columns([1,1.2])
    with l:
        section("Territorial return radar","Assoliment relatiu dels objectius")
        fig=go.Figure()
        fig.add_trace(go.Scatterpolar(r=dims.Actual,theta=dims.Dimensió,fill='toself',name='Actual'))
        fig.add_trace(go.Scatterpolar(r=dims.Target,theta=dims.Dimensió,name='Target'))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,100])),height=390,margin=dict(l=40,r=40,t=20,b=20),paper_bgcolor="white",legend_title="")
        st.plotly_chart(fig,use_container_width=True)
    with r:
        section("Evidence matrix","Traçabilitat del retorn per startup")
        ev=su[["Startup","Sector","Local_jobs","Local_pilots","Local_supplier","Alliances"]].copy()
        ev.columns=["Startup","Sector","Nous FTE locals","Pilots locals","Proveïdor local","Aliances"]
        st.dataframe(ev,hide_index=True,use_container_width=True,height=390)
    st.caption("No es construeix un índex sintètic únic de retorn: les dimensions es mantenen separades per evitar ponderacions arbitràries i preservar la traçabilitat.")

with tab5:
    section("Methodology & Data Governance","Com es transforma la Teoria del Canvi en informació per decidir")
    st.markdown("**TEORIA DEL CANVI → INDICADORS → DADES → MONITORATGE → ALERTA → ACCIÓ CORRECTORA → AVALUACIÓ → APRENENTATGE**")
    st.markdown("""
**5 nivells d'indicadors**  
1. **Execució:** tasques, fites, lliurables, pressupost, documentació i riscos.  
2. **Outputs:** productes directes de la intervenció.  
3. **Outcomes:** canvis observats en les startups.  
4. **Impacte:** canvis de major abast, interpretats amb prudència causal.  
5. **Retorn territorial:** economia, ocupació i talent, innovació i coneixement, ecosistema.

**Fitxa mínima de cada indicador:** definició · fórmula · baseline · target · font de verificació · periodicitat · responsable · llindar d'alerta quan correspongui.

**Governança:** qualitat i actualització de dades · traçabilitat · control d'accés · protecció de dades · supervisió humana. L'analítica predictiva només s'incorporaria amb una base històrica suficient, validació i explicabilitat.
""")
    st.info("Prototip funcional desenvolupat amb dades sintètiques exclusivament amb finalitat demostrativa. Els valors no representen resultats reals de Neàpolis.")
