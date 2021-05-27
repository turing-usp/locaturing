import requests
import numpy as np
import itertools as it

import dash_bootstrap_components as dbc
import dash_trich_components as dtc
import dash_core_components as dcc
import dash_html_components as html

from dash import Dash
from dash.dependencies import State, Input, Output
from locaturing.preprocess import merge_dataframes, preprocess
from locaturing.modeling import create_model, create_soup, get_recommendations, get_recommendations_filtered, reset_df_index
from locaturing.utils.constants import TMDB_API_KEY, TMDB_DETAILS_BASE_URL, TMDB_POSTER_BASE_URL

def create_model_vars(df1, df2):
    movie_df = merge_dataframes(df1, df2)
    movie_df = preprocess(movie_df)
    movie_df_soup = create_soup(movie_df)
    cosine_sim = create_model(movie_df_soup)
    df_final, indices = reset_df_index(movie_df_soup)
    return movie_df, df_final, cosine_sim, indices

external_stylesheets = [
    "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css",
    "https://use.fontawesome.com/releases/v5.7.2/css/all.css"
]

movie_df, df_final, cosine_sim, indices = create_model_vars(df1 = 'tmdb_5000_credits.csv', df2 = 'tmdb_5000_movies.csv')
app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    title="Locaturing"
)

def get_movie_poster(movie_id):
    r = requests.get(f"{TMDB_DETAILS_BASE_URL}/{movie_id}?api_key={TMDB_API_KEY}&language=en-US")
    r = r.json()
    return f"{TMDB_POSTER_BASE_URL}{r['poster_path']}"

@app.callback(
    Output('movie-carousel', 'children'),
    Input('movie-select', 'value'),
    Input('genre-select', 'value'),
    prevent_initial_call=True
)
def create_carousel_components(movie_select, genre_select):
    if genre_select:
        recommendations = get_recommendations_filtered(movie_df, movie_select, cosine_sim, indices, genre_select)
    else:
        recommendations = get_recommendations(movie_df, movie_select, cosine_sim, indices)#, genre_select)
    children = [dtc.Card(
        image=get_movie_poster(idx),
        title=recommendation['title'],
        description=recommendation['overview'],
        badges=recommendation['genres_list']
    ) for idx, recommendation in recommendations.iterrows()]
    return children

layout = html.Div([
    dbc.Row([
        dbc.Col(
            html.H1(
                "Locaturing", 
                className='display-1', 
                style={'text-align': 'center'}
            ), 
            width={'size':6, 'offset':3}, 
            style={'padding-top':'2em'}
        )
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Select(
                id="movie-select", 
                className="select-box",
                options=[
                    {"label": movie.capitalize(), "value": movie} 
                    for movie in movie_df.title
                ]
            ), 
            width={'size':6, 'offset':3}, 
            style={'padding-top':'2em'}
        )
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Select(
                id="genre-select", 
                options=[
                    {"label": genre.capitalize(), "value": genre} 
                    for genre in set(it.chain.from_iterable(movie_df.genres_list))
                ]
            ), 
            width={'size':6, 'offset':3}, 
            style={'padding-top':'2em'}
        )
    ]),
    dtc.Carousel(
            id='movie-carousel',
            slides_to_scroll=1,
            swipe_to_slide=False,
            autoplay=False,
            speed=2000,
            variable_width=True,
            center_mode=True,
            responsive=[
            {
                'breakpoint': 991,
                'settings': {
                    'arrows': True
                }
            }]
		)
])

app.layout = layout
app.run_server(debug=True)