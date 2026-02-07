from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    table = None
    num = None
    start_range = 1
    end_range = 10
    
    if request.method == "POST":
        num = int(request.form.get("number"))
        start_range = int(request.form.get("start_range", 1))
        end_range = int(request.form.get("end_range", 10))
        
        # Validate ranges
        if start_range < 1:
            start_range = 1
        if end_range < start_range:
            end_range = start_range + 10
        if end_range > 100:
            end_range = 100
        
        table = [(num, i, num * i) for i in range(start_range, end_range + 1)]
    
    return render_template("index.html", table=table, num=num, start_range=start_range, end_range=end_range)

if __name__ == "__main__":
    # For production, debug is set to False, and host is set to '0.0.0.0' to allow external access
    app.run(debug=False, host="0.0.0.0")