from flask import Flask, render_template, abort
import database  # the new database.py file
import re

app = Flask(__name__)

@app.route('/')
def home():
    # Show competitions first
    competitions = database.fetchall("SELECT * FROM competitions ORDER BY cl_year DESC;")
    return render_template('Competitions.html', competitions=competitions)

def filename_from_club_name(name):
    return re.sub(r'[^\w]', '', name.replace(' ', '_'))

Club_Names = {
    "Arsenal Football Club": "Arsenal FC",
    "Association sportive de Monaco Football Club": "AS Monaco",
    "Associazione Calcio Milan": "AC Milan",
    "Atalanta Bergamasca Calcio S.p.a.": "Atalanta BC",
    "Bayer 04 Leverkusen FuÃŸball": "Bayer 04 Leverkusen",
    "Club AtlÃ©tico de Madrid S.A.D.": "Club Atlético de Madrid",
    "Club Brugge Koninklijke Voetbalvereniging": "Club Brugge KV",
    "Eindhovense Voetbalvereniging Philips Sport Vereniging": "PSV Eindhoven",
    "FC Bayern MÃ¼nchen" : "FC Bayern Munich",
    "Football Club Internazionale Milano S.p.A.": "Inter Milan",
    "Futbol Club Barcelona": "FC Barcelona",
    "Juventus Football Club": "Juventus FC",
    "Lille Olympique Sporting Club": "Lille OSC",
    "Liverpool Football Club": "Liverpool FC",
    "Manchester City Football Club": "Manchester City FC",
    "Paris Saint-Germain Football Club": "PSG",
    "Real Madrid Club de FÃºtbol": "Real Madrid",
    "Sport Lisboa e Benfica": "SL Benfica",
    "Sporting Clube de Portugal": "Sporting CP",
    "Stade brestois 29": "Stade Brestois 29",
    "The Celtic Football Club": "Celtic FC"
}

@app.route('/competitions/<int:cl_year>')
def competition_detail(cl_year):
    clubs = database.fetchall("""
        SELECT * FROM clubs WHERE cl_year = %s ORDER BY name;
    """, (cl_year,))
    competition = database.fetchone("SELECT * FROM competitions WHERE cl_year = %s", (cl_year,))
    if not competition:
        abort(404)
    
    for club in clubs:
        club['logo_filename'] = filename_from_club_name(club['name']) + '.png'
        club['display_name'] = Club_Names.get(club['name'], club['name'])
        print(f"Club: {club['name']}, Logo filename: {club['logo_filename']}")
    
    clubs.sort(key=lambda c: c['display_name'].lower())

    return render_template('Cl.html', clubs=clubs, competition=competition)



@app.route('/clubs/<club_id>')
def club_detail(club_id):
    club = database.fetchone("SELECT * FROM clubs WHERE club_id = %s", (club_id,))
    if not club:
        abort(404)
    players = database.fetchall("SELECT * FROM players WHERE current_club_id = %s ORDER BY last_name;", (club_id,))
    return render_template('ClubDetail.html', club=club, players=players)

@app.route('/players')
def player_page():
    
    player_df['last_season'] = player_df['last_season'].astype(str)
    filter_players_df = player_df[player_df['last_season'] >= 2024].dropna(subset=['last_season'])
    
    players = filter_players_df.to_dict(orient='records')
    return render_template('Player.html', players=players)


if __name__ == '__main__':
    app.run(debug=True)
