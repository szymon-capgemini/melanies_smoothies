# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize your smoothie :cup_with_straw:")
st.write('Choose the fruits you want')

name_on_order = st.text_input('Name on smoothie:')
st.write(f'The name on your smoothie will be: {name_on_order}')

cnx = st.connection('snowflake')
session = cnx.session()
my_dataframe = session \
    .table("smoothies.public.fruit_options") \
    .select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose 5 fruits", 
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    
    # st.write(ingredients_string)
    
    my_insert_stmt = f"insert into smoothies.public.orders(ingredients, name_on_order) values ('{ingredients_string}', '{name_on_order}')"

    # st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered {name_on_order}!', icon="✅")
