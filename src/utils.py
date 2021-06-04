import requests
import itertools as it

from locaturing.preprocess import merge_dataframes, preprocess
from locaturing.modeling import create_model, create_soup, reset_df_index
from locaturing.utils.constants import TMDB_API_KEY, TMDB_DETAILS_BASE_URL, TMDB_POSTER_BASE_URL

def get_movie_titles_and_genres(df1, df2):
    movie_df = merge_dataframes(df1, df2)
    movie_df = preprocess(movie_df)
    movie_titles = [title for title in movie_df.title]
    movie_genres = [genre for genre in set(it.chain.from_iterable(movie_df.genres_list))]
    return movie_titles, movie_genres

def create_model_vars(df1, df2, weights=(1, 1, 1, 1, 0)):
    movie_df = merge_dataframes(df1, df2)
    movie_df = preprocess(movie_df)
    movie_df_soup = create_soup(movie_df, weights)
    cosine_sim = create_model(movie_df_soup)
    df_final, indices = reset_df_index(movie_df_soup)
    return movie_df, df_final, cosine_sim, indices

def get_movie_poster(movie_id):
    r = requests.get(f"{TMDB_DETAILS_BASE_URL}/{movie_id}?api_key={TMDB_API_KEY}&language=en-US")
    r = r.json()
    try:
        poster_path = f"{TMDB_POSTER_BASE_URL}{r['poster_path']}"
    except KeyError as e:
        poster_path = ""
    return poster_path