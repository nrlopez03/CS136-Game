from flask import Flask, render_template, request
import random
import os
import psycopg2
import check
from resp import hand_to_num
import pandas as pd
import time
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

app = Flask(__name__)

p1_resp = pd.read_csv(os.path.join(app.static_folder, 'p1_resp.csv'), header=None).values
p2_resp = pd.read_csv(os.path.join(app.static_folder, 'p2_resp.csv'), header=None).values

# PnL = 0.0

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
        card3 = request.form.get('card3')
        card4 = request.form.get('card4')
        PnL = float(request.form.get('PnL'))

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

            if position == "sb":
                change = -0.5
                history = "You folded as the small blind. -0.5"
            else:
                change = -1.0
                history = "You folded as the big blind. -1"

            return newGame(skill, position, PnL + change, history)
        else:

            if position == "sb":
                fold, call = p2_resp[hand_to_num[(card3, card4)]]
                if call < 0 or (random.random() < fold/(fold + call) and fold > 0):
                    change = 1.0
                    return newGame(skill, position, PnL + change, f"The BB folds. +1")

            suits = ["s", "h", "d", "c"]
            values = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
            deck = [value + suit for suit in  suits for value in values]
            deck.remove(card1)
            deck.remove(card2)
            deck.remove(card3)
            deck.remove(card4)
            card5, card6, card7, card8, card9 = random.sample(deck, 5)
            for card in [card5, card6, card7, card8, card9]:
                deck.remove(card)

            board = check.board_state(3, [card1, card2], [card3, card4], [card5, card6, card7, card8, card9], deck)

            result = board.calculate_winner()

            if result == 1:
                result = "You won. +10"
                PnL += 10
            elif result == 2:
                result = "You lost. -10"
                PnL -= 10
            else:
                result = "Chop."

            site = "reveal" + skill + ".html"

            return render_template(site, title="CS136 Game", card1 = card1.upper(), card2 = card2.upper(), card3 = card3.upper(), 
                                   card4 = card4.upper(), card5 = card5.upper(), card6 = card6.upper(), card7 = card7.upper(), card8 = card8.upper(), 
                                   card9 = card9.upper(), position = position, result = result, PnL = PnL, skill = skill)

    else:

        return newGame(skill)
    
def newGame(skill, position = "unassigned", PnL = 0.0, previous = ""):
    site = skill + ".html"

    suits = ["s", "h", "d", "c"]
    values = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
    deck = [value + suit for suit in  suits for value in values]
    card1, card2, card3, card4 = random.sample(deck, 4)

    if position == "unassigned":
        coin = random.randint(0, 1)
        if coin == 0:
            position = "sb"
            aggress = "Shove"
        else:
            position = "bb"
            aggress = "Call"
    elif position == "sb":
        position = "bb"
        aggress = "Call"
    else:
        position = "sb"
        aggress = "Shove"

    if position == "bb":
        fold, call = p1_resp[hand_to_num[(card3, card4)]]

        if call < 0 or (random.random() < fold/(fold + call) and fold > 0):

            if previous != "":
                result = previous + "\n Then, the small blind folded. +0.5"
            else:
                result = "Then, the small blind folded. +0.5"

            return render_template("sb_fold.html", skill = skill, position = position, PnL = PnL + 0.5, 
                                   result = result)

    return render_template(site, title="CS136 Game", card1 = card1, card2 = card2, card3 = card3, card4 = card4, 
                           position = position, aggress = aggress, PnL = PnL, previous = previous)

@app.route("/advanced", methods=["GET", "POST"])
def advanced():
    return play("advanced")

@app.route("/intermediate", methods=["GET", "POST"])
def intermediate():
    return play("intermediate")

@app.route("/beginner", methods=["GET", "POST"])
def beginner():
    return play("beginner")

@app.route("/next", methods=["GET", "POST"])
def next():
    skill = request.form.get('skill')
    position = request.form.get('position')
    PnL = float(request.form.get('PnL'))
    result = request.form.get('result')
    return newGame(skill, position, PnL, result)

if __name__ == "__main__":
    app.run(debug=True)