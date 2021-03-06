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
    ]),
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
            dbc.Button("Como funciona?", id="open-modal", block=True), 
            width={'size':6, 'offset':3}, 
        )
    ]),
    dbc.Modal(
        [
            dbc.ModalHeader("Locaturing"),
            dbc.ModalBody([html.P("""
                    O Locaturing ?? um projeto da ??rea de Data Science do Turing.USP que tem como objetivo a cria????o de uma 
                    ferramenta que recomenda filmes com base na escolha do usu??rio por um t??tulo conhecido. Nela voc?? pode inserir um filme de seu gosto 
                    e receber 8 recomenda????es. ?? poss??vel tamb??m selecionar os filmes com base no g??nero, de modo a encontrar a melhor recomenda????o para 
                    cada momento. 
                """),
                html.P("""
                    A t??cnica usada at?? o momento consiste me uma recomenda????o content based, 
                    na qual escolhe-se os filmes que apresentam caracter??sticas mais semelhantes com as caracter??sticas do filme indicado pelo usu??rio. Al??m disso, a 
                    aplica????o permite que o usu??rio altere a import??ncia que cada caracter??stica do filme ?? considerada para as recomenda????es. 
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
