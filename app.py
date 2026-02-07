from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    table = None
    num = None
    start_range = 1
    end_range = 10
    
    if request.method == "POST":
        num = int(request.form.get("number", 1))
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
    import os
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Flask app on port {port}")
    app.run(debug=False, host="0.0.0.0", port=port)