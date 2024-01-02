import streamlit as st
import pandas as pd
import numpy as np
from st_files_connection import FilesConnection
from google.cloud import storage

# Function to fetch NPY data from Google Cloud Storage


def read_npy_data_from_gcs(bucket_name, file_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    data = blob.download_as_bytes()
    np_array = np.load(io.BytesIO(data))
    return np_array

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
# conn = st.connection('gcs', type=FilesConnection)
# npy_bytes = conn.read("streamlitmovies-bucket/complete-embd.npy", ttl=600)
# Use numpy to load the bytes as an array
# embd = np.load(BytesIO(npy_bytes))
data = pd.read_csv('data.csv')

def main():
    st.title('Movie Recommender System')

    movie_list = data['title'].values

    selected_movies = st.selectbox("Type and select your favorite movie", movie_list)

    if st.button("Show Recommendation"):
        st.write("Here is your recommendation")
    
    st.write("HI")

    # Streamlit app code
    st.title("Google Cloud Data in Streamlit")

    # Define Google Cloud Storage details
    gcs_bucket_name = "streamlitmovies-bucket"
    gcs_file_name = "complete-embd.npy"

    # Fetch NPY data from Google Cloud Storage
    npy_data = read_npy_data_from_gcs(gcs_bucket_name, gcs_file_name)

    # Display NPY data in Streamlit
    st.write("### Data from Google Cloud Storage (NPY)")
    st.write(npy_data[0])

# Run the Streamlit app
if __name__ == '__main__':
    main()
