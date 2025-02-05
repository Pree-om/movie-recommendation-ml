import streamlit as st
import pandas as pd
import pickle
import requests  # to hit API


def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=f3d34ed7fcbcd0f6e585329cff4fd781&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]  # fetching index of movie
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[
                 1:6]  # fetching top 5 similar movies
    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].get('movie_id')  # Safe get for movie_id
        if movie_id:  # Proceed only if movie_id exists
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))  # rb: read binary
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender')

selected_movie_name = st.selectbox("Select Movie", movies['title'].values)

if st.button('Recommend Movie(s)'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

    # Updated to use `st.columns()` instead of `st.beta_columns()`
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
