import streamlit as st
import pandas as pd
import pickle


def recommend(movie):
    # Fetching the index of 'movie'
    ind = moviesList[moviesList['title'] == movie].index[0]
    distances = similarity[ind]
    # Generating a list of enumerated similarity values [{0, val1}, {1, val2}, .... {4799, val4800}] to preserve index position
    # Sort distances based on similarity & not based on index
    recommended_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    display_list = []
    for i in recommended_list:
        display_list.append(moviesList.iloc[i[0]].title)
    return display_list


def recommenderFnVoteBased(genre):
    # Removing spaces from genre & converting to lower case
    genre = genre.replace(" ", "")
    genre = genre.lower()
    ct = 0
    recommendedList = []
    for movie in range(len(movie_ratings)):
        if movie_ratings.loc[movie, 'genres'].find(genre) != -1:
            recommendedList.append({'title': movie_ratings.loc[movie, 'original_title'],
                                    'score': round(movie_ratings.loc[movie, 'score'], 2)})
            ct += 1
            if ct == 3:
                break
    if (len(recommendedList) == 0):
        return 'No movies found for the genre: '+'\"genre\"'
    else:
        return recommendedList

st.title('Movie Recommender System')
tab1, tab2 = st.tabs(["By Movie", "By Genre"])

with tab1:
    st.header('Recommendation based on selected Movie')
    moviesListDict = pickle.load(open('moviesListDict.pkl', 'rb'))
    moviesList = pd.DataFrame(moviesListDict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))

    selectedMovie = st.selectbox('Select Movie', moviesList['title'].values)
    recommendations = []
    if st.button('Recommend based on Movie'):
        recommendations = recommend(selectedMovie)

    if len(recommendations) != 0:
        st.subheader("Movies similar to \"" + selectedMovie + "\":")
    for i in recommendations:
        st.write(i)

with tab2:
    st.header('Recommendation based on Genre')
    movie_ratings = pickle.load(open('movie_ratings.pkl', 'rb'))
    movie_genre = []
    for movie in range(len(movie_ratings)):
        for g in movie_ratings.loc[movie, 'genres'].split(" "):
            if movie_genre.count(g) == 0:
                movie_genre.append(g)
    movie_genre.pop()

    selectedGenre = st.selectbox('Select Genre', movie_genre)
    recommendations = []
    if st.button('Recommend based on Genre'):
        recommendations = recommenderFnVoteBased(selectedGenre)

    if len(recommendations) != 0:
        st.subheader("Top \""+ selectedGenre +"\" Movies")
    for i in recommendations:
        st.write(i['title'])