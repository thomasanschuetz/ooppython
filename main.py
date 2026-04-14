from src.entity.Studium import Studium
from src.entity.Kurs import Kurs
from src.view.StudiumView import StudiumView

from datetime import date
from dateutil.relativedelta import relativedelta
from flask import Flask, request, render_template
app = Flask(__name__)


studium = None
studium_view = None


@app.route("/")
def dashboard() -> str:



    return render_template('dashboard.html', studium_name=studium.name, studium=studium_view)

@app.route("/update_studium", methods=["GET"])
def get_update_studium() -> str:
    return (
        '<form method="POST">'
        '<input type="text" name="name" />'
        '</form>'
    )
    

def create_course():
    return 'create_course'


if __name__ == "__main__":

    kurse = [Kurs(str(k+1), f"kurs {k+1}", k//6 + 1, 3, 5) for k in range(15)]
    
    
    kurse[0].schwere = 6
    kurse[1].note = 3.0
    kurse[12].ects = 10
    kurse[13].ects = 10
    kurse[14].ects = 10
    kurse[12].schwere = 9
    kurse[13].schwere = 9
    kurse[14].schwere = 12
    studium = Studium("KI", date.today(), 39, 2.0, kurse)
    studium_view = StudiumView(studium, date.today() + relativedelta(days=250))





    app.run(debug=True)