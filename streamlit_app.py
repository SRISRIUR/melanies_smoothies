# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# App title
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw: {st.__version__}")
st.write("Choose the fruits you want in your custom Smoothie")

# User input
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

# Snowflake connection and fruit options
cnx = st.connection("snowflake")
session = cnx.session()
fruit_df = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).collect()
fruit_list = [row['FRUIT_NAME'] for row in fruit_df]

# Multiselect
ingredients_list = st.multiselect("Choose up to 5 ingredients", fruit_list, max_selections=5)

# When user selects fruits
if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)
    st.write("Your Smoothie Ingredients:", ingredients_string)

    if name_on_order:
        my_insert_stmt = f"""
            INSERT INTO smoothies.public.orders (ingredients, name_on_order)
            VALUES ('{ingredients_string}', '{name_on_order}')
        """
        time_to_insert = st.button('Submit Order')
        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            st.success('Your Smoothie is ordered!', icon="✅")

# New Section: External API call
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
