from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

player_df =  pd.read_csv('players.csv')
club_df = pd.read_csv('CL.csv')
club_df = club_df[pd.to_numeric(club_df['club_id'], errors='coerce').notnull()]
club_df['club_id'] = club_df['club_id'].astype(int)



@app.route('/')
def home_page():
    return render_template('FrontPage.html')

@app.route('/players')
def player_page():
    player=player_df.to_dict(orient='records')
    return render_template('Player.html', players=player)
    

@app.route('/players/<int:player_id>')
def PlayerDetail(player_id):
    print(f"DEBUG: Requested player_id = {player_id}")
    filtered = player_df[player_df['player_id'] == player_id]
    print(f"DEBUG: Filtered dataframe:\n{filtered}")

    if filtered.empty:
        print("DEBUG: No player found!")
        return "Player not found", 404

    player = filtered.iloc[0].to_dict()
    print(f"DEBUG: Player dict:\n{player}")

    player_club = club_df[club_df['name'] == player['current_club_name']]
    print(f"DEBUG: Player club dataframe:\n{player_club}")

    if not player_club.empty:
        player_club = player_club.iloc[0].to_dict()
    else:
        player_club = None
    print(f"DEBUG: Player club dict:\n{player_club}")

    return render_template('PlayerDetail.html', player=player, club=player_club)

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
