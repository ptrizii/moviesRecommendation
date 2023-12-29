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

    # Display the result
    if st.button('Search'):
        # Filter data based on the search term
        result = data[data['title'].str.contains(search_term, case=False)]

        if not result.empty:
            st.write('Search Results:')
            for index, row in result.iterrows():
                # Display the title, genres, and year
                st.write(f"# {row['title']}")
                st.write(f"Genres: {row['genres']}")
                st.write(f"Released year: {row['year']}")

                # Add a button with a unique label and pass the id to the recommend function
                if st.button(f"Recommend for {row['title']} (ID: {row['id']})"):
                    recommend_movies(row['id'])

            st.success("Movies found!")
        else:
            st.warning("The movie doesn't exist.")


# Run the Streamlit app
if __name__ == '__main__':
    main()
