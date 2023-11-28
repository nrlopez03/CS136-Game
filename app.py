from flask import Flask, render_template, request

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods=["GET", "POST"])
def homepage():

    if request.method == "POST":

        position = "Position: sb"
        card1 = "4s"
        card2 = "3s"

        return render_template("index.html", title="CS136 Game", card1 = card1, card2 = card2, position = position)

    else:

        position = "Position: sb"
        card1 = "4s"
        card2 = "3s"

        return render_template("index.html", title="CS136 Game", card1 = card1, card2 = card2, position = position)

if __name__ == "__main__":
    app.run(debug=True)