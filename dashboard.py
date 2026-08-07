from datetime import date
from flask import Flask, request, render_template, redirect, flash
from src.repo.studium_repository import StudiumRepository
from src.service.studium_planung_service import StudiumPlanungService
from src.controller.dashboard_controller import DashboardController
from src.validation.validator import Validator
from src.entity.enums import KursSchwere

class WebApplication:
    def __init__(self, repo_pfad: str):
        self.app = Flask(__name__)
        
        self.today = date.today()
        self.studium_repo = StudiumRepository(repo_pfad)
        self.studium_planning_service = StudiumPlanungService()
        self.dashboard_controller = DashboardController(
            self.studium_planning_service, 
            self.studium_repo, 
            self.today
        )
        
        self._registriere_routen()

    def _registriere_routen(self):
        
        self.app.add_url_rule("/", "dashboard", self.dashboard, methods=["GET"])
        self.app.add_url_rule("/update_studium", "get_update_studium", self.get_update_studium, methods=["GET"])
        self.app.add_url_rule("/update_studium", "post_update_studium", self.post_update_studium, methods=["POST"])
        self.app.add_url_rule("/bewege_kurs", "bewege_kurs", self.bewege_kurs, methods=["POST"])
        self.app.add_url_rule("/bearbeite_kurs", "get_bearbeite_kurs", self.get_bearbeite_kurs, methods=["GET"])
        self.app.add_url_rule("/bearbeite_kurs", "post_bearbeite_kurs", self.post_bearbeite_kurs, methods=["POST"])
        self.app.add_url_rule("/erstelle_kurs", "get_erstelle_kurs", self.get_erstelle_kurs, methods=["GET"])
        self.app.add_url_rule("/erstelle_kurs", "post_erstelle_kurs", self.post_erstelle_kurs, methods=["POST"])

    def dashboard(self) -> str:
        studium_view = self.dashboard_controller.lade_studium_view()
        return render_template('dashboard.html', studium=studium_view)

    def get_update_studium(self) -> str:
        studium = self.dashboard_controller.lade_studium()
        return render_template('update_studium.html', 
            name=studium.name,
            beginn=studium.beginn.isoformat(),
            ziel_note=studium.ziel_note,
            ziel_monate=studium.ziel_monate
        )

    def post_update_studium(self) -> str:
        p = request.form
        name = p.get('name')
        beginn = p.get('beginn')
        ziel_note = p.get('ziel_note')
        ziel_monate = p.get('ziel_monate')

        errors = Validator.validiere_studium(
            name, beginn, 
            float(ziel_note) if ziel_note else None, 
            int(ziel_monate) if ziel_monate else None
        )
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('update_studium.html', name=name, beginn=beginn, ziel_note=ziel_note, ziel_monate=ziel_monate)

        studium = self.dashboard_controller.lade_studium()
        studium.name = name
        studium.beginn = date.fromisoformat(beginn)
        studium.ziel_monate = int(ziel_monate)
        studium.ziel_note = float(ziel_note)
        self.studium_repo.speichere_studium(studium)

        return redirect('/')

    def bewege_kurs(self) -> str:
        p = request.form
        kurs_id = p.get('kurs_id')
        hoch = p.get('richtung') == 'hoch'
        self.dashboard_controller.verschiebe_kurs(kurs_id, hoch)
        return redirect('/')

    def get_bearbeite_kurs(self) -> str:
        g = request.args
        kurs_id = g.get('id')
        kurs_view = self.dashboard_controller.lade_kurs_view(kurs_id)
        return render_template("bearbeite_kurs.html", kurs=kurs_view, KursSchwere=KursSchwere)

    def post_bearbeite_kurs(self) -> str:
        p = request.form
        kurs_id = p.get('id')
        name = p.get('name')
        ects = p.get('ects')
        schwere = p.get('schwere')
            
        noten = []
        for key in ['note1', 'note2', 'note3']:
            val = p.get(key)
            if val:
                noten.append(float(val))
        
        errors = Validator.validiere_kurs(name, int(ects) if ects else None, int(schwere) if schwere else None)
        errors.extend(Validator.validiere_noten(noten))
        if errors:
            for error in errors:
                flash(error, 'error')
            kurs_view = self.dashboard_controller.lade_kurs_view(kurs_id)
            return render_template("bearbeite_kurs.html", kurs=kurs_view, errors=errors, KursSchwere=KursSchwere)

        self.dashboard_controller.aktualisiere_kurs(kurs_id, name, int(ects), int(schwere), noten)
        return redirect('/')

    def get_erstelle_kurs(self) -> str:
        return render_template("erstelle_kurs.html", kurs={'name': '', 'ects': 5, 'schwere': 3}, KursSchwere=KursSchwere)

    def post_erstelle_kurs(self) -> str:
        p = request.form
        name = p.get('name')
        ects = p.get('ects')
        schwere = p.get('schwere')

        errors = Validator.validiere_kurs(name, int(ects) if ects else None, int(schwere) if schwere else None)
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template("erstelle_kurs.html", kurs={'name': name, 'ects': ects, 'schwere': schwere}, errors=errors, KursSchwere=KursSchwere)

        self.dashboard_controller.erstelle_kurs(name, int(ects), int(schwere))
        return redirect('/')

    def run(self, debug=True):
        self.app.run(debug=True)

if __name__ == "__main__":
    web_app = WebApplication('data/studium.json')
    web_app.run(debug=True)