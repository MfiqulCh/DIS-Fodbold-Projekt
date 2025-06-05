First you have to get acces to venv by typing this in the terminal:
.\venv\Scripts\activate

If flask isn't installed you should do this command:

pip install flask 

pip install psycopg2-binary 

pip install python-dotenv

You need to get acces to postgres by typing:
.\psql.exe -U postgres -d ChampionsLeague -f "Path\to\football.sql"
Then postgres need a password, where you type:
1234

You still need to get acces to our footbal.sql by making a pgAdmin (or any PostgresSQl client), then insert our file footbal.sql, and 
execute the scripts.

Now you would be able to run the code, but first, you need to run load_data.py by typing this command in a git bash terminal.
python load_data.py

After you can run the code by typing: 
python Code.py
Then u will get a server address that you should copy and paste it on a browser or hold ctrl and click on it.
__________________________________________________________________________________________________________________________
The SQL part of our code only uses the SELECT statement in the Code.py file, to fetch data for competitions, 
clubs, and players that competed in the Champions League during a specific year.

In the load_data.py we use INSERT statement to add data into the competition, clubs and players tables
We also use UPDATE statement, but its combined with INSERT statement, when a conflict occurs by updating existing rows when necessary
