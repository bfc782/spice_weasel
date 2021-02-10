# pip install flask

from flask import Flask, request
from flask.templating import render_template
import recommender
from films_db import db_insert

app = Flask('Bens Movie Recommender')

@app.route('/movie')
def get_movie():
    #TODO read the URL parameters
    d = dict(request.args)    
    name = d['movie1']
    rating = int(d['rating1'])
    db_insert(name,rating)
    movie = recommender.get_movie_recommendation(name,rating)
    return render_template('result.html',movie=movie)

@app.route('/')
def hello():
    return render_template('main.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
