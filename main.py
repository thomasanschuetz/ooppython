from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def home() -> str:
    return (
        "<h1>Übersicht</h1>"
        '<a href="/create_studies">Neues Studium</a>'
    )

@app.route("/create_studies", methods=["GET"])
def get_create_studies() -> str:
    return (
        '<form method="POST">'
        '<input type="text" name="name" />'
        '</form>'
    )
    
@app.route("/create_studies", methods=["POST"])
def post_create_studies() -> str:
    name = request.form.get('name')
    return (
        'Post done: ' + name
    )


def create_course():
    return 'create_course'


if __name__ == "__main__":
    app.run(debug=True)