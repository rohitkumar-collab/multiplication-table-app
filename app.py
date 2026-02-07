from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    table = None
    if request.method == "POST":
        num = int(request.form.get("number"))
        table = [(num, i, num * i) for i in range(1, 11)]  # Generate the table
    return render_template("index.html", table=table)

if __name__ == "__main__":
    # For production, debug is set to False, and host is set to '0.0.0.0' to allow external access
    app.run(debug=False, host="0.0.0.0")