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

    def erzeuge_tage(self)->List[str]:
         days = [self.studium.beginn + timedelta(days=i) for i in range(self.studium.anzahl_tage())]
         return [d for d in map(lambda d: {'tag': d.isoformat(), 'vergangen': d < self.datum}, days)]

    
    