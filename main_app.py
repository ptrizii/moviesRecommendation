import streamlit as st
import pandas as pd
import numpy as np
from st_files_connection import FilesConnection
from google.cloud import storage
import os
from recommendation import get_recommendations
import io

# Set the environment variable for Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

# Load data
data = pd.read_csv('data.csv')
client = storage.Client()
bucket = client.get_bucket("streamlitmovies-bucket")
blob = bucket.get_blob("embd-18-20k.npy")
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
        scores = []
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

def main():
    st.title('Movie Recommender System')

    movie_list = data['title'][18000:20000].values
    data_copy = data.loc[18000:20000].reset_index()

    selected_index = st.selectbox("Type and select your favorite movie", range(len(movie_list)), format_func=lambda i: movie_list[i])
    selected_index = int(selected_index)

    if st.button("Show Recommendation"):

        # st.write(np_array[selected_index])
        st.write(selected_index)
        # st.write(film_recommendation)
        st.write(data_copy.loc[selected_index, 'title'])

        jac_scores = jaccard_similarity(selected_index, data_copy['genres'])
        cos_scores = cosine_similarity(np_array[selected_index], np_array)



        st.write(jac_scores[selected_index])
        st.write(cos_scores[selected_index])
        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.write("film")
            
            with st.container(border=True):
                st.write("film 2")

        with col2:
            with st.container(border=True):
                st.write("Film 1")

            with st.container(border=True):
                st.write("Film 2")

        st.snow()
    

# Run the Streamlit app
if __name__ == '__main__':
    main()
