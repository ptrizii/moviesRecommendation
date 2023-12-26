import streamlit as st
import pandas as pd

# Read data
data = pd.read_csv('data.csv')
columns_to_display = ['Title', 'genres']
result = pd.DataFrame()  # Initialize result as an empty DataFrame

# Add title
st.title('Movies Recommendation System')

# Add search bar for movies
search_term = st.text_input('Enter your favorite film title:')

# Display the result
# Button for executing the search
if st.button('Search'):
    # Filter data based on the search term
    result = data[data['Title'].str.contains(search_term, case=False)]

# Display search results as buttons
if not result.empty:
    st.write('Search Results:')
    for index, row in result.iterrows():
        button_label = f"{row['Title']} - {row['genres']}"
        if st.button(button_label):
            st.write(f"You clicked the button for {row['Title']}")
            # You can add more actions or details for the selected movie
else:
    st.write('No results found.')
