from flask import Flask


app = Flask(__name__)
@app.route("/") #"@" this is decorator
@app.route("/index")
def index():

    return "Hello world from CTC"

app.run(debug=True)
