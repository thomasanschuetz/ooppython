from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hallo Welt!</h1>"

@app.route("/create_studies")
def create_studies():
    return 'create_studies'

def create_course():
    return 'create_course'


if __name__ == "__main__":
    app.run(debug=True)