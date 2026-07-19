from dataclasses import dataclass


@dataclass
class StudiumStatistik:
    """
    Klasse zur Darstellung der Statistiken eines Studiums.
    
    Attribute:
        anzahl_kurse (int): Die Gesamtanzahl der Kurse.
        anzahl_kurse_soll (int): Die geplante Anzahl der Kurse.
        anzahl_kurse_ist (int): Die tatsächliche Anzahl der Kurse.
        anzahl_ects (float): Die Gesamtanzahl der ECTS-Punkte.
        anzahl_ects_soll (float): Die geplante Anzahl der ECTS-Punkte.
        anzahl_ects_ist (float): Die tatsächliche Anzahl der ECTS-Punkte.
        durchnitt_note (float): Die durchschnittliche Note.
        benoetigt_note (float): Die benötigte Note für das Ziel.
    """
    anzahl_kurse: int
    anzahl_kurse_soll: int
    anzahl_kurse_ist: int
    anzahl_ects: float
    anzahl_ects_soll: float
    anzahl_ects_ist: float
    durchnitt_note: float
    benoetigt_note: float
