from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    player_df =  pd.read_csv('players.csv')
    club_df = pd.read_csv('CL.csv')
    
    players = player_df.to_dict(orient='records')
    clubs = club_df.to_dict(orient='records')
    

    return render_template('index.html', players=players, clubs=clubs)

if __name__ == '__main__':
    app.run(debug=True)