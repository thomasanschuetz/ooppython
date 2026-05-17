from src.repo.studium_repository import StudiumRepository
from src.service.studium_planung_service import StudiumPlanungService
from src.controller.dashboard_controller import DashboardController


from datetime import date
from dateutil.relativedelta import relativedelta
from flask import Flask, request, render_template, redirect
app = Flask(__name__)

today = date.today() + relativedelta(days=250)

studium_planning_service = StudiumPlanungService()
studium_repo = StudiumRepository('data/studium.pkl')
dashboard_controller = DashboardController(studium_planning_service, studium_repo, today)


@app.route("/")
def dashboard() -> str:
    studium_view = dashboard_controller.lade_dashboard_view()
    return render_template('dashboard.html', studium=studium_view)

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

    studium.name = name
    studium.beginn = beginn
    studium.ziel_monate = ziel_monate
    studium.ziel_note = ziel_note
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
        
    noten = []
    note1 = p.get('note1')
    note2 = p.get('note2')
    note3 = p.get('note3')
    if note1:
        noten.append(float(note1))
        if note2:
            noten.append(float(note2))
            if note3:
                noten.append(float(note3))
    
    #todo validieren
    studium.set_kurs_data(kurs_id, name, ects, schwere, noten)
    

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
    app.run(debug=True)