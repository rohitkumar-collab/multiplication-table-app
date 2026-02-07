from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return """
    <html>
    <head><title>Multiplication Table App</title></head>
    <body style="font-family: Arial; text-align: center; padding: 50px;">
        <h1>Hello! App is working!</h1>
        <p>If you see this, Render deployment is working.</p>
    </body>
    </html>
    """

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
