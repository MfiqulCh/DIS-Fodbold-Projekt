from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

player_df =  pd.read_csv('players.csv')
club_df = pd.read_csv('CL.csv')
club_df = club_df[pd.to_numeric(club_df['club_id'], errors='coerce').notnull()]
club_df['club_id'] = club_df['club_id'].astype(int)


@app.route('/')
def player_page():
    players = player_df.to_dict(orient='records')
    return render_template('Player.html', players=players)


@app.route('/clubs')
def club_page():
    clubs = club_df.to_dict(orient='records')
    return render_template('Cl.html', clubs=clubs)

@app.route('/clubs/<int:club_id>')
def club_detail_page(club_id):
    club = club_df[club_df['club_id'] == club_id].to_dict(orient='records')
    
    if not club:
        return "Club not found", 404
    club = club[0]
    
    club_players = player_df[player_df['current_club_name'] == club ['name']].to_dict(orient='records')

    
    return render_template('ClubDetail.html', club=club, players=club_players)

if __name__ == '__main__':
    app.run(debug=True)