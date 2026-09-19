import streamlit as st, pandas as pd, numpy as np, plotly.graph_objects as go
from pathlib import Path
from datetime import date
import io
st.set_page_config(page_title='NEÀPOLIS IMPACT',page_icon='◉',layout='wide',initial_sidebar_state='collapsed')
BASE=Path(__file__).parent/'dades'
TABLES=['Projectes','Inputs','Activitats','Objectius','Outputs','Outcomes','Impactes','Hipòtesis','Retorn territorial','WorkPackages','Deliverables','Milestones','Tasks','Economics','Startups','Riscos']
@st.cache_data
def load_demo(): return {n:pd.read_csv(BASE/f'{n}.csv') for n in TABLES}
if 'dades' not in st.session_state: st.session_state.dades=load_demo(); st.session_state.mode='DEMO · DADES FICTÍCIES'
if 'nav' not in st.session_state: st.session_state.nav='HOME'
D=st.session_state.dades

def dt(df,*cols):
 d=df.copy()
 for c in cols:
  if c in d: d[c]=pd.to_datetime(d[c],errors='coerce')
 return d

def money(x):
 try:return f'{float(x):,.0f} €'.replace(',','.')
 except:return '—'
def pct(v): return f'{100*v:.0f}%'
def gohome(): st.session_state.nav='HOME'; st.rerun()
def goto(x): st.session_state.nav=x; st.rerun()
def card(title,value,desc,delta=''):
 st.markdown(f'''<div class="kpi"><div class="kt">{title}</div><div class="kv">{value}</div>{f'<div class="kd">{delta}</div>' if delta else ''}<div class="kx">{desc}</div></div>''',unsafe_allow_html=True)
def section(t,s=''): st.markdown(f'<div class="sect"><h2>{t}</h2><p>{s}</p></div>',unsafe_allow_html=True)
def filtered(name,pid,asof=None):
 d=D[name].copy(); d=d[d.Id_projecte==pid] if 'Id_projecte' in d else d
 if asof:
  for c in ['Data_mesura','Data_disponibilitat','Data_fi_prevista','Data_prevista','Data_obertura']:
   if c in d.columns:
    d[c]=pd.to_datetime(d[c],errors='coerce'); d=d[(d[c].isna())|(d[c]<=pd.Timestamp(asof))]; break
 return d

def derive(pid,asof):
 cut=pd.Timestamp(asof)
 dl=dt(filtered('Deliverables',pid),'Data_prevista','Data_real'); dl['Pes_percent']=pd.to_numeric(dl.Pes_percent,errors='coerce').fillna(0)
 dl['Planificat']=dl.Data_prevista<=cut; dl['Real']=dl.Data_real.notna()&(dl.Data_real<=cut); dl['Vençut']=dl.Planificat&~dl.Real
 agg=dl.groupby('Id_WP').apply(lambda g:pd.Series({'plan':(g.Pes_percent*g.Planificat).sum()/max(g.Pes_percent.sum(),1),'real':(g.Pes_percent*g.Real).sum()/max(g.Pes_percent.sum(),1),'vençuts':int(g.Vençut.sum())}),include_groups=False).reset_index()
 wp=filtered('WorkPackages',pid).merge(agg,on='Id_WP',how='left').fillna({'plan':0,'real':0,'vençuts':0}); wp['gap']=(wp.plan-wp.real).clip(lower=0)
 eco=dt(filtered('Economics',pid),'Data_inici_elegibilitat','Data_fi_elegibilitat'); eco=eco[eco.Data_inici_elegibilitat<=cut];
 for c in ['Pressupost_planificat','Import_compromès','Import_pagat','Factura_o_justificant','Evidència_activitat']: eco[c]=pd.to_numeric(eco[c],errors='coerce').fillna(0)
 r=dt(filtered('Riscos',pid),'Data_obertura','Data_tancament'); r['obert']=(r.Data_obertura<=cut)&(r.Data_tancament.isna()| (r.Data_tancament>cut))
 openr=int(r.obert.sum()); docs=int(((eco.Factura_o_justificant==0)|(eco.Evidència_activitat==0)).sum())
 schedule=float(wp.gap.mean()) if len(wp) else 0; overdue=int(wp.vençuts.sum())
 budget_plan=float(eco.Pressupost_planificat.sum()); paid=float(eco.Import_pagat.sum()); committed=float(eco.Import_compromès.sum())
 budget_pressure=max(0,(committed/max(budget_plan,1))-.85)
 risk=min(100,round(45*min(schedule/.25,1)+20*min(overdue/4,1)+15*min(openr/4,1)+12*min(docs/5,1)+8*min(budget_pressure/.15,1)))
 status='ALT' if risk>=70 else ('MODERAT' if risk>=40 else 'CONTROLAT')
 return wp,dl,eco,r,dict(risk=risk,status=status,plan=float(wp.plan.mean()) if len(wp) else 0,real=float(wp.real.mean()) if len(wp) else 0,overdue=overdue,openr=openr,docs=docs,budget=paid/max(budget_plan,1),paid=paid,committed=committed,budget_plan=budget_plan)

