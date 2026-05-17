from datetime import date, timedelta
from typing import List

from src.entity.studium import Studium
from src.entity.kurs import Kurs
from src.entity.semester import Semester
from src.entity.enums import KursStatus
from src.entity.studium_statistik import StudiumStatistik

class StudiumView:
    def __init__(self, studium:Studium, statistik: StudiumStatistik, semester: List[Semester], datum:date):
        self.studium = studium
        self.statistik = statistik
        self.name = studium.name
        self.datum = datum
        self.anzahl_tage_gesamt = self.studium.anzahl_tage
        self.vergangene_tage = self.studium.vergangene_tage(datum)
        self.verbleibende_tage = self.studium.verbleibende_tage(datum)
        
        self.erzeuge_kurse()
        self.semester = [{
            'name': str(s.no),
            'hoehe_rel': s.anzahl_tage()
        } for s in semester]

        self.faellige_pruefungen = self.erzeuge_faellige_pruefungen()
        self.naechste_pruefungen = self.erzeuge_naechste_pruefungen()
        self.noten = self.erzeuge_noten()
        self.stats = self.erzeuge_stats()

    def erzeuge_stats(self):
        anzahl_kurse_soll = self.statistik.anzahl_kurse_soll
        anzahl_kurse_ist = self.statistik.anzahl_kurse_ist
        anzahl_ects_soll = self.statistik.anzahl_ects_soll
        anzahl_ects_ist = self.statistik.anzahl_ects_ist
        return {
            'anzahl_kurse': self.statistik.anzahl_kurse,
            'anzahl_ects': self.statistik.anzahl_ects,
            'anzahl_kurse_soll': anzahl_kurse_soll,
            'anzahl_ects_soll': anzahl_ects_soll,
            'kurse_ist': {'anzahl': anzahl_kurse_ist, 'ok': anzahl_kurse_ist >= anzahl_kurse_soll},
            'ects_ist': {'anzahl': anzahl_ects_ist, 'ok': anzahl_ects_ist >= anzahl_ects_soll}
        }

    def erzeuge_kurse(self):
                
        self.kurse = []

        for k in self.studium.kurse:

            status = k.get_status(self.datum)

            self.kurse.append({
                'id': k.id,
                'name': k.name,
                'schwere': k.schwere,
                'ects': k.ects,
                'anzahl_tage': k.anzahl_tage,
                'hoehe_rel': k.anzahl_tage,
                'beginn': k.beginn.isoformat(),
                'ende': k.ende.isoformat(),
                'ist_fertig': status == KursStatus.FERTIG,
                'ist_faellig': status == KursStatus.FAELLIG,
                'ist_aktiv': status == KursStatus.AKTIV,
                'note': self.formatiere_note(k.note),
                'noten': [str(note) for note in k.noten],
                'noten-formatiert': [self.formatiere_note(note) for note in k.noten],
                'zeige_note2': len(k.noten) >= 1,
                'zeige_note3': len(k.noten) >= 2
            })

    def erzeuge_noten(self):
        ziel_note = self.studium.ziel_note
        durchnitt_note = self.statistik.durchnitt_note
        benoetigt_note = self.statistik.benoetigt_note
        
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
        } for k in self.studium.kurse if k.get_status(self.datum) == KursStatus.FAELLIG]
    
    def erzeuge_naechste_pruefungen(self):
        return [{
            'name': k.name,
            'faellig_in_tage': k.faellig_in_tagen(self.datum)
        } for k in self.studium.kurse if k.get_status(self.datum) == KursStatus.OFFEN][:3]

    def formatiere_note(self, note:float|None) -> str:
        if not note:
            return ''
        return f"{note:.2f}".replace('.', ',')
    
    def get_kurs(self, kurs_id: str) -> dict|None:
        return next((kurs for kurs in self.kurse if kurs['id'] == kurs_id))
    
    def __str__(self):
        return f"{self.name}"
    