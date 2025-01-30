import streamlit as st
import pickle
import pandas as pd

# Load data
movies_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Ensure movies_df is a DataFrame
if isinstance(movies_df, dict):  # In case it's stored as a dictionary
    movies_df = pd.DataFrame(movies_df)

movies_list = movies_df['title'].values

def recommend(movie_name):
    try:
        movie_index = movies_df[movies_df['title'] == movie_name].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = [movies_df.iloc[i[0]].title for i in movies_list]
        return recommended_movies
    except IndexError:
        return ["Movie not found in the database."]

# Streamlit UI
st.title("Movie Recommender System")

selected_movie = st.selectbox("Select a Movie:", movies_list)

if st.button("Get Movie Recommendation"):
    recommendations = recommend(selected_movie)
    st.write("### Recommended Movies:")
    for movie in recommendations:
        st.write(movie)