st.markdown('''<style>
.stApp{background:#f4f7fb;color:#10283d}.block-container{padding-top:1.1rem;max-width:1450px}.hero{background:linear-gradient(125deg,#071b2d,#103a53 65%,#0a6672);border-radius:24px;padding:28px 34px;color:white;margin:8px 0 18px;box-shadow:0 12px 35px #0b233326}.hero h1{font-size:42px;margin:3px 0}.hero p{font-size:17px;color:#d8e8ef;margin:0}.badge{font-size:11px;font-weight:800;letter-spacing:.13em;background:#ffffff17;border:1px solid #ffffff33;padding:6px 10px;border-radius:999px}.eyebrow{font-size:11px;letter-spacing:.16em;font-weight:800;color:#74d6de;margin-top:15px}.kpi{background:white;border:1px solid #dce7ef;border-radius:18px;padding:17px 18px;min-height:145px;box-shadow:0 4px 16px #16384d0c}.kt{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:#597286;font-weight:800}.kv{font-size:28px;font-weight:850;color:#0b2c43;margin:7px 0}.kd{font-size:12px;font-weight:800;color:#0d7b86}.kx{font-size:12px;color:#667d8d;line-height:1.35;margin-top:7px}.sect{margin:25px 0 10px}.sect h2{margin:0;color:#0b2c43;font-size:23px}.sect p{margin:4px 0;color:#6b7e8c}.risk{background:#081c2d;border-radius:20px;padding:22px;color:white;min-height:218px}.lights{display:flex;gap:11px;margin:18px 0}.light{width:32px;height:32px;border-radius:50%;opacity:.18}.on{opacity:1;box-shadow:0 0 20px currentColor}.rtitle{font-size:28px;font-weight:900}.rsub{font-size:12px;color:#bdd0dd;margin-top:8px;line-height:1.45}.projectname{font-size:18px;font-weight:850;color:#fff;margin-top:8px}.navbox{background:white;border:1px solid #dce7ef;border-radius:16px;padding:15px;margin-bottom:7px}.smallnote{font-size:12px;color:#6b7e8c}.stButton>button{border-radius:12px;font-weight:750;border:1px solid #cbdde8}.stButton>button:hover{border-color:#0a7f89;color:#0a6872}.dataframe{border-radius:14px}.call{background:#eaf7f7;border-left:4px solid #0a7f89;padding:14px 16px;border-radius:10px;color:#234a5a}
</style>''',unsafe_allow_html=True)
# permanent home navigation button
h1,h2=st.columns([1,8]);
with h1:
 if st.button('⌂  INICI',use_container_width=True): gohome()
