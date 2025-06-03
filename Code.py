# from flask import Flask, render_template, abort
# import database

# app = Flask(__name__)

# player_df =  pd.read_csv('players.csv')
# club_df = pd.read_csv('CL.csv')
# club_df = club_df[pd.to_numeric(club_df['club_id'], errors='coerce').notnull()]
# club_df['club_id'] = club_df['club_id'].astype(int)



# @app.route('/')
# def home_page():
#     return render_template('FrontPage.html')

# @app.route('/players')
# def player_page():
    
#     player_df['last_season'] = player_df['last_season'].astype(str)
#     filter_players_df = player_df[player_df['last_season'] >= 2024].dropna(subset=['last_season'])
    
#     players = filter_players_df.to_dict(orient='records')
#     return render_template('Player.html', players=players)


# @app.route('/clubs')
# def club_page():
#     clubs = club_df.to_dict(orient='records')
#     return render_template('Cl.html', clubs=clubs)

# @app.route('/clubs/<int:club_id>')
# def club_detail_page(club_id):
#     club = club_df[club_df['club_id'] == club_id].to_dict(orient='records')
    
#     if not club:
#         return "Club not found", 404
#     club = club[0]
    
#     club_players = player_df[player_df['current_club_name'] == club ['name']].to_dict(orient='records')

    
#     return render_template('ClubDetail.html', club=club, players=club_players)

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, abort
import database  # the new database.py file

app = Flask(__name__)

@app.route('/')
def home():
    # Show competitions first
    competitions = database.fetchall("SELECT * FROM competitions ORDER BY cl_year DESC;")
    return render_template('Competitions.html', competitions=competitions)

@app.route('/competitions/<int:cl_year>')
def competition_detail(cl_year):
    # Show clubs for this competition
    clubs = database.fetchall("""
        SELECT * FROM clubs WHERE cl_year = %s ORDER BY name;
    """, (cl_year,))
    competition = database.fetchone("SELECT * FROM competitions WHERE cl_year = %s", (cl_year,))
    if not competition:
        abort(404)
    return render_template('Cl.html', clubs=clubs, competition=competition)

@app.route('/clubs/<club_id>')
def club_detail(club_id):
    club = database.fetchone("SELECT * FROM clubs WHERE club_id = %s", (club_id,))
    if not club:
        abort(404)
    players = database.fetchall("SELECT * FROM players WHERE current_club_id = %s ORDER BY last_name;", (club_id,))
    return render_template('ClubDetail.html', club=club, players=players)

@app.route('/players')
def players():
    players = database.fetchall("SELECT * FROM players ORDER BY last_name LIMIT 100;")
    for p in players:
        p['name'] = f"{p.get('first_name', '')} {p.get('last_name', '')}".strip()

    return render_template('Player.html', players=players)

if __name__ == '__main__':
    app.run(debug=True)
