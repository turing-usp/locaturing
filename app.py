import streamlit as st
import pandas as pd

from typing import List
from locaturing.preprocess import preprocess, merge_dataframes
from locaturing.modeling import create_soup, create_model, reset_df_index, get_recommendations

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

movie_dataframe = load_dataframe()
movie_dataframe_final, cosine_sim, indices = train_model(movie_dataframe)

st.title(":popcorn: Locaturing :popcorn:")
st.write("Modelo de recomendação content-based feito pelo Turing-USP")
movie_option = st.selectbox(
    label='Selecione um filme!',
    options=movie_dataframe['title'].tolist()
)
st.dataframe(
    movie_dataframe.merge(get_recommendations(movie_dataframe_final, movie_option, cosine_sim, indices), how='inner', left_on='title', right_on='title')
)