#Instrucitons for notebook
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from PIL import Image

# %%
@st.cache
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/lucasdanielgeo/analise-carregamento-app/master/data/carregamento_faixa_ponto_criticas.csv")
    return df
df = load_data()
df = df.sort_values(by=['faixa'])
to_time = pd.to_datetime(df.faixa,format='%H').dt.time[0:]
faixa_to_hora = pd.DataFrame({'faixa_time': to_time})
df = df.join(faixa_to_hora)

df.groupby('id_pc').agg({'sum_faixa_estu':'sum', 'sum_faixa_estu':'mean','sum_faixa':'mean'})

print(df)
#read_and_cahe_csv = st.cache(pd.read_csv)
#df = read_and_cahe_csv('C:/Users/Luis/Documents/Documents/IPUF_Trabalhos/Projeto Análise Ocupação/1605_analises_python/carregamento_faixa_ponto_criticas.csv')
#df = pd.read_csv()


image = Image.open("C:/Users/GEOIPUF/Desktop/Logo_pmf.jpg")
st.image(image,  use_column_width=True)
# %%
st.markdown("## **Dados da pesquisa DUT 2019 🚌**")
st.markdown("Esta aplicação é um painel de informações, que pode ser usado para explorar dados "
            "sobre a pesquisa de carregamento em dias úteis realizada no final de 2019 - ** DUT 2019 ** 🚍")
st.markdown("** Estatisticas gerais 🚍**")
st.markdown("* Abaixo, pode ser explorado um panorama dos dados obtidos nos pontos de controle, como, carregamento, ocupação e descidas "
            "das linhas, pontos com mais carregamento por faixa de horário e o mapa dos pontos de controle.")
st.markdown("◀️◀️◀️ Use a barra lateral para realizar filtros sobre os dados")


# %%

#create sidebar
st.sidebar.title('Filtro de dados')


#Filtro gráfico 1

faixa_list = st.sidebar.selectbox("Selecione a faixa de horário: ", df["faixa_time"].unique())

data =  px.data.gapminder()
data_faixa = df[df.faixa_time == faixa_list]


#Filtro gráfico 2
s = df["faixa_time"].unique()
dados_select = st.sidebar.multiselect('Selecione uma ou mais faixas de horário: ', s)  ## pensar em como colocar o defaul int
mask = df['faixa_time'].isin(dados_select)
data_mask = df[mask]


# %%
st.markdown("### ** Mapa dos pontos de controle**")
map_fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="id_pc", hover_data=["faixa_time", "n partidas"],
                        color_discrete_sequence=["fuchsia"], zoom=8, height=300)


map_fig.update_layout(mapbox_style="open-street-map")
map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


# map_fig.update_layout(
#     mapbox_style="white-bg",
#     mapbox_layers=[
#         {
#             "below": 'traces',
#             "sourcetype": "raster",
#             "source": [
#                 "http://a.tile.openstreetmap.fr/hot/${z}/${x}/${y}"
#             ]
#         }        
#       ])
# map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.write(map_fig,use_collumn_width=True)


filter_field = df["faixa_time"]



# %% Gráfico 1
#FIltro único
chart_1 = px.bar(data_faixa, x='id_pc', y='sum_faixa_estu', title= f'Carregamento nos pontos na faixa  {faixa_list}', 
            color= 'corredor', hover_data=['sum_faixa_estu','numero linha'], 
            labels={'sum_faixa_estu':'Soma de carregamento', 'id_pc':'Ponto de controle'}, text='sum_faixa_estu' )



chart_1.update_traces(texttemplate='%{text:.2s}', textposition= 'outside')
chart_1.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', barmode='stack')
#chart_1.update_xaxes(tickangle=-90)
#, xaxis=dict(title='id_pc',tickmode='linear'
st.plotly_chart(chart_1, use_container_width=True)

# %% Gráfico 2
# Filtro por tags

chart_2 = px.bar(data_mask, x='id_pc', y='sum_faixa_estu', title='Carregamento nos pontos por faixa', 
            hover_data=['sum_faixa_estu','numero linha'],
            labels={'sum_faixa_estu':'Soma de carregamento', 'id_pc':'Ponto de controle'}, height=500, text='sum_faixa_estu')

chart_2.update_traces(texttemplate='%{text:.2s}', textposition= 'outside')
chart_2.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', barmode='stack')

st.plotly_chart(chart_2, use_container_width=True)


# %% Mostrar tabela

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