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
# if st.button('Search'):
#     # Filter data based on the search term
#     result = data[data['title_query'].str.contains(search_term, case=False)]

#     # Display search results
#     st.write('Search Results:')
#     st.table(result[column_name])


# Display the result
# Button for executing the search
if st.button('Search'):
    # Filter data based on the search term
    result = data[data['Title'].str.contains(search_term, case=False)]

# Display search results as buttons
if result is not None and not result.empty:
    st.write('Search Results:')
    for index, row in result.iterrows():
        button_label = f"{row['Title']} - {row['genres']}"
        if st.button(button_label):
            st.write(f"You clicked the button for {row['Title']}")
            # You can add more actions or details for the selected movie
else:
    st.write('No results found.')