st.markdown(f'''<div class="hero"><span class="badge">{st.session_state.mode}</span><div class="eyebrow">PROJECT & IMPACT INTELLIGENCE SYSTEM</div><h1>NEÀPOLIS IMPACT</h1><p>Control, anticipació i impacte en una sola vista: de l’execució calendaritzada a les decisions, els resultats i el retorn territorial.</p></div>''',unsafe_allow_html=True)
# compatible filters
proj=D['Projectes']; pmap=dict(zip(proj.Nom_projecte,proj.Id_projecte)); c1,c2,c3=st.columns([1.5,1,1.3])
with c1: pname=st.selectbox('Projecte',proj.Nom_projecte.tolist(),index=0); pid=pmap[pname]
with c2: asof=st.date_input('Data d’anàlisi',value=date.today(),min_value=date(2023,6,1),max_value=date(2028,4,30))
startup_options=['Totes']+D['Startups'].loc[D['Startups'].Id_projecte==pid,'Nom_startup'].tolist()
with c3: startup=st.selectbox('Startup',startup_options)
wp,dl,eco,risks,K=derive(pid,asof)
# navigation helpers
TDC=['Inputs','Activitats','Outputs','Outcomes','Impactes','Hipòtesis','Retorn territorial']

if st.session_state.nav=='HOME':
 section('Quadre de comandaments',f'Visualització de dades a {pd.Timestamp(asof).strftime("%d/%m/%Y")}.')
 left,right=st.columns([1.05,2.35])
 with left:
  color={'ALT':'#ef4444','MODERAT':'#f59e0b','CONTROLAT':'#22c55e'}[K['status']]
  st.markdown(f'''<div class="risk"><div class="smallnote" style="color:#9fc1d1">PROJECTE SELECCIONAT</div><div class="projectname">{pname}</div><div class="lights"><div class="light {'on' if K['status']=='CONTROLAT' else ''}" style="background:#22c55e;color:#22c55e"></div><div class="light {'on' if K['status']=='MODERAT' else ''}" style="background:#f59e0b;color:#f59e0b"></div><div class="light {'on' if K['status']=='ALT' else ''}" style="background:#ef4444;color:#ef4444"></div></div><div class="rtitle" style="color:{color}">RISC {K['status']} · {K['risk']}/100</div><div class="rsub">Índex explicable de priorització. Integra desviació temporal, lliurables vençuts, riscos oberts, evidències pendents i pressió pressupostària. No és una probabilitat.</div></div>''',unsafe_allow_html=True)
 with right:
  if startup=='Totes':
   o=filtered('Objectius',pid,asof); cols=st.columns(3)
   for i in range(3):
    if i<len(o):
     r=o.iloc[i]; val=f"{r.Valor_actual:g} / {r.Valor_objectiu:g}"; desc=f"{r.Indicador_clau}. Mesura l'avenç de l'objectiu {r.Id_objectiu}: {r.Objectiu}."
     with cols[i]: card(f'Objectiu {r.Id_objectiu}',val,desc)
   cols=st.columns(3)
   with cols[0]: card('Progrés real',pct(K['real']),"Proporció ponderada de lliurables completats fins a la data d’anàlisi.",f"Planificat {pct(K['plan'])}")
   with cols[1]: card('Execució pressupostària',pct(K['budget']),"Import pagat respecte del pressupost planificat registrat al sistema.",money(K['paid']))
   with cols[2]: card('Control documental',str(K['docs']),"Moviments econòmics amb factura/justificant o evidència d’activitat pendent.",'pendències')
  else:
   s=D['Startups'][(D['Startups'].Id_projecte==pid)&(D['Startups'].Nom_startup==startup)].iloc[0]; cols=st.columns(3)
   with cols[0]: card('Capacitats',f"{s['Índex_capacitats_actual']}/100",'Evolució de capacitats empresarials respecte de la línia de base.',f"T0 {s['Índex_capacitats_T0']}/100")
   with cols[1]: card('Nous clients',int(s.Nous_clients),'Nous clients o oportunitats comercials atribuïdes al període de seguiment.')
   with cols[2]: card('Inversió captada',money(s.Inversió_captada_EUR),'Capital privat mobilitzat per la startup durant el seguiment.')
   cols=st.columns(3)
   with cols[0]: card('Ocupació actual',int(s.Ocupació_actual),'Llocs de treball actuals declarats per la startup.',f"T0 {int(s.Ocupació_T0)}")
   with cols[1]: card('Outcome clau',s.Outcome_clau,'Canvi esperat de curt/mitjà termini vinculat a la participació de la startup.')
   with cols[2]: card('Retorn territorial',s.Retorn_territorial_clau,'Dimensió de valor local que es vol verificar i seguir.')
 section('Teoria del Canvi','Selecciona una dimensió per obrir els seus indicadors de seguiment i control.')
 cc=st.columns(4)
 for i,x in enumerate(TDC):
  with cc[i%4]:
   if st.button(x,use_container_width=True,key='tdc'+x): goto(x)
 if startup=='Totes':
  section('Trajectòria del projecte','Progrés planificat vs progrés real calculat a partir dels lliurables i les seves dates.')
  p=proj[proj.Id_projecte==pid].iloc[0]; start=pd.to_datetime(p.Data_inici); end=min(pd.Timestamp(asof),pd.to_datetime(p.Data_fi)); dates=list(pd.date_range(start,end,freq='MS'))+[pd.Timestamp(asof)]; hist=[]
  for dte in sorted(set(dates)):
   _,_,_,_,kk=derive(pid,dte.date()); hist.append([dte,100*kk['plan'],100*kk['real']])
  hh=pd.DataFrame(hist,columns=['Data','Planificat','Real']); fig=go.Figure(); fig.add_trace(go.Scatter(x=hh.Data,y=hh.Planificat,name='Planificat',mode='lines')); fig.add_trace(go.Scatter(x=hh.Data,y=hh.Real,name='Real',mode='lines+markers')); fig.update_layout(height=330,margin=dict(l=10,r=10,t=15,b=10),yaxis_title='Progrés %',legend_orientation='h'); st.plotly_chart(fig,use_container_width=True)
 else:
  section('Evolució de la startup','Comparació entre línia de base i situació actual dels indicadors de capacitat i ocupació.')
  s=D['Startups'][(D['Startups'].Id_projecte==pid)&(D['Startups'].Nom_startup==startup)].iloc[0]
  f=go.Figure(); f.add_trace(go.Bar(name='T0',x=['Capacitats','Ocupació'],y=[s['Índex_capacitats_T0'],s.Ocupació_T0])); f.add_trace(go.Bar(name='Actual',x=['Capacitats','Ocupació'],y=[s['Índex_capacitats_actual'],s.Ocupació_actual])); f.update_layout(barmode='group',height=330,margin=dict(l=10,r=10,t=15,b=10)); st.plotly_chart(f,use_container_width=True)
 section('Accés ràpid','Selecciona l’opció d’anàlisi que desitges visualitzar.')
 quick=[('Seguiment del projecte','Calendari, WP, lliurables, fites i tasques.'),('Resultats en startups','Última mesura disponible per startup.'),('Analítica predictiva','Semàfor, causes, escenaris i accions correctores.'),('Data Hub','Visualitza, filtra, carrega i descarrega les taules de dades.'),('Metodologia','Regles de càlcul, governança i traçabilitat.')]
 cols=st.columns(5)
 for i,(a,b) in enumerate(quick):
  with cols[i]:
   st.markdown(f'<div class="navbox"><b>{a}</b><div class="smallnote">{b}</div></div>',unsafe_allow_html=True)
   if st.button('Obrir →',key='q'+a,use_container_width=True): goto(a)

