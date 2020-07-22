#Instrucitons for notebook
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pydeck as pdk
# %%
@st.cache
def load_data():
    df = pd.read_csv("C:/Users/223136/Desktop/carregamento_faixa_ponto_criticas.csv")
    return df
df = load_data()
df = df.sort_values(by=['faixa'])
to_time = pd.to_datetime(df.faixa,format='%H').dt.time[0:]
faixa_to_hora = pd.DataFrame({'faixa_time': to_time})
df = df.join(faixa_to_hora)

#read_and_cahe_csv = st.cache(pd.read_csv)
#df = read_and_cahe_csv('C:/Users/Luis/Documents/Documents/IPUF_Trabalhos/Projeto Análise Ocupação/1605_analises_python/carregamento_faixa_ponto_criticas.csv')
#df = pd.read_csv()

# %%
st.markdown("## **🎲 Dados da pesquisa DUT 2019**")
st.markdown("Esta aplicação é um painel de informações, que pode ser usado para explorar dados "
            "sobre a pesquisa de carregamento em dias úteis realizada no final de 2019 - ** DUT 2019 **")
st.markdown("**♟ Estatisticas gerais ♟**")
st.markdown("* Isto dá um panorama dos pontos de controle, como, carregamento, ocupação e descidas "
            "das linhas, pontos com mais carregamento por faixa de horário, mapas dos pontos de controle.")

# %%

#create sidebar
st.sidebar.title("Filtro de dados")

# %%

filter_field = df["faixa_time"]

# %%
faixa_list = st.sidebar.selectbox("Selecione a faixa de horário: ", df["faixa_time"].unique())

data =  px.data.gapminder()
data_faixa = df[df.faixa_time == faixa_list]

#sorted_val = data_faixa.sort_values(by=['id_pc'])

#atitlebar = 'Carregamento nos pontos na faixa '+data_faixa
#data_faixa2 = data_faixa.id_pc.sort()

fig = px.bar(data_faixa, x='id_pc', y='sum_faixa_estu', title= f'Carregamento nos pontos na faixa  {faixa_list}', 
            color= 'corredor', hover_data=['sum_faixa_estu','numero linha'], 
            labels={'sum_faixa_estu':'Soma de carregamento', 'id_pc':'Ponto de controle'}, text='sum_faixa_estu' )



fig.update_traces(texttemplate='%{text:.2s}', textposition= 'outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', barmode='stack')
#fig.update_xaxes(tickangle=-90)
st.write(fig)


# Filtro por tags
s = df["faixa_time"].unique()
dados_select = st.sidebar.multiselect('Selecione uma ou mais faixas de horário: ', s)  ## pensar em como colocar o defaul int
mask = df['faixa_time'].isin(dados_select)
data_mask = df[mask]



fig1 = px.bar(data_mask, x='id_pc', y='sum_faixa_estu', title='Carregamento nos pontos por faixa', 
            hover_data=['sum_faixa_estu','numero linha'],
            labels={'sum_faixa_estu':'Soma de carregamento', 'id_pc':'Ponto de controle'}, height=500, text='sum_faixa_estu')

fig1.update_traces(texttemplate='%{text:.2s}', textposition= 'outside')
fig1.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', barmode='stack',xaxis=dict(title='id_pc',tickmode='linear'))

st.write(fig1)


fig_map = px.scatter_geo(data_faixa, lat='lat', lon='lon', size='sum_faixa_estu', hover_name='id_pc', projection='mercator', animation_frame='faixa')

#st.write(fig_map)

def show_df():
    show_df = st.radio(
        "Mostrar tabela:",
        options=["Sim", "Não"])
    if show_df == 'Sim':
        rename_col = {"numero linha": "Cód. da linha", "faixa_time": "Faixa de horário", "n partidas": "Partidas","sum_faixa_estu":"Soma carreg."}
        st.write(df[['numero linha','faixa_time','n partidas', 'id_pc', 'corredor','sum_faixa_estu']].rename(columns=rename_col))
    else:
        pass

show_df()
################################################


UK_ACCIDENTS_DATA = (
    "C:/Users/223136/Desktop/carregamento_faixa_ponto_criticas.csv"
)
TEXT_COLOUR = {
    'Black': [0,0,0,255],
    'Red': [189,27,33,255],
    'Green': [0,121,63,255],
    'Gold': [210,160,30,255]
}

radius_scale=0.01
opacity=0.01
text_colour = TEXT_COLOUR.get('Black')
mapdata = df[['id_pc','sum_faixa_estu','lon', 'lat']]

layer = pdk.Layer(
    type='ScatterplotLayer',
    id='scatterplot-layer',
    data=mapdata,
    pickable=True,
    get_position=['lon', 'lat'],
    get_radius='sum_faixa_estu',
    radius_min_pixels=2*radius_scale,
    radius_max_pixels=3*radius_scale,
    get_fill_color='fill_color',
    get_line_color=[45,128,128,200],
    get_line_width=500,
    stroked=True,
    filled=True,
    opacity=opacity
)
text_layer = pdk.Layer(
    type='TextLayer',
    id='text-layer',
    data=mapdata,
    pickable=True,
    get_position=['lon', 'lat'],
    get_text='id_pc',
    get_color=text_colour,
    billboard=False,
    get_size=1,
    get_angle=0,
    get_text_anchor='middle',
    get_alignment_baseline='center'
)
# Set the viewport location
view_state = pdk.ViewState(
    longitude=-48.549580, latitude=-27.596910, zoom=10, min_zoom=5, max_zoom=15, pitch=40.5, bearing=-27.36
)
# Combined all of it and render a viewport
r = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"html": "<b>Id ponto:</b> {id_pc}", "style": {"color": "white"}},
)
st.pydeck_chart(r)
####################


import geopandas

gdf = geopandas.GeoDataFrame(
    df, geometry=geopandas.points_from_xy(df.lon, df.lat))
st.write(gdf.head())
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
ax = world[world.continent == 'South America'].plot(
    color='white', edgecolor='black')
gdf.plot(ax=ax, color='red')

st.pyplot()