# Import python packages
import streamlit as st


# Write directly to the app
st.title(f" :cup_with_straw: Customize your smoothie :cup_with_straw: ")
st.write(
  """choose the fruit you want in your custom smoothie
  """
)

name_on_order = st.text_input("Name on smoothie:")
st.write("The name on the smoothie will be : ",name_on_order )

from snowflake.snowpark.functions import col 
 
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


# ✅ Convert to Pandas (THIS LINE WAS MISSING)
df = my_dataframe.to_pandas()

# Multiselect widget
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    df["FRUIT_NAME"].tolist()
    ,max_selections=5
)
if len(ingredients_list) > 5:
    st.error("You can select up to 5 ingredients only!")

if ingredients_list:

    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
       ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_list)

    my_insert_stmt = """ 
    INSERT INTO smoothies.public.orders (ingredients,name_on_order)
    VALUES ('""" + ingredients_string + """','""" + name_on_order + """')
"""
    #st.write(my_insert_stmt)
   # st.stop()

    
    time_to_insert=st.button('Sumbit Order')

    if time_to_insert and name_on_order:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,'+ name_on_order, icon="✅")

cnx = st.connection("Snowflake")
session = cnx.session()
