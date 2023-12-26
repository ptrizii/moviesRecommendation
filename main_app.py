import streamlit as st
import pandas as pd

# Read data
data = pd.read_csv('data.csv')
columns_to_display = ['title', 'genres']
result = pd.DataFrame()  # Initialize result as an empty DataFrame

# Define a function to print something based on the film index


def print_something(index):
    st.write(f"Function called for film with Index: {index}")


# Add title
st.title('Movies Recommendation System')

# Add search bar for movies
search_term = st.text_input('Enter your favorite film title:')

# Display the result
# Button for executing the search
if st.button('Search'):
    # Check if 'title' is in the columns
    if 'title' in data.columns:
        # Filter data based on the search term
        result = data[data['title'].str.contains(search_term, case=False)]
    else:
        st.write('Error: The column "title" does not exist in the DataFrame.')

# Display search results as buttons
if not result.empty:
    st.write('Search Results:')
    for index, row in result.iterrows():
        # Display the title
        st.write(f"# {row['title']}")

        # Display the genres below the title
        st.write(f"Genres: {row['genres']}")
        st.write(f"Released year: {row['year']}")

        # Add a button with a unique label
        button_label = f"Find recommendation for {row['title']} (Index: {index})"
        if st.button(button_label):
            # Call the function with the film index
            print_something(index)
            # You can add more actions or details for the selected movie using the index
else:
    st.write('No results found.')
