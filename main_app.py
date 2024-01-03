import streamlit as st
import pandas as pd
import numpy as np
from st_files_connection import FilesConnection
from google.cloud import storage
import os
from recommendation import get_recommendations

# Explicitly set the Google Cloud project ID
# project_id = "solid-league-409409"
# client = storage.Client(project=project_id)

# Set the environment variable for Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
# conn = st.connection('gcs', type=FilesConnection)
# df = conn.read("streamlitmovies-bucket/data.csv",
#                input_format="csv", ttl=600)
# Use numpy to load the bytes as an array
# embd = np.load(BytesIO(npy_bytes))
data = pd.read_csv('data.csv')

client = storage.Client()
bucket = client.get_bucket("streamlitmovies-bucket")
blob = bucket.get_blob("complete-embd.npy")

def main():
    st.title('Movie Recommender System')

    movie_list = data['title'].values

    selected_index = st.selectbox("Type and select your favorite movie", range(len(movie_list)), format_func=lambda i: movie_list[i])

    if st.button("Show Recommendation"):
        # film_recommendation = get_recommendations(selected_movies)

        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.write("Film 1")
            
            with st.container(border=True):
                st.write("Film 2")

        with col2:
            with st.container(border=True):
                st.write("Film 1")

            with st.container(border=True):
                st.write("Film 2")

        st.snow()
    

# Run the Streamlit app
if __name__ == '__main__':
    main()
