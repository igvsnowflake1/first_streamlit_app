import streamlit
import pandas as pd
import requests
import snowflake.connector

# Set the page title
streamlit.set_page_config(page_title='Healthy Dinner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Let's put a pick list here so they can pick the fruit they want to include 
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
# Fruits selected
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)

fruityvice_normalized = pd.json_normalize(fruityvice_response.json()) 
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()

# Execute a query on the fruit load list
my_cur.execute("SELECT * from fruit_load_list")

# Fetch all rows from the result set
my_data_rows = my_cur.fetchall()

streamlit.header("Añadir una Nueva Fruta")

new_fruit = streamlit.text_input('Introduce una nueva fruta:')
if new_fruit:
    streamlit.write('Has introducido:', new_fruit)
    # Insert the new fruit into the database
    my_cur.execute("INSERT INTO fruit_load_list (fruit_name) VALUES (%s)", (new_fruit,))
    # Commit the transaction to persist changes
    my_cnx.commit()

streamlit.header("The fruit load list contains:")
# Display all rows from the result set
streamlit.dataframe(my_data_rows)
