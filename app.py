from flask import Flask, render_template, request
import random
import os
import psycopg2
import check
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
def index():
    """Show welcome page."""

    return render_template("index.html")

def play(skill):

    if request.method == "POST":

        position = request.form.get('position')
        card1 = request.form.get('card1')
        card2 = request.form.get('card2')

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

        if action == "fold":
            return newGame(skill)
        else:

            suits = ["s", "h", "d", "c"]
            values = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
            deck = [value + suit for suit in  suits for value in values]
            deck.remove(card1)
            deck.remove(card2)
            card3, card4, card5, card6, card7, card8, card9 = random.sample(deck, 7)
            for card in [card3, card4, card5, card6, card7, card8, card9]:
                deck.remove(card)

            board = check.board_state(3, [card1, card2], [card3, card4], [card5, card6, card7, card8, card9], deck)

            result = board.calculate_winner()
            print(result)

            if result == 1:
                result = "You win"
            elif result == 2:
                result = "You lose"
            else:
                result = "Chop"

            site = "reveal" + skill + ".html"

            return render_template(site, title="CS136 Game", card1 = card1.upper(), card2 = card2.upper(), card3 = card3.upper(), 
                                   card4 = card4.upper(), card5 = card5.upper(), card6 = card6.upper(), card7 = card7.upper(), card8 = card8.upper(), 
                                   card9 = card9.upper(), position = position, result = result)

    else:

        return newGame(skill)
    
def newGame(skill):
    site = skill + ".html"

    suits = ["s", "h", "d", "c"]
    values = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
    deck = [value + suit for suit in  suits for value in values]
    card1, card2 = random.sample(deck, 2)

    coin = random.randint(0, 1)
    if coin == 0:
        position = "sb"
        aggress = "Shove"
    else:
        position = "bb"
        aggress = "Call"

    return render_template(site, title="CS136 Game", card1 = card1, card2 = card2, position = position, aggress = aggress)

@app.route("/advanced", methods=["GET", "POST"])
def advanced():
    return play("advanced")

@app.route("/intermediate", methods=["GET", "POST"])
def intermediate():
    return play("intermediate")

@app.route("/beginner", methods=["GET", "POST"])
def beginner():
    return play("beginner")

if __name__ == "__main__":
    app.run(debug=True)