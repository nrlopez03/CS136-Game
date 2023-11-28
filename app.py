from flask import Flask, render_template, request
import random
import os
import psycopg2
# from datetime import datetime

app = Flask(__name__)

# Retrieve PostgreSQL database URL from Heroku environment variable
database_url = os.environ.get("DATABASE_URL")

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
        cursor.execute("CREATE TABLE results (card1 VARCHAR(255),card2 VARCHAR(255),position VARCHAR(255),skill VARCHAR(255),decision VARCHAR(255),created_at TIMESTAMP);")
        cursor.execute("INSERT INTO results (card1, card2, position, skill, decision, created_at) VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)",
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