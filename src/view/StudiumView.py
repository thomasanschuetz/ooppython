from src.entity.Studium import Studium
from src.entity.Kurs import Kurs
from src.entity.Semester import Semester

from datetime import date, timedelta
from typing import List

class StudiumView:
    def __init__(self, studium:Studium, datum:date):
        self.studium = studium
        self.datum = datum
        self.anzahl_tage_gesamt = self.studium.anzahl_tage()
        self.vergangene_tage = self.studium.vergangene_tage(datum)
        self.verbleibende_tage = self.studium.verbleibende_tage(datum)
        self.kurse = [{
            'name': k.name,
            'hoehe_rel': k.anzahl_tage(),
            'beginn': k.beginn.isoformat(),
            'ende': k.ende.isoformat()
        } for k in studium.get_kurse()]

        self.semester = [{
            'name': str(s.no),
            'hoehe_rel': s.anzahl_tage()
        } for s in studium.semester]

        self.tage = self.erzeuge_tage()
        self.faellige_pruefungen = self.erzeuge_faellige_pruefungen()
        self.naechste_pruefungen = self.erzeuge_naechste_pruefungen()
        self.noten = self.erzeuge_noten()
        self.stats = self.erzeuge_stats()

    def erzeuge_stats(self):
        anzahl_kurse_soll = len(self.studium.kurse_soll(self.datum))
        anzahl_kurse_ist = len(self.studium.kurse_fertig())
        anzahl_ects_soll = self.studium.anzahl_ects_soll(self.datum)
        anzahl_ects_ist = self.studium.anzahl_ects_fertig()
        return {
            'anzahl_kurse': self.studium.anzahl_kurse(),
            'anzahl_ects': self.studium.anzahl_ects(),
            'anzahl_kurse_soll': anzahl_kurse_soll,
            'anzahl_ects_soll': anzahl_ects_soll,
            'kurse_ist': {'anzahl': anzahl_kurse_ist, 'ok': anzahl_kurse_ist >= anzahl_kurse_soll},
            'ects_ist': {'anzahl': anzahl_ects_ist, 'ok': anzahl_ects_ist >= anzahl_ects_soll}
        }

    def erzeuge_noten(self):
        ziel_note = self.studium.ziel_note
        durchnitt_note = self.studium.durchschnittsnote()
        benoetigt_note = self.studium.benoetigte_durchschnittsnote()
        
        if durchnitt_note is None:
            return {
            'ziel': self.formatiere_note(ziel_note),
            'aktuell': {
                'note': 'n.a.',
                'ok': True
            },
            'benoetigt': {
                'note': 'n.a.',
                'ok': True
            }
        }
        
        return {
            'ziel': ziel_note,
            'aktuell': {
                'note': self.formatiere_note(durchnitt_note),
                'ok': durchnitt_note <= ziel_note
            },
            'benoetigt': {
                'note': self.formatiere_note(benoetigt_note),
                'ok': benoetigt_note >= ziel_note
            }
        }

    def erzeuge_faellige_pruefungen(self):
        return [{
            'name': k.name,
            'faellig_seit_tage': -k.faellig_in_tagen(self.datum)
        } for k in self.studium.kurse_soll(self.datum)]
    
    def erzeuge_naechste_pruefungen(self):
        return [{
            'name': k.name,
            'faellig_in_tage': k.faellig_in_tagen(self.datum)
        } for k in self.studium.naechste_pruefungen(self.datum, 3)]

    def erzeuge_tage(self) -> List[str]:
         days = [self.studium.beginn + timedelta(days=i) for i in range(self.studium.anzahl_tage())]
         return [d for d in map(lambda d: {'tag': d.isoformat(), 'vergangen': d < self.datum}, days)]

    def formatiere_note(self, note:float) -> str:
        return f"{note:.2f}".replace('.', ',')
    