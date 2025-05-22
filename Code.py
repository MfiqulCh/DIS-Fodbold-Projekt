import sqlite3
import pandas as pd

# Connect to the SQLite DB
conn = sqlite3.connect("database.sqlite")

# List of tables to extract
tables_to_extract = ["Player", "Team", "League"]

for table in tables_to_extract:
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    df.to_csv(f"{table.lower()}.csv", index=False)
    print(f"Exported {table}.csv with {len(df)} rows")

conn.close()
