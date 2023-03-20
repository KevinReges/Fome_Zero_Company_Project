import pandas as pd
import numpy as np
import streamlit as st
import folium
from streamlit_folium import folium_static
import plotly.express as px
from PIL import Image

st.set_page_config( page_title='Home', page_icon='🎲')

df = pd.read_csv('dataset/zomato.csv')
df1 = df.copy()



# Renomear as colunas

df1 = df1.rename(columns={'Aggregate rating': 'Ratings'})
df1 = df1.rename(columns={'Has Online delivery': 'Online_delivery'})
df1 = df1.rename(columns={'Has Table booking': 'Table_booking'})
df1 = df1.rename(columns={'Restaurant ID': 'Restaurant_id'})
df1 = df1.rename(columns={'Restaurant Name': 'Restaurant_name'})
df1 = df1.rename(columns={'Average Cost for two': 'Average_cost_for_two'})
df1 = df1.rename(columns={'Is delivering now': 'Is_delivering_now'})
df1 = df1.rename(columns={'Price range': 'Price_range'})
df1 = df1.rename(columns={'Rating text': 'Rating_text'})


# Preenchimento dos nomes dos países

countries = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

def country_name(country_id):
  return countries[country_id]

# Criando coluna Country com nome dos paises

code = [1, 14, 30, 37, 94, 148, 162, 166, 184, 189, 191, 208, 214, 215, 216]
for i in code:
  df1['Country'] = df1['Country Code'].apply(lambda x: country_name(x)) 

#------------------------------------------------------------------------------------   

# Criação nome das cores

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "yellow",
}
def color_name(color_code):
  return COLORS[color_code]

code = ["3F7E00", "5BA829", "9ACD32", "CDD614", "FFBA00", "CBCBC8", "FF7800"]
for i in code:
  df1['Colors'] = df1['Rating color'].apply(lambda x: color_name(x))  

#----------------------------------------------------------------------------------

# Diponibilidade 0 -> No 1 -> Yes

table = {0: "No", 
         1: "Yes"}
def disponibilidade(table_id):
  return table[table_id]

code = [0, 1]
for c in code:
  
  df1['Is_delivering'] = df1['Is_delivering_now'].apply(lambda x: disponibilidade(x))

#-----------------------------------------------------------------------------------------------  

# Removendo colunas

df1 = df1.drop(columns=['Country Code'])
df1 = df1.drop(columns=['Switch to order menu'])
df1 = df1.drop(columns=['Rating color'])

# reajustastando coluna Cuisines para 1 tipo de culinaria 

df1["Cuisines"] = df1.loc[:, "Cuisines"].astype(str).apply(lambda x: x.split(",")[0])



# Ordenação de posições das colunas

df1 = df1[['Restaurant_id', 'Restaurant_name', 'Country', 'City', 'Address', 'Locality',
           'Locality Verbose', 'Longitude', 'Latitude', 'Cuisines', 'Currency', 'Average_cost_for_two', 
           'Table_booking', 'Online_delivery', 'Is_delivering',
           'Price_range', 'Ratings', 'Colors', 'Rating_text', 'Votes']]  



# =====================================================
#              Layout no Streamilit
# =====================================================

image = Image.open('logo_fome_zero.png')
st.image(image, width=120)
st.title(":orange[Fome Zero]")
st.markdown("#### :**green[Procurando um novo restaurante?]**")


with st.container():
    
    st.markdown('### Aqui você encontra:')
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        qtd_countries = len(df1.loc[:, 'Country'].unique())
        col1.metric('Total de Países', qtd_countries)
    
    with col2:
        qtd_citys = len(df1.loc[:, 'City'].unique())
        col2.metric('Total de Cidades', qtd_citys)
        
    with col3:
        qtd_restaurants = len(df1.loc[:, 'Restaurant_name'].unique())
        col3.metric('Total de Restaurantes', qtd_restaurants)    
    
    with col4:
        qtd_culinarias = len(df1.loc[:, 'Cuisines'].unique())
        col4.metric('Culinarias diferentes', qtd_culinarias)
        
    with col5:
        qtd_aval = df1.loc[:, 'Votes'].sum()
        col5.metric('Total de Avaliações', qtd_aval) 
        

with st.container():
    
    st.markdown('## Mapa')
    
    cols = ['Longitude', 'Latitude', 'Restaurant_name', 'Average_cost_for_two',   'Ratings', 'Currency', 'Colors', 'City']
    data_plot = df1.loc[:, cols].sample(100)

    map = folium.Map()

    for index, location_info in data_plot.iterrows():
        folium.Marker( [location_info['Latitude'], location_info['Longitude']], 
                popup=location_info[['Restaurant_name', 'Average_cost_for_two',  'Ratings', 'Currency', 'City']],
        icon=folium.Icon(color=location_info['Colors'])).add_to(map)

    folium_static(map, width=1024, height=600)  
