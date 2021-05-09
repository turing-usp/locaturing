from preprocess import df_preprocess
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings("ignore")


def create_soup(x, pesos=(1, 1, 1, 1, 0)):
    """
    Funcao que cria a string para cada filme, cada um dos argumentos em pesos define quantas vezes cada uma das features
    vao aparecer nessa composicao de string
    peso0=director
    peso1=keywords
    peso2=lista de genero
    peso3=lista de cast principal
    peso4=lista de companias envolvidas
    """
    return ' '.join(pesos[1]*x['keywords_list']) + ' ' + \
    ' '.join(pesos[2]*x['genres_list']) + ' ' + ' '.join(pesos[3]*x['cast_list']) + ' '.join(pesos[4]*x['companies_list']) + \
           " "+ pesos[0] * (x['director'] + ' ')



df_preprocess['soup'] = df_preprocess.apply(create_soup, axis=1)

df_preprocess['soup'] = df_preprocess['soup'].apply(lambda x : " ".join(x.split()))

# Criacao do bag of words com o countvectorizer do sklearn
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df_preprocess['soup'])
cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

df_preprocess = df_preprocess.reset_index()
indices = pd.Series(df_preprocess.index, index=df_preprocess['title'])

def get_recommendations(title, cosine_sim=cosine_sim2):
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
    return df_preprocess['title'].iloc[movie_indices]



print(get_recommendations('The Godfather'))