from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

player_df =  pd.read_csv('players.csv')
club_df = pd.read_csv('CL.csv')

player_df['last_season'] = player_df['last_season'].astype(str).str.strip()

club_df = club_df[pd.to_numeric(club_df['club_id'], errors='coerce').notnull()]
club_df['club_id'] = club_df['club_id'].astype(int)



@app.route('/')
def home_page():
    return render_template('FrontPage.html')

@app.route('/players')
def player_page():
    
    filter_players_df = player_df[player_df['last_season'] == '2015']
    players = filter_players_df.to_dict(orient='records')
    

    
    print(player_df['last_season'].head())
    print(player_df['last_season'].dtype)
    print("Filtered players count:", len(filter_players_df))

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
        
    club_players = player_df[
        (player_df['current_club_name'] == club['name']) &
        (player_df['last_season'] == '2015')
    ].to_dict(orient='records')
    

    
    return render_template('ClubDetail.html', club=club, players=club_players)

if __name__ == '__main__':
    app.run(debug=True)