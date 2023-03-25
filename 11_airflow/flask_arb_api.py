# pip install flask

from flask import Flask, request, jsonify
from flask.templating import render_template
from datetime import datetime

app = Flask('arb_data_server')

@app.route('/data')
def get_data():
    date_data = datetime.now()
    return jsonify({'data': [f'hello world {date_data}' for i in range(5)]})

if __name__ == "__main__":
    app.run(debug=True, port=5000)