elif st.session_state.nav in TDC:
 name=st.session_state.nav; section(name,f'Lectura gerencial de {name.lower()} per al projecte seleccionat.')
 df=filtered(name,pid,asof)
 if startup!='Totes':
  s=D['Startups'][(D['Startups'].Id_projecte==pid)&(D['Startups'].Nom_startup==startup)].iloc[0]
  field={'Inputs':'Input_clau','Outputs':'Output_clau','Outcomes':'Outcome_clau','Impactes':'Impacte_clau','Hipòtesis':'Hipòtesi_clau','Retorn territorial':'Retorn_territorial_clau'}.get(name)
  if field: st.markdown(f'<div class="call"><b>{startup}</b><br>{s[field]}</div>',unsafe_allow_html=True)
 if name in ['Outputs','Outcomes','Impactes','Retorn territorial'] and len(df):
  val='Valor_actual'; tar='Valor_objectiu'; label=[c for c in df.columns if c in ['Output','Outcome','Impacte','Indicador_retorn']][0]
  plot=df[[label,val,tar]].copy(); fig=go.Figure(); fig.add_trace(go.Bar(name='Actual',x=plot[label],y=plot[val])); fig.add_trace(go.Bar(name='Objectiu',x=plot[label],y=plot[tar])); fig.update_layout(barmode='group',height=390,margin=dict(l=10,r=10,t=20,b=120)); st.plotly_chart(fig,use_container_width=True)
 elif name=='Inputs' and len(df):
  fig=go.Figure(go.Bar(x=df.Quantitat,y=df.Input,orientation='h')); fig.update_layout(height=380,margin=dict(l=10,r=10,t=20,b=10)); st.plotly_chart(fig,use_container_width=True)
 elif name=='Activitats' and len(df):
  fig=go.Figure(); fig.add_trace(go.Bar(name='Assolit',x=df.Activitat,y=df.Valor_assolit)); fig.add_trace(go.Bar(name='Objectiu',x=df.Activitat,y=df.Valor_objectiu)); fig.update_layout(barmode='group',height=380,margin=dict(l=10,r=10,t=20,b=100)); st.plotly_chart(fig,use_container_width=True)
 elif name=='Hipòtesis' and len(df):
  fig=go.Figure(go.Scatter(x=df.Probabilitat_1_5,y=df.Impacte_1_5,mode='markers+text',text=df.Id_hipòtesi,textposition='top center',marker_size=22)); fig.update_layout(xaxis_title='Probabilitat',yaxis_title='Impacte',xaxis_range=[0.5,5.5],yaxis_range=[0.5,5.5],height=360); st.plotly_chart(fig,use_container_width=True)
 st.dataframe(df,use_container_width=True,hide_index=True)

