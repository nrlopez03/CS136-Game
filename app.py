from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods=["GET", "POST"])
def homepage():

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
        elif 'Fold' in request.form:
            action = "fold"

        return render_template("index.html", title="CS136 Game", card1 = card1, card2 = card2, position = position, aggress = aggress)

    else:

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


        return render_template("index.html", title="CS136 Game", card1 = card1, card2 = card2, position = position, aggress = aggress)

if __name__ == "__main__":
    app.run(debug=True)