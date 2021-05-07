import pandas as pd

# criando a tabela
df1=pd.read_csv('../Data/tmdb_5000_credits.csv')
df2=pd.read_csv('../Data/tmdb_5000_movies.csv')

df2.drop(['homepage'], axis=1,inplace=True)
df1.columns = ['id','tittle','cast','crew']
df2= df2.merge(df1,on='id')
df2.set_index('id',inplace=True)

del df1

df2.head()