elif st.session_state.nav=='Seguiment del projecte':
 section('Seguiment del projecte','Calendari, Work Packages, lliurables, fites i tasques calculats a la data seleccionada.')
 c=st.columns(4)
 with c[0]: card('Progrés planificat',pct(K['plan']),'Percentatge ponderat que hauria d’estar completat segons calendari.')
 with c[1]: card('Progrés real',pct(K['real']),'Percentatge ponderat efectivament completat a la data d’anàlisi.')
 with c[2]: card('Lliurables vençuts',K['overdue'],'Lliurables amb data prevista superada i sense finalització registrada.')
 with c[3]: card('Hores planificades',int(pd.to_numeric(filtered('Tasks',pid).Hores_planificades).sum()),'Càrrega total planificada de les tasques del projecte.')
 tabs=st.tabs(['WorkPackages','Deliverables','Milestones','Tasks','Economics'])
 for tab,n in zip(tabs,['WorkPackages','Deliverables','Milestones','Tasks','Economics']):
  with tab: st.dataframe(filtered(n,pid),use_container_width=True,hide_index=True)

elif st.session_state.nav=='Resultats en startups':
 section('Resultats en startups','Seguiment individual de capacitats, mercat, inversió, ocupació i retorn territorial.')
 df=filtered('Startups',pid); st.dataframe(df,use_container_width=True,hide_index=True)

