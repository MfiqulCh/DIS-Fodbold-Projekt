import os
import csv
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_NAME     = os.getenv("DB_NAME", "ChampionsLeague")
DB_USER     = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Mush2003")

conn = psycopg2.connect(
    host=DB_HOST,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cur = conn.cursor()

def parse_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except:
        return None

# Competitions.csv
with open("competitions (1).csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(
        f,
        delimiter=",",
        quotechar='"',
    )
    
    if reader.fieldnames and reader.fieldnames[0].startswith("\ufeff"):
        reader.fieldnames[0] = reader.fieldnames[0].lstrip("\ufeff")

    attributes = []
    for row in reader:
        cl_year = None
        if row.get("cl_year"):
            try:
                cl_year = int(row["cl_year"])
            except:
                cl_year = None
        attributes.append((
            row.get("competition_id"),
            row.get("name"),
            row.get("type"),
            row.get("sub_type"),
            row.get("confederation"),
            cl_year,
            row.get("url")
        ))

    sql = """
        INSERT INTO competitions(
            competition_id, 
            name, 
            type, 
            sub_type, 
            confederation, 
            cl_year, 
            url
        ) VALUES %s
        ON CONFLICT (cl_year) DO NOTHING
    """
    execute_values(cur, sql, attributes)

# CL.csv
with open("CL.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(
        f,
        delimiter=",",
        quotechar='"'
    )

    if reader.fieldnames and reader.fieldnames[0].startswith("\ufeff"):
        reader.fieldnames[0] = reader.fieldnames[0].lstrip("\ufeff")

    attributes = []
    for row in reader:
        squad_size = int(row["squad_size"]) if row.get("squad_size") else None
        average_age = float(row["average_age"]) if row.get("average_age") else None
        foreigners_number = int(row["foreigners_number"]) if row.get("foreigners_number") else None
        foreigners_percentage = float(row["foreigners_percentage"]) if row.get("foreigners_percentage") else None
        stadium_seats = int(row["stadium_seats"]) if row.get("stadium_seats") else None
        coach_name = row.get("coach_name") 
        if coach_name == '': 
            coach_name = None

        cl_year = None
        if row.get("cl_year"):
            try:
                cl_year = int(row["cl_year"])
            except:
                cl_year = None

        attributes.append((
            row.get("club_id"),
            row.get("club_code"),
            row.get("name"),
            row.get("domestic_competition_id"),
            squad_size,
            average_age,
            foreigners_number,
            foreigners_percentage,
            row.get("stadium_name"),
            stadium_seats,
            coach_name,
            row.get("url"),
            cl_year
        ))
    
    sql = """
        INSERT INTO clubs(
            club_id,
            club_code,
            name,
            domestic_competition_id,
            squad_size,
            average_age,
            foreigners_number,
            foreigners_percentage,
            stadium_name,
            stadium_seats,
            coach_name,
            url,
            cl_year
        ) VALUES %s
        ON CONFLICT (club_id) DO NOTHING;
    """
    execute_values(cur, sql, attributes)

cur.execute("SELECT club_id FROM clubs;")
valid_clubs = {row[0] for row in cur.fetchall()}

# Players.csv
with open("players.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(
        f,
        delimiter=",",
        quotechar='"'
    )

    if reader.fieldnames and reader.fieldnames[0].startswith("\ufeff"):
        reader.fieldnames[0] = reader.fieldnames[0].lstrip("\ufeff")

    attributes = []

    for row in reader:
        date_of_birth = parse_date(row.get("date_of_birth", ""))
        height_in_cm = int(row["height_in_cm"]) if row.get("height_in_cm") else None
        mkt_val = float(row["market_value_in_eur"]) if row.get("market_value_in_eur") else None
        high_mkt_val = float(row["highest_market_value_in_eur"]) if row.get("highest_market_value_in_eur") else None
        current_club = row.get("current_club_id")
        club_id = current_club if current_club in valid_clubs else None

        attributes.append((
            int(row["player_id"].split(",")[0]),
            row.get("first_name"),
            row.get("last_name"),
            date_of_birth,
            row.get("position"),
            row.get("sub_position"),
            height_in_cm,
            mkt_val,
            high_mkt_val,
            club_id,
            row.get("current_club_name"),
            row.get("country_of_birth"),
            row.get("agent_name"),
            row.get("first_name") + " " + row.get("last_name") if row.get("first_name") and row.get("last_name") else None
            
        ))


        if len(attributes) >= 1000:
            sql_players = """
                INSERT INTO players(
                    player_id,
                    first_name,
                    last_name,
                    date_of_birth,
                    position,
                    sub_position,
                    height_in_cm,
                    market_value_in_eur,
                    highest_market_value_in_eur,
                    current_club_id,
                    current_club_name,
                    country_of_birth,
                    agent_name
                ) VALUES %s
                ON CONFLICT (player_id) DO NOTHING;
            """

            execute_values(cur, sql_players, attributes)
            attributes.clear()
    
    if attributes:
        sql_players = """
            INSERT INTO players(
                player_id,
                first_name,
                last_name,
                date_of_birth,
                position,
                sub_position,
                height_in_cm,
                market_value_in_eur,
                highest_market_value_in_eur,
                current_club_id,
                current_club_name,
                country_of_birth,
                agent_name
            ) VALUES %s
            ON CONFLICT (player_id) DO NOTHING;
        """
        execute_values(cur, sql_players, attributes)

conn.commit()
cur.close()
conn.close()

print("Data loading complete.")