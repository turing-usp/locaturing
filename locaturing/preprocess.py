from imports import *
import json
import numpy as np
import pandas as pd

# funcoes para extrair e organizar os dados a partir dos json files
def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

def get_author(x):
    for i in x:
        if i['job'] == 'Author':
            return i['name']
    return np.nan

for feature in ['crew','genres','keywords','production_companies','production_countries','cast']:
    df2[feature] = df2[feature].apply(json.loads)

df2['director'] = df2['crew'].apply(get_director)
df2['author'] = df2['crew'].apply(get_author)


def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        return names

        if len(names) > 3:
            names = names[:3]
        return names

    return []

# aplicacao da funcao para que seja possivel ter a lista de features a partir do json
df2['keywords_list'] = df2['keywords'].apply(get_list)
df2['genres_list'] = df2['genres'].apply(get_list)
df2['companies_list'] = df2['production_companies'].apply(get_list)
df2['countries_list'] = df2['production_countries'].apply(get_list)
df2['cast_list'] = df2['cast'].apply(get_list)
df2['cast_list'] = df2['cast_list'].apply(lambda x : x[:3])

def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        #Check if director exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ''


features = ['keywords_list','genres_list','companies_list','countries_list','cast_list','director']
for feature in features:
    df2[feature] = df2[feature].apply(clean_data)

df2.drop(['cast','production_companies','production_countries','keywords','genres','original_title','crew'],axis=1,inplace=True)


df_preprocess=df2[['budget','overview','title','director','author','keywords_list','genres_list','companies_list',
                   'countries_list','cast_list']]

# lidando com dados faltantes em author
df_preprocess['author'] = df_preprocess['author'].apply(lambda x : x if str(x) != 'nan' else "")
