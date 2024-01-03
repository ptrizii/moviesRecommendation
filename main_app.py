import streamlit as st
import pandas as pd
import numpy as np
from st_files_connection import FilesConnection
from google.cloud import storage
import os
import io

# Set the environment variable for Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

# Load data
data = pd.read_csv('data.csv')
client = storage.Client()
bucket = client.get_bucket("streamlitmovies-bucket")
blob = bucket.get_blob("embd-9-10k.npy")
# Download the content of the blob as bytes
blob_content = blob.download_as_bytes()
# # Convert the content to a NumPy array
np_array = np.load(io.BytesIO(blob_content))


def jaccard_score(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0


def jaccard_similarity(index, genre):
    # Split genres and convert into list
    genre_set = genre.apply(lambda x: set(x.split(', '))).to_list()
    jaccard_similarities = []
    set1 = genre_set[index]

    for i in range(len(genre_set)):
        set2 = genre_set[i]
        score = jaccard_score(set1, set2)
        jaccard_similarities.append(score)

    jaccard_similarities = np.array(jaccard_similarities)
    return jaccard_similarities


def cosine_score(embd1, embd2):
    dot_product = np.dot(embd1, embd2)
    norm_vec1 = np.linalg.norm(embd1)
    norm_vec2 = np.linalg.norm(embd2)
    # Calculate cosim score
    cosim_score = dot_product / (norm_vec1 * norm_vec2)
    return cosim_score


def cosine_similarity(embd_query, embedding):
    scores = []
    for i in range(len(embedding)):
        score = cosine_score(embd_query, embedding[i])
        scores.append(score)

    scores = np.array(scores)
    return scores


def weight_similarity(query_index, embedding, genres):
    # Define weight for each similarity
    w_jac = 0.3
    w_cos = 0.7

    # Calculate jaccard scores
    jaccard_scores = jaccard_similarity(query_index, genres)
    # Initialize an array to store the cosine scores
    cosine_scores = np.zeros_like(jaccard_scores)

    # Check if Jaccard score is not zero, then calculate cosine scores
    non_zero_jaccard_indices = np.nonzero(jaccard_scores)
    if len(non_zero_jaccard_indices[0]) > 0:
        non_zero_indices = non_zero_jaccard_indices[0]
        # Calculate cosine scores for non-zero Jaccard scores
        cosine_scores[non_zero_indices] = cosine_similarity(
            embedding[query_index], embedding[non_zero_indices])

    # calculate weighted similarity
    weigted_jaccard = jaccard_scores*w_jac
    weighted_cosine = cosine_scores*w_cos

    similarity_scores = weigted_jaccard + weighted_cosine

    return similarity_scores


def get_recommendations(query_index, data, embedding, k=10):
    # query_index = query_title
    data_sorted = data.copy()
    # calculated weighted sim
    similarity_scores = weight_similarity(query_index, embedding, data['genres'])
    data_sorted['similarity'] = similarity_scores
    data_sorted['short_overview'] = data_sorted['overview'].apply(lambda x: ' '.join(x.split()[:15]))
    # # # sorted the list
    data_sorted = data_sorted.sort_values(by='similarity', ascending=False)

    return data_sorted[1:k+1].reset_index()

def main():
    st.title('Movie Recommender System')

    movie_list = data['title'][9000:9999].values
    data_copy = data.loc[9000:9999].reset_index()

    selected_index = st.selectbox("Type and select your favorite movie", range(len(movie_list)), format_func=lambda i: movie_list[i])
    selected_index = int(selected_index)

    if st.button("Show Recommendation"):

        # st.write(np_array[selected_index])
        st.write(selected_index)
        # st.write(film_recommendation)
        st.write(data_copy.loc[selected_index, 'title'])
     
        film_recommendation = get_recommendations(selected_index, data_copy, np_array)
        st.write(film_recommendation)
        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.write(f"<h4 style='text-align: center;'>1. {film_recommendation.loc[0, 'title']}</h4>", unsafe_allow_html=True)
                st.write(f"Genre: {film_recommendation.loc[0, 'genres']}")
                st.write(film_recommendation.loc[0, 'short_overview'])

            with st.container(border=True):
                st.write(
                    f"<h4 style='text-align: center;'>3. {film_recommendation.loc[2, 'title']}</h4>", unsafe_allow_html=True)
                st.write(f"Genre: {film_recommendation.loc[2, 'genres']}")
                st.write(film_recommendation.loc[2, 'short_overview'])

            with st.container(border=True):
                st.write(
                    f"<h4 style='text-align: center;'>5. {film_recommendation.loc[4, 'title']}</h4>", unsafe_allow_html=True)
                st.write(f"Genre: {film_recommendation.loc[4, 'genres']}")
                st.write(film_recommendation.loc[4, 'short_overview'])

            with st.container(border=True):
                st.write(
                    f"<h4 style='text-align: center;'>7. {film_recommendation.loc[6, 'title']}</h4>", unsafe_allow_html=True)
                st.write(f"Genre: {film_recommendation.loc[6, 'genres']}")
                st.write(film_recommendation.loc[6, 'short_overview'])

            with st.container(border=True):
                st.write(
                    f"<h4 style='text-align: center;'>9. {film_recommendation.loc[8, 'title']}</h4>", unsafe_allow_html=True)
                st.write(f"Genre: {film_recommendation.loc[8, 'genres']}")
                st.write(film_recommendation.loc[8, 'short_overview'])

        with col2:
            with st.container(border=True):
                st.write(
                    f"<h4 style='text-align: center;'>2. {film_recommendation.loc[1, 'title']}</h4>", unsafe_allow_html=True)
                st.write(f"Genre: {film_recommendation.loc[1, 'genres']}")
                st.write(film_recommendation.loc[1, 'short_overview'])

            with st.container(border=True):
                st.write(
                    f"<h4 style='text-align: center;'>4. {film_recommendation.loc[3, 'title']}</h4>", unsafe_allow_html=True)
                st.write(f"Genre: {film_recommendation.loc[3, 'genres']}")
                st.write(film_recommendation.loc[3, 'short_overview'])

            with st.container(border=True):
                st.write(
                    f"<h4 style='text-align: center;'>6. {film_recommendation.loc[5, 'title']}</h4>", unsafe_allow_html=True)
                st.write(f"Genre: {film_recommendation.loc[5, 'genres']}")
                st.write(film_recommendation.loc[5, 'short_overview'])

            with st.container(border=True):
                st.write(
                    f"<h4 style='text-align: center;'>8. {film_recommendation.loc[7, 'title']}</h4>", unsafe_allow_html=True)
                st.write(f"Genre: {film_recommendation.loc[7, 'genres']}")
                st.write(film_recommendation.loc[7, 'short_overview'])

            with st.container(border=True):
                st.write(
                    f"<h4 style='text-align: center;'>10. {film_recommendation.loc[9, 'title']}</h4>", unsafe_allow_html=True)
                st.write(f"Genre: {film_recommendation.loc[9, 'genres']}")
                st.write(film_recommendation.loc[9, 'short_overview'])
        st.snow()
    

# Run the Streamlit app
if __name__ == '__main__':
    main()
