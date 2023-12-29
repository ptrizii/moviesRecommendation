import streamlit as st
import pandas as pd
import os
import gcsfs
import numpy as np
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'key.json'


# Connect to the bucket
fs = gcsfs.GCSFileSystem(project='solid-league-409409')

# Open the file
embd = np.load('gs://streamlitmovies-bucket/complete-embd.npy', allow_pickle=True)
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
