import streamlit as st
import pickle
import pandas as pd
import requests
import base64

st.set_page_config(page_title ="Movie Recommendation System",
                       page_icon='🎬',
                       layout='wide')

# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer:after{
#             content:'© Vansh Aggarwal';
#             display:block;
#             position:relative;
#             color:rgba(250, 250, 250, 0.4);
#             padding:5px;
#             top=3px;
#             }
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)



movies = pickle.load(open(r'C:\Users\aggva\OneDrive\Desktop\Movie-Recommendation-System-main\Movie-Recommendation-System-main\movies.pkl', 'rb'))
movies_list = pd.Series(movies.title.values)
similarity = pickle.load(open(r'C:\Users\aggva\OneDrive\Desktop\Movie-Recommendation-System-main\Movie-Recommendation-System-main\similarity.pkl', 'rb'))


def get_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=46021bb9e6da9b0b2e5a50dc4196528f'.format(movie_id))
    json_data = response.json()
    return "https://image.tmdb.org/t/p/w500"+json_data['poster_path']


def recommend(movie):
    index = movies_list[movies_list == movie].index.values[0]
    top5_movies = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    movies_posters = []
    for index, distance in top5_movies:
        recommended_movies.append(movies_list[index])
        movies_posters.append(get_poster(movies.id[index]))

    return recommended_movies, movies_posters


st.title("Movie Recommendation System")

movie_name = st.selectbox("Enter the Movie Name:",movies_list)

if st.button("Recommend"):
    with st.spinner('Finding Recommendations...'):
        st.subheader("Your Recommendations are:")
        recommendations, posters = recommend(movie_name)
        cols = st.columns(5)

        for i in range(5):
            with cols[i]:
                st.image(posters[i])
                st.subheader(recommendations[i])

