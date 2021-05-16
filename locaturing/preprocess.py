import json
from typing import List
from locaturing.dataset import get_dataframe, get_dataframe_local
import numpy as np
import pandas as pd


def _get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]

        if len(names) > 3:
            names = names[:3]

        return names

    return []


def _clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]

    #Check if director exists. If not, return empty string
    if isinstance(x, str):
        return str.lower(x.replace(" ", ""))

    return ''


def _get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan


def _get_author(x):
    for i in x:
        if i['job'] == 'Author':
            return i['name']
    return np.nan


def merge_dataframes(df1_name: str, df2_name: str) -> pd.DataFrame:
    """
    Mergeia 2 dataframes do pandas e faz algumas operações adicionais

    Args:
        df1_name (str): nome do primeiro dataframe
        df2_name (str): nome do primeiro dataframe

    Returns:
        pd.DataFrame: dataframe mergeado
    """
    df1 = get_dataframe_local(df1_name)
    df2 = get_dataframe_local(df2_name)

    df2.drop(['homepage'], axis=1,inplace=True)
    df1.columns = ['id','tittle','cast','crew']
    df_merged= df2.merge(df1,on='id')
    df_merged.set_index('id',inplace=True)
    
    del df1
    
    return df_merged


def load_columns_json(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Converte as colunas de str para o json equivalente.

    Args:
        df (pd.DataFrame): dataframe base
        columns (List[str]): colunas de interesse

    Returns:
        pd.DataFrame: dataframe com as colunas em json
    """
    for feature in columns:
        df[feature] = df[feature].apply(json.loads)
    return df


def make_applys_in_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica as funcões no dataframe.

    Args:
        df (pd.DataFrame): dataframe base

    Returns:
        pd.DataFrame: dataframe após aplicar as funções
    """
    df['director'] = df['crew'].apply(_get_director)
    df['author'] = df['crew'].apply(_get_author)

    df['keywords_list'] = df['keywords'].apply(_get_list)
    df['genres_list'] = df['genres'].apply(_get_list)
    df['companies_list'] = df['production_companies'].apply(_get_list)
    df['countries_list'] = df['production_countries'].apply(_get_list)
    df['cast_list'] = df['cast'].apply(_get_list)
    df['cast_list'] = df['cast_list'].apply(lambda x : x[:3])
    df['author'] = df['author'].apply(lambda x : x if str(x) != 'nan' else "")

    return df


def clean_df_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Limpa as colunas passadas

    Args:
        df (pd.DataFrame): dataframe base
        columns (List[str]): lista de colunas de interesse

    Returns:
        pd.DataFrame: dataframe processado
    """
    for feature in columns:
        df[feature] = df[feature].apply(_clean_data)
    return df


def select_df_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Seleciona as colunas passadas no dataframe

    Args:
        df (pd.DataFrame): dataframe base
        columns (List[str]): colunas de interesse

    Returns:
        pd.DataFrame: dataframe com as colunas de interesse
    """
    return df[columns]


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza todo o pre-processamento do dataframe.

    Args:
        df (pd.DataFrame): dataframe base

    Returns:
        pd.DataFrame: dataframe processado
    """
    df_jsons = load_columns_json(
        df,
        ['crew', 'genres', 'keywords', 'production_companies', \
        'production_countries', 'cast']
    )

    df_applied = make_applys_in_df(df_jsons)

    df_cleaned = clean_df_columns(
        df_applied,
        ['keywords_list', 'genres_list', 'companies_list', \
        'countries_list', 'cast_list', 'director']
    )

    df_processed = select_df_columns(
        df_cleaned,
        ['budget', 'overview', 'title', 'director', 'author', 'keywords_list',\
        'genres_list', 'companies_list', 'countries_list', 'cast_list']
    )

    return df_processed
