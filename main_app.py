import streamlit as st
import pandas as pd

# Read data
data = pd.read_csv('data.csv')

# Function to recommend movies based on the movie id


def recommend_movies(movie_id):
    # Replace this with your actual recommendation logic
    st.write(f"Recommendations for movie with ID {movie_id}")

# Streamlit app


def main():
    st.title('Movie Recommender System')

    # Add search bar for movies
    search_term = st.text_input('Enter the movie title:')

    movie_list = data['title'].values

    selected_movies = st.selectbox("Find", movie_list)


# Run the Streamlit app
if __name__ == '__main__':
    main()
