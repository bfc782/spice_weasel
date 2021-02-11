from sqlalchemy import create_engine
import os
import pandas as pd

engine = create_engine('postgres://postgres:postgres@localhost:5432/films', echo=True)

rating_cols = ['user_id','film_id','rating','unix_timestamp']
genre_cols = [
    "genre_unknown", "Action", "Adventure", "Animation", "Children", "Comedy",
    "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror",
    "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"
]

review_cols = rating_cols + genre_cols
film_cols = ['film_id','film','cinema_rel','video_rel','imdb_url']+genre_cols

file_dict = {'films':["|",film_cols],'reviews':["\t",review_cols]}

data_dir= './data/'
files = os.listdir(data_dir)
for file in files:
    full_path = data_dir + file
    table_name = file
    print(full_path, table_name)
    df = pd.read_table(full_path, sep=file_dict[str(file)][0], index_col=0, names=file_dict[str(file)][1], encoding='latin-1')
    df.to_sql(table_name, engine, method='multi', chunksize=1000)
