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
    # Check if 'Title' is in the columns
    if 'title' in data.columns:
        # Filter data based on the search term
        result = data[data['title_query'].str.contains(search_term, case=False)]
    else:
        st.write('Error: The column "Title" does not exist in the DataFrame.')

# Display search results as buttons
if not result.empty:
    st.write('Search Results:')
    for index, row in result.iterrows():
        # Display the title
        st.write(f"# {row['title']}")

        # Display the genres below the title
        st.write(f"Genres: {row['genres']}")
        st.write(f"Released year: {row['year']}")

        # Add a button
        if st.button(f"Find recommendation for {row['title']}"):
            # You can add more actions or details for the selected movie
            st.write(f"Additional details for {row['title']}")
else:
    st.write('No results found.')
