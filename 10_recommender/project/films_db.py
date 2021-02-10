from sqlalchemy import create_engine

def db_insert(string, number):
    pg = create_engine('postgres://postgres:postgres@localhost:5432/films', echo=True)
    pg.execute('''
        CREATE TABLE IF NOT EXISTS ratings (
        name VARCHAR(200),
        rating NUMERIC
    );
    ''')

#    name = "The Shawshank Redemption test"
#    rating = 3.4
    query = "INSERT INTO ratings VALUES (%s, %s);"
    pg.execute(query, (string, number))


