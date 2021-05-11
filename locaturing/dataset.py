from locaturing.config import cfg
import boto3
import pandas as pd


def get_dataframe(df_name: str) -> pd.DataFrame:
    """
    Coleta um dataframe de um bucket do s3.

    Args:
        df_name (str): nome do dataframe no s3

    Returns:
        pd.DataFrame: um DataFrame do pandas
    """
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket_name=cfg.TURING_AWS_BUCKET, key=df_name)
    response = obj.get()
    df_raw = pd.read_csv(response['Body'])
    return df_raw
