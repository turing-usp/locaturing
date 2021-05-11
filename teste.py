from locaturing.preprocess import merge_dataframes, preprocess
from locaturing.modeling import(
    create_model, create_soup, get_recommendations, reset_df_index
)


if __name__ == '__main__':
    df1 = 'tmdb_5000_credits.csv'
    df2 = 'tmdb_5000_movies.csv'

    df = merge_dataframes(df1, df2)

    df = preprocess(df)

    df_soup = create_soup(df)

    cosine_sim = create_model(df_soup)

    df_final, indices = reset_df_index(df_soup)

    print(get_recommendations(df_final, 'The Godfather', cosine_sim, indices))
