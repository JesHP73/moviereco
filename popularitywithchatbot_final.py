
import streamlit as st
import pandas as pd
import numpy as np

# Define the GitHub URL for the raw CSV data
csv_url = "https://raw.githubusercontent.com/JesHP73/moviereco/85845a1166f211909985e551c8ab860ce58727b5/sample_movies.csv"

# Redefine the functions with the modifications
def calculate_popularity(df):
    # Calculate the count of ratings for each movie
    ratings_count = df.groupby('movieId')['rating'].count()
    # Calculate the average rating for each movie
    average_ratings = df.groupby('movieId')['rating'].mean()
    # Calculate the popularity score as the product of average rating and the logarithm of the count of ratings
    popularity_score = average_ratings * np.log1p(ratings_count)
    # Return the popularity score mapped to the movieId
    return popularity_score.to_dict()

def popularity_recommender(df, num_recommendations):
    # Calculate the popularity score for each movie
    df['popularity_score'] = df['movieId'].map(calculate_popularity(df))
    # Sort the movies by the calculated popularity score in descending order
    sorted_movies = df.sort_values(by='popularity_score', ascending=False)
    # Get the top 'num_recommendations' movies
    recommended_movies = sorted_movies.head(num_recommendations)
    return recommended_movies

# Define the genres
genres = ['Comedy', 'Drama', 'Thriller']

def run_streamlit_app():
    # Load the movie data from the GitHub URL
    df = pd.read_csv(csv_url)

    # Streamlit app
    st.title("Personal movie Recommender")
    st.write("Hi! I'm your personal recommender.")

    genre = st.radio("Choose your genre:", genres)

    if genre:
        st.write(f"You have chosen {genre}")
        recommended_movies = popularity_recommender(df, 15)
        if genre == 'Comedy':
            a = recommended_movies[recommended_movies["genres"].str.contains("Comedy")]
        elif genre == 'Drama':
            a = recommended_movies[recommended_movies["genres"].str.contains("Drama")]
        elif genre == 'Thriller':
            a = recommended_movies[recommended_movies["genres"].str.contains("Thriller")]
        else:
            st.write("Invalid genre selection")

        if not a.empty:
            st.write("Recommended movies:")
            st.table(a[['title', 'popularity_score']].reset_index(drop=True))
        else:
            st.write("No recommendations found for this genre.")

if __name__ == "__main__":
    run_streamlit_app()
