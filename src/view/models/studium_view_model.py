from dataclasses import dataclass
from typing import List
from src.view.models.kurs_view_model import KursViewModel
from src.view.models.semester_view_model import SemesterViewModel
from src.view.models.pruefung_view_model import PruefungViewModel
from src.view.models.noten_view_model import NotenViewModel
from src.view.models.stats_view_model import StatsViewModel

@dataclass
class StudiumViewModel:
    """
    ViewModel für die Darstellung von Studiumsinformationen.
    
    Attribute:
        name (str): Der Name des Studiums.
        datum (str): Das aktuelle Datum.
        anzahl_tage_gesamt (int): Die Gesamtanzahl der Tage des Studiums.
        vergangene_tage (int): Die Anzahl der vergangenen Tage.
        verbleibende_tage (int): Die Anzahl der verbleibenden Tage.
        kurse (List[KursViewModel]): Die Liste der Kurse.
        semester (List[SemesterViewModel]): Die Liste der Semester.
        faellige_pruefungen (List[PruefungViewModel]): Die Liste der fälligen Prüfungen.
        naechste_pruefungen (List[PruefungViewModel]): Die Liste der nächsten Prüfungen.
        noten (NotenViewModel): Die Noteninformationen.
        stats (StatsViewModel): Die Statistikinformationen.
    """
    name: str
    datum: str
    anzahl_tage_gesamt: int
    vergangene_tage: int
    verbleibende_tage: int
    kurse: List[KursViewModel]
    semester: List[SemesterViewModel]
    faellige_pruefungen: List[PruefungViewModel]
    naechste_pruefungen: List[PruefungViewModel]
    noten: NotenViewModel
    stats: StatsViewModel
