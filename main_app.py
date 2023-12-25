import streamlit as st
import pandas as pd 
import numpy as np 

# Read data
data = pd.read_csv('data.csv')

# Add title
st.title('Movies Recommendation System')

# Add search bar for movies
search = search_term = st.text_input('Enter a name to search:')
