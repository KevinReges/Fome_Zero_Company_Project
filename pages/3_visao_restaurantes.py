import pandas as pd
import numpy as np
import streamlit as st
import folium
from streamlit_folium import folium_static
import plotly.express as px
from PIL import Image


df = pd.read_csv('dataset/zomato.csv')
df1 = df.copy()


st.set_page_config( page_title='Restaurantes', page_icon='🍽️', layout='wide')

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

table = {0: "No", 1: "Yes"}

def disponibilidade(table_id):
    return table[table_id]

code = [0, 1]
for c in code:
    df1['Is_delivering'] = df1['Is_delivering_now'].apply(lambda x: disponibilidade(x))

#-----------------------------------------------------------------------------------

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

#--------------------------------------------------------------------------------------------------------

# Dataframe com melhores restaurantes por media de avaliação

def top_best_restaurants(df1):
    cols = ['Restaurant_id', 'Restaurant_name', 'Country', 'City', 'Cuisines',
            'Average_cost_for_two', 'Currency', 'Ratings', 'Votes']
    lines = (df1['Cuisines'].isin(cuisines)) & (df1['Country'].isin(countries))
    df2 = (df1.loc[lines, cols].
    sort_values(['Ratings', 'Restaurant_id'], ascending=[False, True]).reset_index())
    df2 = df2.head(top_n) 
        
    return df2

#---------------------------------------------------------------------------------------------------------

# Top piores restaurantes por media de avaliação.

def top_worst_restaurants(df1):
    
    cols = ['Restaurant_id', 'Restaurant_name', 'Country', 'City', 'Cuisines',
            'Average_cost_for_two', 'Currency', 'Ratings', 'Votes']
    lines = (df1['Cuisines'].isin(cuisines)) & (df1['Country'].isin(countries)) & (df1['Ratings'] > 0)
    df2 = (df1.loc[lines, cols].
    sort_values(['Ratings', 'Restaurant_id'], ascending=[True, True]).reset_index())
    df2 = df2.head(top_n) 
    
    return df2

#---------------------------------------------------------------------------------------------------------

# Top culinarias por avaliações médias. retorna grafico barras.

def top_cuisines_aval(df1, op):
    
    if op == False:
        
        lines = df1['Ratings'] > 4
        write = f'Top {top_n} culinárias melhores avaliações.'
        
    elif op == True:   
        
        lines = (df1['Ratings'] > 0) & (df1['Ratings'] < 3.5) 
        write = f'Top {top_n} culinárias piores avaliações.'
    
    cols = ['Cuisines', 'Ratings']    
    df2 = df1.loc[lines, cols].groupby('Cuisines').mean().sort_values('Ratings', ascending=op).reset_index()
    df2 = df2.head(top_n) 

    grafico = px.bar(df2.head(top_n), x='Cuisines', y='Ratings', text= 'Ratings', 
        text_auto= '.2f', 
        title= write,
        labels={'Cuisines': 'Culinárias', 'Ratings': 'Média de avaliação'})

    return grafico

#----------------------------------------------------------------------------------------------

def graph_bar_delivering(df1):
        
    cols = ['Restaurant_name', 'Is_delivering']
    df2 = df1.loc[:, cols].groupby('Is_delivering').nunique().reset_index()
    grafico = px.bar(df2, x='Is_delivering', y='Restaurant_name',
                    text= 'Restaurant_name',
                    labels={'Is_delivering': 'Serviço de Entrega', 'Restaurant_name': 'Total de Restaurantes'})
    return grafico


def graph_pie_delivering(df1):
    
    cols = ['Restaurant_name', 'Is_delivering']
    df2 = df1.loc[:, cols].groupby('Is_delivering').nunique().reset_index()
    df2['Quantidade_porcentagem'] = np.round((df2['Restaurant_name'] * 100) / df2['Restaurant_name'].sum(), 2)
    grafico = px.pie(df2, values='Quantidade_porcentagem', names='Is_delivering')
        
    return grafico
    
    
# =====================================================
#              Barra Lateral
# =====================================================



def make_sidebar(df1):
    
    # image_path = 'logo.png'
    image = Image.open('logo_fome_zero.png')
    st.sidebar.image(image, width=120)
    
    st.sidebar.markdown('# Fome Zero')
    st.sidebar.markdown('### Seu restaurante está aqui!')
    st.sidebar.markdown("# Restaurantes 🍽️")
    st.sidebar.markdown("""___""")
    st.sidebar.markdown("## Filtros")

    countries = st.sidebar.multiselect(
        "Países",
        df1.loc[:, 'Country'].unique().tolist(),
        default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"],
    )

    top_n = st.sidebar.slider(
        "Quantidade de Restaurantes", 1, 20, 10
    )

    cuisines = st.sidebar.multiselect(
        "Tipos de Culinária",
        df1.loc[:, 'Cuisines'].unique().tolist(),
        default=[
            "Home-made",
            "BBQ",
            "Japanese",
            "Brazilian",
            "Arabian",
            "American",
            "Italian",
        ],
    )
    

    return list(countries), top_n, list(cuisines)


countries, top_n, cuisines = make_sidebar(df1)

st.sidebar.markdown("""___""")
st.sidebar.markdown('### Powered by Kevin Reges')


# =====================================================
#              Layout no Streamilit
# =====================================================



st.title('Visão Restaurantes')



with st.container():
        
    st.markdown("""___""")
    st.markdown(f'##### Top {top_n} melhores restaurantes')
    df3 = top_best_restaurants(df1)
    st.dataframe(df3)
    
   
       
    
    
with st.container():
        
    st.markdown("""___""")
    st.markdown(f'##### Top {top_n} piores restaurantes.')
    
    df3 = top_worst_restaurants(df1) 
    st.dataframe(df3)
    
    
with st.container():
    
    st.markdown("""___""")
    
    col1, col2 = st.columns(2)
    
    with col1:
        
        grafico = top_cuisines_aval(df1, op = False)
        st.plotly_chart(grafico, use_container_width=True)
        
    
    with col2:
        
        grafico = top_cuisines_aval(df1, op = True)
        st.plotly_chart(grafico, use_container_width=True)    
        
 
with st.container():
    
    st.markdown("""___""")
    col1, col2 = st.columns(2)
    
    with col1:
        
        st.markdown('##### Proporção de restaurantes por serviço de entregas')
        grafico = graph_pie_delivering(df1)
        st.plotly_chart(grafico, use_container_width=True)
        
    with col2:
        
        st.markdown('##### Total restaurantes por serviço de entregas.')
        grafico = graph_bar_delivering(df1)
        st.plotly_chart(grafico, use_container_width=True)
    
