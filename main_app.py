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

    movies_list = data['Title'].values

    selected_movie = st.selectbox("Select or type your favorite movie", movies_list)

    if st.button("Show Recommendation"):
        st.write("Here is your recommendation")
    else:
        st.write("Please choose a movie first")


# Run the Streamlit app
if __name__ == '__main__':
    main()
