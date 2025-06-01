# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize Your Smoothie !")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name of your smoothie will be:", name_on_order)

ingredients_list = st.multiselect(
    "Choose up to 5 Ingredient?",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    
    ingredients_string = ''

    for ingredient in ingredients_list:
        ingredients_string += ingredient + ' '
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
        sf_dt = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered '+ name_on_order +'!', icon="✅")

