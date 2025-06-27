# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f"Cuztomize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the smoothie you want in your Custom Smoothie!
  """
)

name_of_smoothie = st.text_input('Smoothie name:')
st.write('The name of your smoothie is ', name_of_smoothie)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
   "Choose up to 5 ingridients:",
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''
  
    for i in ingredients_list:
        ingredients_string += i + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        st.subheader(i + ' Nutrition information:')
        st_df = st.dataframe(smoothiefroot_response.json(), use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(NAME_ON_ORDER, ingredients)
            values ('""" + name_of_smoothie +"""','""" + ingredients_string + """')"""
    #st.write(my_insert_stmt)

    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered, {name_of_smoothie}!', icon="✅")
