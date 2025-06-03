from fpiplask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('FrontPage.html')

@app.route('/players')
def player_page():
    
    player_df['last_season'] = player_df['last_season'].astype(str)
    filter_players_df = player_df[player_df['last_season'] >= 2024].dropna(subset=['last_season'])
    
    players = filter_players_df.to_dict(orient='records')
    return render_template('Player.html', players=players)


@app.route('/clubs')
def club_page():
    clubs = club_df.to_dict(orient='records')
    

    return render_template('index.html', players=players, clubs=clubs)

if __name__ == '__main__':
    app.run(debug=True)