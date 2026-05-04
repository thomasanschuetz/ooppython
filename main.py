from src.entity.Studium import Studium
from src.entity.Kurs import Kurs
from src.view.StudiumView import StudiumView
#from src.service.StudiumService import StudiumService
from src.repo.StudiumRepo import StudiumRepo
from datetime import date
from dateutil.relativedelta import relativedelta
from flask import Flask, request, render_template, redirect
app = Flask(__name__)


studium = None
studium_view = None
studium_service = None
studium_repo = None
today = date.today() + relativedelta(days=250) # todo change to today


@app.route("/")
def dashboard() -> str:
    print('rendering')
    print(studium_view)
    return render_template('dashboard.html', studium_name=studium.name, studium=studium_view)

@app.route("/update_studium", methods=["GET"])
def get_update_studium() -> str:
    return render_template('update_studium.html', 
        name=studium.name,
        beginn=studium.beginn.isoformat(),
        ziel_note=studium.ziel_note,
        ziel_monate=studium.ziel_monate
    )
@app.route("/update_studium", methods=["POST"])
def post_update_studium() -> str:
    global studium_view
    #todo validieren
    p = request.form
    name = p.get('name')
    beginn = date.fromisoformat(p.get('beginn'))
    ziel_note = float(p.get('ziel_note'))
    ziel_monate = int(p.get('ziel_monate'))

    studium.set_name(name)
    studium.set_beginn(beginn)
    studium.set_ziel_monate(ziel_monate)
    studium.set_ziel_note(ziel_note)
    studium_repo.save(studium)
    studium_view = StudiumView(studium, today) # set_studium um global unnötig zu machen

    return redirect('/')

@app.route("/bewege_kurs", methods=["POST"])
def bewege_kurs() -> str:
    global studium_view

    p = request.form
    kurs_id = p.get('kurs_id')
    hoch = p.get('richtung') == 'hoch'
    studium.bewege_kurs(kurs_id, hoch)
    studium_repo.save(studium)
    studium_view = StudiumView(studium, today) # set_studium um global unnötig zu machen

    return redirect('/')

@app.route("/bearbeite_kurs", methods=["GET"])
def get_bearbeite_kurs() -> str:

    g = request.args
    kurs_id = g.get('id')
    kurs = studium_view.get_kurs(kurs_id)
    #todo validation
    return render_template("bearbeite_kurs.html", kurs=kurs)

@app.route("/bearbeite_kurs", methods=["POST"])
def post_bearbeite_kurs() -> str:
    global studium_view

    p = request.form
    kurs_id = p.get('id')
    name = p.get('name')
    ects = int(p.get('ects'))
    schwere = int(p.get('schwere'))
    #todo validieren
    studium.set_kurs_data(kurs_id, name, ects, schwere)
    studium_repo.save(studium)
    studium_view = StudiumView(studium, today) # set_studium um global unnötig zu machen

    return redirect('/')


@app.route("/erstelle_kurs", methods=["GET"])
def get_erstelle_kurs() -> str:

    return render_template("erstelle_kurs.html", kurs={'name': '', 'ects': 5, 'schwere': 3})

@app.route("/erstelle_kurs", methods=["POST"])
def post_erstelle_kurs() -> str:
    global studium_view

    p = request.form
    name = p.get('name')
    ects = int(p.get('ects'))
    schwere = int(p.get('schwere'))
    #todo validieren
    studium.add_kurs(name, ects, schwere)
    studium_repo.save(studium)
    studium_view = StudiumView(studium, today) # set_studium um global unnötig zu machen

    return redirect('/')



if __name__ == "__main__":

    studium_repo = StudiumRepo('data/studium.pkl')

    kurse = [Kurs(str(k+1), f"kurs {k+1}", 3, 5) for k in range(15)]
    kurse[0].schwere = 5
    kurse[1].note = 3.0
    kurse[12].ects = 10
    kurse[13].ects = 10
    kurse[14].ects = 10
    kurse[12].schwere = 4
    kurse[13].schwere = 4
    kurse[14].schwere = 5
    studium = Studium("KI", date.today(), 39, 2.0, kurse)


    
    studium = studium_repo.load()
    
    studium_view = StudiumView(studium, today)
    

    app.run(debug=True)