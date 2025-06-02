from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def player_page():
    player_df =  pd.read_csv('players.csv')
    players = player_df.to_dict(orient='records')
    return render_template('Player.html', players=players)


@app.route('/clubs')
def club_page():
    club_df = pd.read_csv('CL.csv')
    clubs = club_df.to_dict(orient='records')
    return render_template('Cl.html', clubs=clubs)

if __name__ == '__main__':
    app.run(debug=True)