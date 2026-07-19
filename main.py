# Hauptdatei für die Flask-Anwendung zur Verwaltung eines Studiums.
# Diese Datei enthält die Routen und die Hauptlogik der Webanwendung.
from src.repo.studium_repository import StudiumRepository
from src.service.studium_planung_service import StudiumPlanungService
from src.controller.dashboard_controller import DashboardController
from src.validation.validator import Validator
from src.entity.enums import KursSchwere

from datetime import date
from flask import Flask, request, render_template, redirect, flash

# Initialisierung der Flask-Anwendung
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

today = date.today()

# Initialisierung der Services und Controller
studium_planning_service = StudiumPlanungService()
studium_repo = StudiumRepository('data/studium.json')
dashboard_controller = DashboardController(studium_planning_service, studium_repo, today)


@app.route("/")
def dashboard() -> str:
    """
    Zeigt das Dashboard der Anwendung an.
    
    Returns:
        str: Gerenderte HTML-Seite des Dashboards.
    """
    studium_view = dashboard_controller.lade_studium_view()
    return render_template('dashboard.html', studium=studium_view)


@app.route("/update_studium", methods=["GET"])
def get_update_studium() -> str:
    """
    Zeigt das Formular zum Aktualisieren des Studiums an.
    
    Returns:
        str: Gerenderte HTML-Seite des Aktualisierungsformulars.
    """
    studium = dashboard_controller.lade_studium()
    
    return render_template('update_studium.html', 
        name=studium.name,
        beginn=studium.beginn.isoformat(),
        ziel_note=studium.ziel_note,
        ziel_monate=studium.ziel_monate
    )


@app.route("/update_studium", methods=["POST"])
def post_update_studium() -> str:
    """
    Verarbeitet das Formular zum Aktualisieren des Studiums.
    
    Returns:
        str: Weiterleitung zur Startseite nach erfolgreicher Aktualisierung.
    """
    p = request.form
    name = p.get('name')
    beginn = p.get('beginn')
    ziel_note = p.get('ziel_note')
    ziel_monate = p.get('ziel_monate')

    errors = Validator.validiere_studium(name, beginn, float(ziel_note) if ziel_note else None, int(ziel_monate) if ziel_monate else None)
    if errors:
        for error in errors:
            flash(error, 'error')
        return render_template('update_studium.html', 
            name=name,
            beginn=beginn,
            ziel_note=ziel_note,
            ziel_monate=ziel_monate
        )

    studium = dashboard_controller.lade_studium()
    studium.name = name
    studium.beginn = date.fromisoformat(beginn)
    studium.ziel_monate = int(ziel_monate)
    studium.ziel_note = float(ziel_note)
    studium_repo.speichere_studium(studium)

    return redirect('/')


@app.route("/bewege_kurs", methods=["POST"])
def bewege_kurs() -> str:
    """
    Verschiebt einen Kurs in eine andere Richtung (hoch oder runter).
    
    Returns:
        str: Weiterleitung zur Startseite nach erfolgreicher Verschiebung.
    """
    p = request.form
    
    kurs_id = p.get('kurs_id')
    hoch = p.get('richtung') == 'hoch'

    dashboard_controller.verschiebe_kurs(kurs_id, hoch)
    return redirect('/')


@app.route("/bearbeite_kurs", methods=["GET"])
def get_bearbeite_kurs() -> str:
    """
    Zeigt das Formular zum Bearbeiten eines Kurses an.
    
    Returns:
        str: Gerenderte HTML-Seite des Bearbeitungsformulars.
    """
    g = request.args
    kurs_id = g.get('id')
    kurs_view = dashboard_controller.lade_kurs_view(kurs_id)
    
    return render_template("bearbeite_kurs.html", kurs=kurs_view, KursSchwere=KursSchwere)


@app.route("/bearbeite_kurs", methods=["POST"])
def post_bearbeite_kurs() -> str:
    """
    Verarbeitet das Formular zum Bearbeiten eines Kurses.
    
    Returns:
        str: Weiterleitung zur Startseite nach erfolgreicher Aktualisierung.
    """
    p = request.form
    kurs_id = p.get('id')
    name = p.get('name')
    ects = p.get('ects')
    schwere = p.get('schwere')
        
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
    
    errors = Validator.validiere_kurs(name, int(ects) if ects else None, int(schwere) if schwere else None)
    errors.extend(Validator.validiere_noten(noten))
    if errors:
        for error in errors:
            flash(error, 'error')
        kurs_view = dashboard_controller.lade_kurs_view(kurs_id)
        return render_template("bearbeite_kurs.html", kurs=kurs_view, errors=errors, KursSchwere=KursSchwere)

    dashboard_controller.aktualisiere_kurs(kurs_id, name, int(ects), int(schwere), noten)

    return redirect('/')


@app.route("/erstelle_kurs", methods=["GET"])
def get_erstelle_kurs() -> str:
    """
    Zeigt das Formular zum Erstellen eines neuen Kurses an.
    
    Returns:
        str: Gerenderte HTML-Seite des Erstellungsformulars.
    """
    return render_template("erstelle_kurs.html", kurs={'name': '', 'ects': 5, 'schwere': 3}, KursSchwere=KursSchwere)


@app.route("/erstelle_kurs", methods=["POST"])
def post_erstelle_kurs() -> str:
    """
    Verarbeitet das Formular zum Erstellen eines neuen Kurses.
    
    Returns:
        str: Weiterleitung zur Startseite nach erfolgreicher Erstellung.
    """
    p = request.form
    name = p.get('name')
    ects = p.get('ects')
    schwere = p.get('schwere')

    errors = Validator.validiere_kurs(name, int(ects) if ects else None, int(schwere) if schwere else None)
    if errors:
        for error in errors:
            flash(error, 'error')
        return render_template("erstelle_kurs.html", kurs={'name': name, 'ects': ects, 'schwere': schwere}, errors=errors, KursSchwere=KursSchwere)

    dashboard_controller.erstelle_kurs(name, int(ects), int(schwere))
    
    return redirect('/')


if __name__ == "__main__":
    """
    Startet die Flask-Anwendung im Debug-Modus.
    """
    app.run(debug=True)