elif st.session_state.nav=='Analítica predictiva':
 section('Analítica predictiva','Models de priorització i escenaris de risc. En aquesta fase són models explicables basats en regles i tendències; no es presenten com a probabilitats de machine learning.')
 # multiple explainable predictive models
 models=[('Risc de calendari',min(100,round(100*min(max(K['plan']-K['real'],0)/.25,1))), 'Desviació entre trajectòria planificada i real.'),('Pressió pressupostària',min(100,round(100*max(0,K['committed']/max(K['budget_plan'],1)-.70)/.30)), 'Compromisos acumulats respecte del pressupost disponible.'),('Risc documental',min(100,K['docs']*20),'Evidències o justificants pendents que poden comprometre el tancament.'),('Risc de governança',min(100,K['openr']*22),'Riscos oberts i necessitat d’accions correctores.'),('Risc d’objectius',0,'Distància dels objectius clau respecte dels seus targets.')]
 o=filtered('Objectius',pid); ratios=[]
 for _,r in o.iterrows(): ratios.append(float(r.Valor_actual)/max(float(r.Valor_objectiu),1))
 models[-1]=(models[-1][0],round(100*(1-min(ratios))) if ratios else 0,models[-1][2])
 cols=st.columns(len(models))
 for i,(n,v,d) in enumerate(models):
  with cols[i]: card(n,f'{v}/100',d)
 section('Causes i accions correctores','Priorització dels riscos oberts, responsables i resposta prevista.')
 rr=filtered('Riscos',pid); st.dataframe(rr,use_container_width=True,hide_index=True)
 st.markdown('<div class="call"><b>Evolució futura:</b> amb històric suficient es poden incorporar models de supervivència/retard, regressió per desviació pressupostària, classificació de risc documental, forecasting de resultats i models de propensió per startups, sempre amb validació, explicabilitat i supervisió humana.</div>',unsafe_allow_html=True)

elif st.session_state.nav=='Data Hub':
 section('Data Hub','Les taules són la font del sistema. Visualitza-les, descarrega-les o carrega un Excel/CSV per substituir dades durant la sessió.')
 st.markdown('### Visualització de taules')
 name=st.selectbox('Taula de dades',TABLES,index=0); df=D[name]
 st.dataframe(df,use_container_width=True,hide_index=True,height=440)
 st.download_button(f'Descarregar {name}.csv',df.to_csv(index=False).encode('utf-8-sig'),file_name=f'{name}.csv',mime='text/csv',use_container_width=True)
 st.markdown('### Carrega de dades')
 up=st.file_uploader('Carrega un Excel (.xlsx) amb fulls homònims o un CSV per actualitzar la taula seleccionada',type=['xlsx','csv'])
 if up:
  try:
   if up.name.lower().endswith('.csv'): st.session_state.dades[name]=pd.read_csv(up)
   else:
    x=pd.ExcelFile(up)
    for sh in x.sheet_names:
     if sh in TABLES: st.session_state.dades[sh]=pd.read_excel(up,sheet_name=sh)
   st.session_state.mode='DADES CARREGADES · SESSIÓ'; st.success('Dades carregades.'); st.rerun()
  except Exception as e: st.error(f'No s’han pogut carregar les dades: {e}')
 if st.button('Restablir dades fictícies'): st.session_state.dades=load_demo(); st.session_state.mode='DEMO · DADES FICTÍCIES'; st.rerun()

elif st.session_state.nav=='Metodologia':
 section('Metodologia','Regles de càlcul, governança, traçabilitat i límits interpretatius.')
 st.markdown('''<div class="call"><b>Cadena de valor:</b> Inputs → Activitats → Outputs → Outcomes → Impactes → Retorn territorial.<br><br><b>Execució temporal:</b> el progrés es calcula a partir de lliurables ponderats i dates previstes/reals; no s’introdueix manualment.<br><br><b>Early warning:</b> els scores són índexs de priorització explicables, no probabilitats. La decisió final correspon a l’equip responsable.<br><br><b>Traçabilitat:</b> les dades públiques verificades s’identifiquen a Projectes; la resta del prototip és fictícia amb finalitat demostrativa.</div>''',unsafe_allow_html=True)
 st.markdown('### Fonts públiques utilitzades')
 for _,r in D['Projectes'].iterrows(): st.markdown(f"**{r.Nom_projecte}:** {r.Font_publica}")
