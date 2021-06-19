import dash_bootstrap_components as dbc
import dash_trich_components as dtc
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import State, Input, Output
from src.utils import create_model_vars, get_movie_poster
from locaturing.modeling import get_recommendations, get_recommendations_filtered


def create_recommendation_callback(app):
    @app.callback(
        Output('movie-carousel', 'children'),
        Input('movie-select', 'value'),
        Input('genre-select', 'value'),
        Input('director-weight', 'value'),
        Input('keywords-weight', 'value'),
        Input('genres-weight', 'value'),
        Input('cast-weight', 'value'),
        Input('companies-weight', 'value'),
        Input('overview-weight', 'value'),
        prevent_initial_call=True
    )
    def create_carousel_components(
        movie_select, genre_select, director_weight, 
        keywords_weight, genres_weight, cast_weight, companies_weight, overview_weight
    ):
        weight_tuple = (
            director_weight, keywords_weight, 
            genres_weight, cast_weight, companies_weight, overview_weight
        )
        movie_df, df_final, cosine_sim, indices = create_model_vars(df1 = 'tmdb_5000_credits.csv', df2 = 'tmdb_5000_movies.csv', weights=weight_tuple)
        if genre_select:
            recommendations = get_recommendations_filtered(movie_df, movie_select, cosine_sim, indices, genre_select)
        else:
            recommendations = get_recommendations(movie_df, movie_select, cosine_sim, indices)
        children = [
            dtc.Card(
                image=get_movie_poster(idx),
                title=recommendation['title'],
                description=recommendation['overview'],
                badges=recommendation['genres_list']
            ) for idx, recommendation in recommendations.iterrows()
        ]
        return children


def create_modal_callback(app):
    @app.callback(
        Output("modal", "is_open"),
        [Input("open-modal", "n_clicks"), Input("close-modal", "n_clicks")],
        [State("modal", "is_open")],
    )
    def toggle_modal(n1, n2, is_open):
        if n1 or n2:
            return not is_open
        return is_open