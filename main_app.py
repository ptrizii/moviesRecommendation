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

    movie_list = data['Title'].values

    selected_movie = st.selectbox("Type or select movie", movie_list)

    if st.button("Show Recommendation"):
        st.write("Here is your recommendation")