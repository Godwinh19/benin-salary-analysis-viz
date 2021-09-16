import streamlit as st
from gsheetsdb import connect
import pandas as pd
from preprocessing import DataCleaning
import plotly.express as px
import plotly.graph_objects as go
from texts import *
from unidecode import unidecode

conn = connect()


@st.cache(ttl=6000)
def run_query(query):
    rows = conn.execute(query, headers=1)
    return rows


sheet_url = st.secrets["public_gsheets_url"]
rows = run_query(f'SELECT * FROM "{sheet_url}"')
df = pd.DataFrame(data=rows)
df.dropna(inplace=True)

clean = DataCleaning(df)
data = clean.run

# STREAMLIT APP
st.sidebar.header("Analyse des métiers et des salaires en Informatique au Bénin.")
st.sidebar.markdown(ABOUT)
st.sidebar.write(LINK_TO_ARTICLE)
st.sidebar.info(CITATION)

st.header("Suivie des metiers dans le temps")
fig = px.scatter(data_frame=data, x='date', y='metiers', color='metiers',
              symbol='metiers'
              )
fig.update_layout(showlegend=False,
                  autosize=False,
                  margin=dict(autoexpand=False, l=150, r=0, t=0))
st.plotly_chart(fig)

st.header("Salaire des informaticiens au Bénin")
fig = go.Figure()
fig.add_trace(go.Histogram(x=data['salaire_debut'], name='Salaire au début'))
fig.add_trace(go.Histogram(x=data['salaire_actuel'], name='Salaire actuel'))
fig.layout.yaxis.title.text = f"Nombre d'informatien / {data.shape[0]}"
st.plotly_chart(fig)
salaire_expander = st.expander(label='Lire plus')
with salaire_expander:
    TEXT_SALAIRE

st.header("Les différentes postes en informatique au Bénin")
fig = go.Figure()
fig.add_trace(go.Histogram(y=data['metiers'], orientation='h'))
st.plotly_chart(fig)

st.header("Nombre d’années d’expérience des informaticiens au Bénin")
experience_expander = st.expander(label='Lire plus')
with experience_expander:
    TEXT_EXPERIENCE

fig = go.Figure()
fig.add_trace(go.Histogram(y=data['experience'], orientation='h'))
st.plotly_chart(fig)

satisfaction = pd.DataFrame(data['satisfaction'].value_counts())
st.header("Satisfaction des informaticiens par rapport à leur salaire")
fig = go.Figure()
fig.add_trace(go.Bar(y=satisfaction.satisfaction, orientation='v', marker=dict(color='green')))
fig.layout.yaxis.title.text = "Nombre d'informatien"
fig.layout.xaxis.title.text = "Satisfaction"
st.plotly_chart(fig)
st.markdown(TEXT_SATISFACTION)

st.header("Salaires moyens et satisfaction moyenne relativement aux metiers")
data = data[['salaire_debut', 'salaire_actuel', 'satisfaction', 'metiers']]
data['metiers_decode'] = data['metiers'].apply(lambda x: unidecode(x).lower())
df = data.groupby('metiers_decode').mean()
st.dataframe(df)