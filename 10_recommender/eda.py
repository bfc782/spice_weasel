import pandas as pd

url = '/Users/bfc782/Downloads/ml-100k/'
rating = 'u.data'
info = 'u.info'
film = 'u.item'

rating_cols = ['user_id','film_id','rating','unix_timestamp']
genre_cols = [
    "genre_unknown", "Action", "Adventure", "Animation", "Children", "Comedy",
    "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror",
    "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"
]
film_cols = ['film_id','film','cinema_rel','video_rel','imdb_url']+genre_cols

rating = pd.read_table(url + rating, sep="\t", names=rating_cols)
# info = pd.read_table(url + info, header=None)
film = pd.read_table(url + film, sep="|", names=film_cols, encoding='latin-1')


