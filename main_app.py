import streamlit as st
import pandas as pd 
import numpy as np 

# Read data
data = pd.read_csv('data.csv')
column_name = ['Title', 'genres', 'year', 'overview']

# Add title
st.title('Movies Recommendation System')

# Add search bar for movies
search_term = st.text_input('Enter your favorite film title:')

# Display the result
# Button for executing the search
if st.button('Search'):
    # Filter data based on the search term
    result = data[data['title_query'].str.contains(search_term, case=False)]

#     # Display search results
#     st.write('Search Results:')
#     st.table(result[column_name])

st.write('Search Results:')
for index, row in result.iterrows():
    button_label = row['Title']
    if st.button(button_label):
        st.write(f"You clicked the button for {button_label}")