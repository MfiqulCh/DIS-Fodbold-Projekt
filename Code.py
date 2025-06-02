from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    df =  pd.read_csv('players.csv')
    players = df.to_dict(orient='records')
    return render_template('index.html', players=players)

if __name__ == '__main__':
    app.run(debug=True)