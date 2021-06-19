import dash_bootstrap_components as dbc
import dash_trich_components as dtc
import dash_core_components as dcc
import dash_html_components as html

from src.utils import get_movie_titles_and_genres
titles, genres = get_movie_titles_and_genres(df1 = 'tmdb_5000_credits.csv', df2 = 'tmdb_5000_movies.csv')

layout = html.Div([
    dtc.SideBar([
        dtc.SideBarItem(id='director-label', label="Peso do Diretor", icon="fas fa-user-edit"),
        dcc.Slider(
            id='director-weight',
            min=0,
            max=5,
            step=1,
            value=1,
        ),
        dtc.SideBarItem(id='keywords-label', label="Peso das Keywords", icon="fas fa-file-word"),
        dcc.Slider(
            id='keywords-weight',
            min=0,
            max=5,
            step=1,
            value=1,
        ),
        dtc.SideBarItem(id='genres-label', label="Peso dos Generos", icon="fas fa-list"),
        dcc.Slider(
            id='genres-weight',
            min=0,
            max=5,
            step=1,
            value=1,
        ),
        dtc.SideBarItem(id='cast-label', label="Peso dos Atores", icon="fas fa-users"),
        dcc.Slider(
            id='cast-weight',
            min=0,
            max=5,
            step=1,
            value=1,
        ),
        dtc.SideBarItem(id='companies-label', label="Peso da Produtora", icon="fas fa-building"),
        dcc.Slider(
            id='companies-weight',
            min=0,
            max=5,
            step=1,
            value=0,
        ),
        dtc.SideBarItem(id='overview-label', label="Peso da Sinopse", icon="fas fa-book"),
        dcc.Slider(
            id='overview-weight',
            min=0,
            max=5,
            step=1,
            value=1,
        ),
    ], bg_color="#dc3545"),
    dbc.Row([
        dbc.Col(
            html.H1(
                "Locaturing", 
                className='display-1', 
                style={'text-align': 'center', 'font-family': "Fantasy"},
            ), 
            width={'size':6, 'offset':3}, 
            style={'padding-top':'2em', 'font-family': "Fantasy"}
        )
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col(
            dbc.Button("Como funciona?", id="open-modal", block=True, color="danger"), 
            width={'size':6, 'offset':3},
            # style={"background-color": "#4CAF50",
            # "border": "none",
            # "color": "white",
            # "padding": "15px 32px",
            # "text-align": "center",
            # "text-decoration": "none",
            # "display": "inline-block",
            # "font-size": "16px",
            # "background-image": "none"}
        ),
    ]),
    html.Br(),
    dbc.Modal(
        [
            dbc.ModalHeader("Locaturing"),
            dbc.ModalBody([html.P("""
                    O Locaturing é um projeto da área de Data Science do Turing.USP que tem como objetivo a criação de uma 
                    ferramenta que recomenda filmes com base na escolha do usuário por um título conhecido. Nela você pode inserir um filme de seu gosto 
                    e receber 8 recomendações. É possível também selecionar os filmes com base no gênero, de modo a encontrar a melhor recomendação para 
                    cada momento. 
                """),
                html.P("""
                    A técnica usada até o momento consiste me uma recomendação content based, 
                    na qual escolhe-se os filmes que apresentam características mais semelhantes com as características do filme indicado pelo usuário. Além disso, a 
                    aplicação permite que o usuário altere a importância que cada característica do filme é considerada para as recomendações. 
                """),
                html.P("""
                    Para o deploy utilizamos a biblioteca Dash, biblioteca para criar fronts focados em Dados de maneira simples.
                """)
            ]),
            dbc.ModalFooter(
                dbc.Button("Fechar", id="close-modal", className="ml-auto")
            ),
        ],
        id="modal",
        size='xl'
    ),
    html.Br(),
    dbc.Row([
        dbc.Col(
            dbc.Select(
                id="movie-select", 
                className="select-box",
                options=[
                    {"label": title.capitalize(), "value": title} 
                    for title in titles
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
                    for genre in genres
                ]
            ), 
            width={'size':6, 'offset':3}, 
            style={'padding-top':'2em'}
        )
    ]),
    html.Br(),
    dbc.Spinner([
        dtc.Carousel(
            id='movie-carousel',
            slides_to_scroll=1,
            swipe_to_slide=False,
            autoplay=False,
            speed=2000,
            variable_width=True,
            center_mode=True,
            responsive=[{
                'breakpoint': 991,
                'settings': {
                    'arrows': True
                }
            }]
        ),
    ],
        color='warning',
        type='grow'
    )
])
