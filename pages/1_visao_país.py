import pandas as pd
import numpy as np
import streamlit as st
import folium
from streamlit_folium import folium_static
import plotly.express as px
from PIL import Image

df = pd.read_csv('dataset/zomato.csv')
df1 = df.copy()

st.set_page_config( page_title='País', page_icon='🌏', layout='wide')

#----------------------------------------------------------------------------------------------

# quantidades de valores coluna por país

def qtd_by_country(df1, column):
    
    """
        Função para calcular quantidade de valores em determinada coluna 
        por país.
        Resultado mostrado em um grafico de barras ordenado por país.
        
        _ df1: Nome do dataframe.
        
        - Column: Nome da coluna a ser dada.
            Ex: 'Restaurant Name'
    """
    
    if column == 'Restaurant_name':
        cols = ['Country', column]
        df2 = df1.loc[:, cols].groupby('Country').nunique().sort_values(column, ascending=False).reset_index()
        grafico = px.bar(df2, x='Country', y=column, text=column,
                         title = 'Quantidade de restaurantes por país.',
                         labels={f'Country': 'Países', 'Restaurant_name': 'Quantidade de restaurantes'},
                         color='Country')

        return grafico
    
    elif column == 'City':
        cols = ['Country', column]
        df2 = df1.loc[:, cols].groupby('Country').nunique().sort_values(column, ascending=False).reset_index()
        grafico = px.bar(df2, x='Country', y=column, text=column,
                         title='Quantidade de cidades por país.',  
                         labels={f'Country': 'Países', 'City': 'Quantidade de cidades'}, 
                         color='Country', text_auto=False)

        return grafico
        

#----------------------------------------------------------------------------------------------------

def avg_by_country(df1, column):
    
    """
        Função para calcular media de valores em determinada coluna 
        por país.
        Resultado mostrado em um grafico de barras ordenado por país.
        
        _ df1: Nome do dataframe.
        
        - Column: Nome da coluna a ser dada.
            Ex: 'Votes'
    """
    
    if column == 'Ratings':
        cols = ['Country', column]
        df2 = df1.loc[:, cols].groupby('Country').mean().sort_values(column, ascending=False).reset_index()
        grafico = px.bar(df2, x='Country', y=column, text=column,
                         text_auto='.2f',
                         labels= {'Country': 'Países', 'Ratings': 'Média avaliações'})

        return grafico

    elif column == 'Average_cost_for_two':
        
        cols = ['Country', 'Currency',column]
        lines = df1[column] < 10000
        df2 = df1.loc[lines, cols].groupby(['Country', 'Currency']).mean().sort_values(column, ascending=False).reset_index()
        grafico = px.bar(df2, x='Country', y=column, text=column,
                         text_auto='.2f',
                         labels= {'Country': 'Países', 'Average_cost_for_two': 'Média preço'})
        
        return grafico

#-------------------------------------------------------------------------------------------------------------------

# Grafico barras mostrando quantidade de restaurantes por país que fazem ou não entregas.

def restaurants_deliveries(df1, op):
    
    if op == True:
        
        lines = (df1['Is_delivering'] == 'Yes')  
        write = 'Quantidade de restaurantes que fazem entregas.'
        
    elif op == False:
        
        lines = (df1['Is_delivering'] == 'No') & (df1['Country'].isin(country_options))
        write = 'Quantidade de restaurantes que não fazem entregas.'
        
    cols = ['Restaurant_name', 'Country']
    df2 = ( df1.loc[lines, cols].groupby(['Country'])
                                .nunique()
                                .sort_values('Restaurant_name', ascending=False)
                                .reset_index() )

    grafico = px.bar(df2, x='Country', y='Restaurant_name', 
                        labels={'Country': 'Países', 'Restaurant_name': 'Quantidade de restaurantes'},
                        title = write,
                        color='Country', text_auto=True)
        
    return grafico

#---------------------------------------------------------------------------------------------------------------------
# Diponibilidade 0 -> No 1 -> Yes

table = {0: "No", 
         1: "Yes"}
def disponibilidade(table_id):
    return table[table_id]

code = [0, 1]
for c in code:
  
  df1['Is_delivering'] = df1['Is_delivering_now'].apply(lambda x: disponibilidade(x))
        
#---------------------------------------------------------------------------------------------------------------------


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
#              Barra Lateral
# =====================================================



# image_path = 'logo.png'
image = Image.open('logo_fome_zero.png')
st.sidebar.image(image, width=120)

st.sidebar.markdown('# :orange[Fome Zero]')
st.sidebar.markdown('### :green[Seu restaurante está aqui!]')
st.sidebar.markdown("# País 🌏")
st.sidebar.markdown("""___""")

st.sidebar.markdown("## Filtros")

country_options = st.sidebar.multiselect(
    'Countries',
    ['Philippines', 'Brazil', 'Australia', 'United States of America',
     'Canada', 'Singapure', 'United Arab Emirates', 'India', 'Indonesia', 
     'New Zeland', 'England', 'Qatar', 'South Africa', 'Sri Lanka', 'Turkey'],
    default = ['Brazil', 'India', 'United States of America', 'Australia', 'Philippines', 'Qatar'] )

# Filtro por transito
select_lines = df1['Country'].isin(country_options)
df1 = df1.loc[select_lines, :]

st.sidebar.markdown("""___""")
st.sidebar.markdown('### Powered by Kevin Reges')




# =====================================================
#              Layout no Streamilit
# =====================================================

st.title('Visão País')
    
with st.container():
        
    grafico = qtd_by_country(df1, 'City')
    st.plotly_chart(grafico, use_container_with=True)

    
with st.container():
    
    st.markdown("""___""")
    grafico = qtd_by_country(df1, 'Restaurant_name')
    st.plotly_chart(grafico, use_container_width=True)
    
        
with st.container():
    
    st.markdown("""___""")
    col1, col2 = st.columns(2)
    
    with col1:
        
        st.markdown('##### Média avalaliações')
        grafico = avg_by_country(df1, 'Ratings')
        st.plotly_chart(grafico, use_container_width=True)
        
        
    with col2:
        
        st.markdown('##### Média preço duas pessoas.')
        
        grafico = avg_by_country(df1, 'Average_cost_for_two')
        st.plotly_chart(grafico, use_container_width=True)
        
        
with st.container(): 
    
    
    
    st.markdown("""___""")
    
    col1, col2 = st.columns(2)
    
    with col1:
        
        grafico = restaurants_deliveries(df1, op=True)
        st.plotly_chart(grafico, use_container_width=True)

        
    with col2:
        
        grafico = restaurants_deliveries(df1, op=False)
        st.plotly_chart(grafico, use_container_width=True)


    
