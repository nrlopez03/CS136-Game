from flask import Flask, render_template, request
import random
import os
import psycopg2
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

app = Flask(__name__)

# Retrieve PostgreSQL database URL from Heroku environment variable
database_url = os.environ.get("DATABASE_URL")
database_url = "postgres://yulppopcmvngzw:69d460d3802d82c396a5d65f5e94bd408ad14474f1a1ba3938855376e4eb7bee@ec2-44-206-204-65.compute-1.amazonaws.com:5432/dfbj7ho88v7t9c"

# Connect to the database
conn = psycopg2.connect(database_url, sslmode='require')
cursor = conn.cursor()

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods=["GET", "POST"])
def homepage():

    if request.method == "POST":

        position = request.form.get('position')
        card1 = request.form.get('card1')
        card2 = request.form.get('card2')

        skill = "expert"

        if position == "sb":
            aggress = "Shove"
        else:
            aggress = "Call"

        if 'Aggress' in request.form:
            action = "aggress"
        else:
            action = "fold"

        # Get the current timestamp
        # created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insert data into the database
        cursor.execute("INSERT INTO results (card1, card2, position, skill, decision, played_at) VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)",
                        (card1, card2, position, skill, action))
        conn.commit()

        return render_template("index.html", title="CS136 Game", card1 = card1, card2 = card2, position = position, aggress = aggress)

    else:

        suits = ["s", "h", "d", "c"]
        values = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
        deck = [value + suit for suit in  suits for value in values]
        card1, card2 = random.sample(deck, 2)

        coin = random.randint(0, 1)
        if coin == 0:
            position = "sb"
            aggress = "Shove"
        else:
            position = "bb"
            aggress = "Call"


        return render_template("index.html", title="CS136 Game", card1 = card1, card2 = card2, position = position, aggress = aggress)

if __name__ == "__main__":
    app.run(debug=True)