from typing import List, Tuple
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _create_soup_str(df: pd.DataFrame, columns: List[str],
                pesos=(1, 1, 1, 1, 0)) -> str:
    """
    Funcao que cria a string para cada filme, cada um dos argumentos em pesos
    define quantas vezes cada uma das features vao aparecer nessa composicao
    de string.

    Args:
        df (pd.DataFrame): dataframe base
        columns (List[str]): colunas de interesse
        pesos (tuple, optional): Peso de cada coluna.
        Defaults to (1, 1, 1, 1, 0).

    Returns:
        str: colunas unidas numa única string
    """
    final_string = ''
    for peso, column in zip(pesos, columns):
        column_value = peso*df[column]
        if isinstance(df[column].iloc[0], list):
            column_value = df[column].apply(lambda row:' '.join(peso*row))
        final_string += column_value + ' '
    return final_string


def create_soup(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria a coluna de soup para predição

    Args:
        df (pd.DataFrame): dataframe base

    Returns:
        pd.DataFrame: dataframe com a coluna soup
    """
    df['soup'] = _create_soup_str(
        df,
        ['director', 'keywords_list', 'genres_list', \
        'cast_list', 'companies_list']
    )

    df['soup'] = df['soup'].apply(lambda x : " ".join(x.split()))

    return df


def create_model(df: pd.DataFrame) -> List[List[float]]:
    """
    Cria a matriz com o CountVectorizer

    Args:
        df (pd.DataFrame): dataframe base
    Returns:
        Tuple[list, pd.Series]: matriz do countvectorizer e index da df
    """
    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(df['soup'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    return cosine_sim


def reset_df_index(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Reseta o index do dataframe

    Args:
        df (pd.DataFrame): dataframe base

    Returns:
        List[pd.DataFrame, pd.Series]: dataframe com índice resetado e a lista
        de índices.
    """
    df_process = df.reset_index()
    indices = pd.Series(df_process.index, index=df_process['title'])

    return df_process, indices


def get_recommendations(df: pd.DataFrame, title: str,
    cosine_sim: List[List[float]], indices: pd.Series) -> List[str]:
    """
    Faz a recomendação baseada na similaridade de cosseno da coluna coup

    Args:
        df (pd.DataFrame): dataframe base
        title (str): titulo do filme de interesse
        cosine_sim (List[List[float]]): matriz com a similaridade de cosseno
        indices (pd.Series): indices para pegar o nome das recomendações

    Returns:
        List[str]: lista com o nome dos 10 filmes recomendados
    """
    # Get the index of the movie that matches the title
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return df['title'].iloc[movie_indices]


def get_recommendations_filtered(df: pd.DataFrame, title: str,
    cosine_sim: List[List[float]], indices: pd.Series, genre: str) -> List[str]:
    """
    Faz a recomendação baseada na similaridade de cosseno da coluna coup

    Args:
        df (pd.DataFrame): dataframe base
        title (str): titulo do filme de interesse
        cosine_sim (List[List[float]]): matriz com a similaridade de cosseno
        indices (pd.Series): indices para pegar o nome das recomendações

    Returns:
        List[str]: lista com o nome dos 10 filmes recomendados
    """
    # Get the index of the movie that matches the title
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))


    genre_scores = [i for i in sim_scores if df['genres_list'][i[0]].count(genre)]

    # Sort the movies based on the similarity scores
    genre_scores = sorted(genre_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    genre_scores = genre_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in genre_scores]

    # Return the top 10 most similar movies
    return df['title'].iloc[movie_indices]


