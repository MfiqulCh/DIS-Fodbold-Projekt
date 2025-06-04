from flask import Flask, render_template, request, abort
import database  # the new database.py file
import re
import pandas as pd

app = Flask(__name__)

<<<<<<< HEAD
player_df =  pd.read_csv('players.csv')
club_df = pd.read_csv('CL.csv')
club_df = club_df[pd.to_numeric(club_df['club_id'], errors='coerce').notnull()]
club_df['club_id'] = club_df['club_id'].astype(int)
competition_df = pd.read_csv('competitions (1).csv')


=======
>>>>>>> 400a3b7ea69a82fee7eea70847e0488ca49824c9

@app.route('/')
def home():
    return render_template('Competitions.html', competitions=competition_df.to_dict(orient='records'))

def filename_from_club_name(name: str) -> str:
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
    print(f"Fetching data for cl_year: {cl_year}")
    clubs = database.fetchall("""
        SELECT * FROM clubs WHERE cl_year = %s ORDER BY name;
    """, (cl_year,))
    competition = database.fetchone("SELECT * FROM competitions WHERE cl_year = %s", (cl_year,))
    print(f"Competition: {competition}")
    print(f"Clubs: {clubs}")
    if not competition:
        abort(404)
    
    for club in clubs:
        club['logo_filename'] = filename_from_club_name(club['name']) + '.png'
        club['display_name'] = Club_Names.get(club['name'], club['name'])
        print(f"Club: {club['name']}, Logo filename: {club['logo_filename']}")
    
    clubs.sort(key=lambda c: c['display_name'].lower())

    return render_template('Cl.html', clubs=clubs, competition=competition)


@app.route('/clubs')
def list_clubs():
    clubs = club_df.to_dict(orient='records')
    for c in clubs:
        c['logo_filename'] = filename_from_club_name(c['name']) + '.png'
        c['display_name']  = Club_Names.get(c['name'], c['name'])
    clubs.sort(key=lambda c: c['display_name'].lower())
    return render_template('Cl.html', clubs=clubs)

<<<<<<< HEAD


@app.route('/clubs/<int:club_id>')
=======
# @app.route('/clubs/<club_id>')
# def club_detail(club_id):
#     club = database.fetchone("SELECT * FROM clubs WHERE club_id = %s", (club_id,))
#     if not club:
#         abort(404)
#     players = database.fetchall("SELECT * FROM players WHERE current_club_id = %s ORDER BY last_name;", (club_id,))
#     return render_template('ClubDetail.html', club=club, players=players)

@app.route('/clubs/<club_id>')
>>>>>>> 400a3b7ea69a82fee7eea70847e0488ca49824c9
def club_detail(club_id):
    club = database.fetchone(
        "SELECT * FROM clubs WHERE club_id = %s", (str(club_id),))
    if not club:
        abort(404)
<<<<<<< HEAD

    cleaned = filename_from_club_name(club["name"])
    club["logo_filename"] = cleaned + ".png"

    players = database.fetchall(
        "SELECT * FROM players WHERE current_club_id = %s", (str(club_id),)
    )

    return render_template("ClubDetail.html", club=club, players=players)

=======
    
    # Updated SQL query without the 'foot' column
    players_sql = """
    SELECT player_id, first_name, last_name, position, height_in_cm, market_value_in_eur 
    FROM players 
    WHERE current_club_id = %s 
    ORDER BY last_name;
    """
    players = database.fetchall(players_sql, (club_id,))
    
    return render_template('ClubDetail.html', club=club, players=players)
>>>>>>> 400a3b7ea69a82fee7eea70847e0488ca49824c9



@app.route('/players')
def player_page():
    
    player_df['last_season'] = player_df['last_season'].astype(str)
    filter_players_df = player_df[player_df['last_season'] >= 2024].dropna(subset=['last_season'])
    
    players = filter_players_df.to_dict(orient='records')
    return render_template('Player.html', players=players)

<<<<<<< HEAD
    

@app.route('/players/<int:player_id>')
def PlayerDetail(player_id):
    filtered = player_df[player_df['player_id'] == player_id]

    if filtered.empty:
        abort (404)
    
    player = filtered.iloc[0].to_dict()
    club_row = club_df[club_df['name'] == player['current_club_name']]
    club_data = None
    
    if not club_row.empty:
        club_data = club_row.iloc[0].to_dict()
        club_data['logo_filename'] = filename_from_club_name(club_data['name']) + '.png'
        club_data['display_name'] = Club_Names.get(club_data['name'], club_data['name'])
    return render_template('PlayerDetail.html', player=player, club=club_data)



# @app.route('/csv/players')
# def csv_players():
#     players = player_df.to_dict(orient='records')
#     for p in players:
#         p['name'] = f"{p.get('first_name','')} {p.get('last_name','')}".strip()
#     return render_template('Player.html', players=players)


# @app.route('/csv/clubs')
# def club_page():
#     clubs = club_df.to_dict(orient='records')
#     return render_template('Cl.html', clubs=clubs)

# @app.route('/csv/clubs/<int:club_id>')
# def club_detail_page(club_id):
#     club_List = club_df[club_df['club_id'] == club_id].to_dict(orient='records')
    
#     if not club_List:
#         return "Club not found", 404
#     club = club_List[0]
    
    
#     club_players = player_df[player_df['current_club_name'] == club ['name']].to_dict(orient='records')
    
#     return render_template('ClubDetail.html', club=club, players=club_players)
=======
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get("query", "").lower()
    
    if not query:
        return render_template('search_results.html', players=[], clubs=[], query=query)
    
    players_sql = """
    SELECT * FROM players 
    WHERE LOWER(first_name) LIKE %s OR LOWER(last_name) LIKE %s OR LOWER(position) LIKE %s;
    """
    players = database.fetchall(players_sql, (f"%{query}%", f"%{query}%", f"%{query}%"))
    
    clubs_sql = """
    SELECT * FROM clubs 
    WHERE LOWER(name) LIKE %s OR LOWER(coach_name) LIKE %s;
    """
    clubs = database.fetchall(clubs_sql, (f"%{query}%", f"%{query}%"))
    
    return render_template('search_results.html', players=players, clubs=clubs, query=query)

@app.route('/players/<int:player_id>')
def player_detail(player_id):
    # Fetch player details without the 'foot' column
    player = database.fetchone("""
        SELECT player_id, first_name, last_name, position, height_in_cm, market_value_in_eur, current_club_name
        FROM players
        WHERE player_id = %s
    """, (player_id,))

    if not player:
        abort(404)

    return render_template('PlayerDetail.html', player=player)


>>>>>>> 400a3b7ea69a82fee7eea70847e0488ca49824c9

if __name__ == '__main__':
    app.run(debug=True)
