import numpy as np
import pandas as pd

from dash import Dash
from src.utils import get_movie_titles_and_genres
from src.layout import layout
from src.callbacks import create_recommendation_callback, create_modal_callback

external_stylesheets = [
    "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css",
    "https://use.fontawesome.com/releases/v5.7.2/css/all.css"
]

app = Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    title="Locaturing"
)

create_recommendation_callback(app)
create_modal_callback(app)

app.layout = layout
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
