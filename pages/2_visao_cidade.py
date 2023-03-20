import pandas as pd
import numpy as np
import streamlit as st
import folium
from streamlit_folium import folium_static
import plotly.express as px
from PIL import Image

df = pd.read_csv('dataset/zomato.csv')
df1 = df.copy()

st.set_page_config( page_title='Cidade', page_icon='🌃', layout='wide')

#----------------------------------------------------------------------------------------------

# Grafico de barras ordenado por cidades com cores de seus respectivos países. Informa top cidades
# com maiores quantidades de detreminada coluna do dataframe.

def qtd_by_city_graph(df1, column): 
    
    """
        df1: Dataframe 
        column: Coluna selecionada para calcular valores. Ex: 'Restaurant ID'
        Função calcula quantidades de determinada coluna agrupado por países e cidades.
        Retorna grafico barras com os top cidades com maiores quantidades da coluna selecionada,
        com cores de seus respectivos países.
        
    """
    if column == 'Restaurant_name':
        write = f'Top {top_n} cidades maiores quantidades restaurantes.'
        
    elif column == 'Cuisines':
        write = f'Top {top_n} cidades com maiores quantidades de culinárias.'
    cols = ['Country', 'City', column]
    lines = (df1['Country'].isin(countries)) 
    df2 = df1.loc[lines, cols].groupby(['Country', 'City']).nunique().sort_values(column, ascending=False).reset_index()
    df2 = df2.head(top_n)

    grafico = px.bar(df2, x='City', y=column, 
                     title= write,
                     labels={'City': 'Cidades', column: 'Quantidade de restaurantes'},
           color= 'Country', text_auto=True)
    
    return grafico

#---------------------------------------------------------------------------------------------


def avg_aval_by_city_graph(df1, op):
    
    if op == 'max':
        
        lines = lines = (df1['Ratings'] > 4) & (df1['Country'].isin(countries))
        write = f'{top_n} Cidades com maiores quantidades restaurantes com avaliações acima da média.'
        
    elif op == 'min':
    
        lines = lines = ( df1['Ratings'] < 4 ) & (df1['Country'].isin(countries))
        write = f'{top_n} Cidades com maiores quantidades restaurantes com avaliações abaixo da média.'

    cols = ['City', 'Restaurant_name', 'Country']
    df2 = ( df1.loc[lines, cols].groupby(['Country', 'City'])
                                .nunique()
                                .sort_values('Restaurant_name', ascending=False)
                                .reset_index() )
    df2 = df2.head(top_n)

    grafico = px.bar(df2, x='City', y='Restaurant_name',
                     title = write,
                     labels={'City': 'Cidades', 'Restaurant_name': 'Quantidade de restaurantes'},
                     color='Country', text_auto=True)

    return grafico

  

#---------------------------------------------------------------------------------------------

# Dataframe informando quantidade de restaurantes que fazem ou não entregas.

def restaurantes_deliveries(df1, op):
    
    if op == True:
        
        lines = (df1['Is_delivering'] == 'Yes') 
        
    elif op == False:
        
        lines = ( (df1['Is_delivering'] == 'No') & (df1['Country'].isin(countries)) )

    cols = ['Restaurant_name', 'Country', 'City']
    df2 = ( df1.loc[lines, cols].groupby(['Country', 'City'])
                                .nunique()
                                .sort_values('Restaurant_name', ascending=False)
                                .reset_index() )
    df2 = df2.head(top_n)

    return df2


#-----------------------------------------------------------------------------------------------

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
#              Barra Lateral
# =====================================================


def make_sidebar(df1):
    
    # image_path = 'logo.png'
    image = Image.open('logo_fome_zero.png')
    st.sidebar.image(image, width=120)
    
    st.sidebar.markdown('# :orange[Fome Zero]')
    st.sidebar.markdown('### :green[Seu restaurante está aqui!]')
    st.sidebar.markdown("## Cidades 🌃")
    st.sidebar.markdown("""___""")
    st.sidebar.markdown("## Filtros")

    countries = st.sidebar.multiselect(
        "Países",
        df1.loc[:, 'Country'].unique().tolist(),
        default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"],
        
    )
    
    st.sidebar.markdown("""___""")
    top_n = st.sidebar.slider(
        "Quantidade de Cidades", 1, 50, 10
    )    
    
   
    return list(countries), top_n


countries, top_n = make_sidebar(df1)

st.sidebar.markdown("""___""")
st.sidebar.markdown('### Powered by Kevin Reges')




# =====================================================
#              Layout no Streamilit
# =====================================================


st.title('Visão Cidade')


with st.container():
    
    grafico = qtd_by_city_graph(df1, 'Restaurant_name')
    st.plotly_chart(grafico)

    
with st.container():
    
    st.markdown("""___""")
        
    grafico = avg_aval_by_city_graph(df1, 'max')
    st.plotly_chart(grafico, use_container_width=True)
        

with st.container():
    
    st.markdown("""___""")    
        
    grafico = avg_aval_by_city_graph(df1, 'min')
    st.plotly_chart(grafico, use_container_width=True)
        
        
with  st.container():
    
    st.markdown("""___""")
    
    grafico = qtd_by_city_graph(df1, 'Cuisines')
    st.plotly_chart(grafico)
    
    
with st.container(): 
    
    st.markdown("""___""")
    col1, col2 = st.columns(2)
   
    with col1:    
        
        st.markdown('##### :blue[Quantidade de restaurantes que fazem entregas]')
        df3= restaurantes_deliveries(df1, op=True)
        st.dataframe(df3, use_container_width=True)

        
    with col2:
        
        st.markdown('##### :red[Quantidade de restaurantes que não fazem entregas]')
        df3 = restaurantes_deliveries(df1, op=False)
        st.dataframe(df3, use_container_width=True)
    
