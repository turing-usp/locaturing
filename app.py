import streamlit as st
import pandas as pd

from typing import List
from locaturing.preprocess import preprocess, merge_dataframes
from locaturing.modeling import create_soup, create_model, get_recommendations_filtered, reset_df_index, get_recommendations

@st.cache(allow_output_mutation=True)
def load_dataframe() -> pd.DataFrame:
    """
    Carrega o dataframe
    Decorator:
        Armazena a funcao no cache do streamlit para evitar o reload do dataset a cada rodada
    Returns:
        pd.DataFrame: um DataFrame do pandas
    """
    df1 = 'tmdb_5000_credits.csv'
    df2 = 'tmdb_5000_movies.csv'
    df = merge_dataframes(df1, df2)
    df = preprocess(df)
    return df

@st.cache
def train_model(dataframe: pd.DataFrame) -> List[List[float]]:
    """
    Cria a matriz com o CountVectorizer
    Decorator:
        Armazena a funcao no cache do streamlit para evitar o reload do dataset a cada rodada
    Args:
        df (pd.DataFrame): dataframe base
    Returns:
        Tuple[list, pd.Series]: matriz do countvectorizer e index da df
    """
    dataframe_soup = create_soup(dataframe)
    cosine_sim = create_model(dataframe_soup)
    df_final, indices = reset_df_index(dataframe_soup)
    return df_final, cosine_sim, indices


st.title(":popcorn: Locaturing :popcorn:")
st.write("Modelo de recomendação content-based feito pelo Turing-USP")

movie_dataframe = load_dataframe()
movie_dataframe_final, cosine_sim, indices = train_model(movie_dataframe)



genre_column = list(movie_dataframe['genres_list'])
flat_genre = [item for sublist in genre_column for item in sublist]
unique_genres = pd.Series(flat_genre).unique()


movie_option = st.selectbox(
    label='Selecione um filme!',
    options=movie_dataframe['title'].tolist()
)

genre_option = st.selectbox(
    label='Selecione um gênero',
    options=unique_genres.tolist()
)

movie_dataframe_final, cosine_sim, indices = train_model(movie_dataframe)



st.dataframe(
    movie_dataframe.merge(get_recommendations_filtered(movie_dataframe_final, movie_option, cosine_sim, indices,genre_option), how='inner', left_on='title', right_on='title')
)