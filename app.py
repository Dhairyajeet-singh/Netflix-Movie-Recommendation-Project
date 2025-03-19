import streamlit as st
import pickle
import pandas as pd
import requests
from dotenv import load_dotenv
import os
import gzip

with gzip.open("similarity.pkl.gz", "rb") as f:
    similarity = pickle.load(f)  

load_dotenv()  
api = os.getenv("api_key")

st.title('Movie Recommender System')
st.write('Welcome to the Movie Recommender System!')

movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

options = st.selectbox('Select a movie', movies['title'].values)

def fetch(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api}&language=en-US')  
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]  
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        poster.append(fetch(movie_id))
    return recommend_movies, poster

st.markdown(
    """
    <style>
    .scroll-container {
        display: flex;
        overflow-x: auto;
        padding: 10px;
        gap: 20px;
    }
    .movie-item {
        min-width: 150px;
        text-align: center;
    }
    .movie-title {
        font-size: 14px;
        font-weight: bold;
        white-space: nowrap;
    }
    img {
        width: 150px;
        height: auto;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Recommend button
if st.button('Recommend'):
    names, posters = recommend(options)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.header(names[0])
        st.image(posters[0])
    with col2:
        st.header(names[1])
        st.image(posters[1])
    with col3:
        st.header(names[2])
        st.image(posters[2])
    with col4:
        st.header(names[3])
        st.image(posters[3])
    with col5:
        st.header(names[4])
        st.image(posters[4])
