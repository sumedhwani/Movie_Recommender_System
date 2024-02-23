import streamlit as st
import pickle
import pandas as pd
import requests
similarity = pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a371a28030e636d8e571155bc73b81e5&language=en-US'.format(movie_id))
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommeded_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch poster from api
        recommended_movies.append(movies.iloc[i[0]].title)
        recommeded_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommeded_movies_poster
movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)


st.title("Movie Recommender System")
selected_movie_name = st.selectbox('Which Movie',movies['title'].values)

if st.button('Recommend similar movie mate'):
    names,poster = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(poster[0])
    with col2:
        st.text(names[1])
        st.image(poster[1])

    with col3:
        st.text(names[2])
        st.image(poster[2])
    with col4:
        st.text(names[3])
        st.image(poster[3])
    with col5:
        st.text(names[4])
        st.image(poster[4])

