import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from st_files_connection import FilesConnection

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.connection('gcs', type=FilesConnection)
npy_bytes = conn.read("streamlitmovies-bucket/complete-embd.npy", input_format="npy", ttl=600)
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


# Run the Streamlit app
if __name__ == '__main__':
    main()
