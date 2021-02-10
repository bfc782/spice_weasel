from random import choice

MOVIES = ['Shrek', 'Ex Machina', 'Star Trek', 'Pulp Fiction']

def get_movie_recommendation(name,rating):
    print("*** doing ML magic ***")
    print("name  : ", name)
    print("rating   : ",rating)

    return choice(MOVIES)
