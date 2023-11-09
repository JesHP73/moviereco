
import streamlit as st
import pandas as pd
import numpy as np


csv_url = "https://raw.githubusercontent.com/JesHP73/moviereco/85845a1166f211909985e551c8ab860ce58727b5/sample_movies.csv"


def calculate_popularity(df):
    ratings_count = df.groupby('movieId')['rating'].count()
    average_ratings = df.groupby('movieId')['rating'].mean()
    popularity_score = average_ratings * np.log1p(ratings_count)
    return popularity_score.to_dict()

def popularity_recommender(df, num_recommendations):
    df['popularity_score'] = df['movieId'].map(calculate_popularity(df))
    sorted_movies = df.sort_values(by='popularity_score', ascending=False)
    recommended_movies = sorted_movies.head(num_recommendations)
    return recommended_movies[['movieId', 'title', 'genres']]  # took out the 'rating' for the user

def run_streamlit_app():
    # Load the movie data from the GitHub URL and lest call it df
    df = pd.read_csv(csv_url)

    # Streamlit app starts from here  for the user 
    st.title("Personal Movie Recommender")
    st.write("Hi! I'm your personal recommender. 😊🎬")

    
    chat = st.container()

    genres = ['Comedy', 'Drama', 'Thriller']
    genre_choice = st.text_input("Choose your genre (type 1 for Comedy, 2 for Drama, 3 for Thriller):")
    
    genre_map = {'1': 'Comedy', '2': 'Drama', '3': 'Thriller'}

    if genre_choice in genre_map:
        selected_genre = genre_map[genre_choice]
        with chat:
            st.chat_message("user", f"You have chosen {selected_genre}")
            top_movies = popularity_recommender(df, 10)

            a = top_movies[top_movies["genres"].str.contains(selected_genre)] 

            if not a.empty:
                st.chat_message("assistant", "Here are your personal movie recommendations, Enjoy! 🍿")
                for movie_title in a['title']:
                    st.chat_message("assistant", movie_title)
            else:
                st.chat_message("assistant", "No recommendations found now, sorry. 😕")

        continue_chat = st.radio("Do you want another recommendation?", ["Yes", "No"])
        if continue_chat == "No":
            with chat:
                st.chat_message("assistant", "Thanks for using the recommender! Have a great day! 👋")
            st.stop()
    else:
        with chat:
            st.chat_message("assistant", "Invalid genre selection. Please type 1, 2, or 3. 🔄")

if __name__ == "__main__":
    run_streamlit_app()
