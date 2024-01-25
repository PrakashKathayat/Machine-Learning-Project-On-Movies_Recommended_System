import streamlit as st
import pickle
import pandas as pd
import requests


MAX_RETRIES = 3

def fetch_poster(movie_id):
    for _ in range(MAX_RETRIES):
        try:
            response = requests.get(
                'https://api.themoviedb.org/3/movie/' +
                '{}?api_key=bad7e46723cb0b3bb4305e2f633703a5'.format(movie_id)
            )
            response.raise_for_status()
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return "https://image.tmdb.org/t/p/w500/" + poster_path
            else:
                st.warning("No poster found for the selected movie.")
                return None
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching poster: {e}")
    return None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.markdown("<h1 style='box-shadow: 5px 5px 5px #888888;'>Movie Recommender System</h1>", unsafe_allow_html=True)


selectbox_style = """
    <style>
        .st-eb {
            width: 300px; /* Adjust the width as needed */
            background-color: #f0f8ff; /* Light Blue background color */
            color: #4682b4; /* Blue font color */
            font-weight: bold;
            border-radius: 8px; /* Rounded corners */
            border: 2px solid #4682b4; /* Border color */
            padding: 8px; /* Padding */
        }
    </style>
"""

# Apply the styling
st.markdown(selectbox_style, unsafe_allow_html=True)

# Use the selectbox
selected_movie_name = st.selectbox('How May I Help You??', movies['title'].values, key="movie_selectbox")

if st.button('Recommend'):
    names, posters =recommend(selected_movie_name)

    for i in range(5):
        if posters[i] is not None:
            st.header(names[i])
            st.image(posters[i])
        else:
            st.warning(f"No poster found for {names[i]}")
