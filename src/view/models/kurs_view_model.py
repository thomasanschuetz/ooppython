from dataclasses import dataclass
from typing import List

@dataclass
class KursViewModel:
    """
    ViewModel für die Darstellung von Kursinformationen.
    
    Attribute:
        id (str): Eindeutige ID des Kurses.
        name (str): Name des Kurses.
        schwere (str): Schwierigkeit des Kurses.
        ects (str): ECTS-Punkte des Kurses.
        anzahl_tage (str): Anzahl der Tage des Kurses.
        hoehe_rel (str): Relative Höhe des Kurses.
        beginn (str): Beginn des Kurses.
        ende (str): Ende des Kurses.
        ist_fertig (bool): Gibt an, ob der Kurs abgeschlossen ist.
        ist_faellig (bool): Gibt an, ob der Kurs fällig ist.
        ist_aktiv (bool): Gibt an, ob der Kurs aktiv ist.
        note (str): Die Note des Kurses.
        noten (List[str]): Die Liste der Noten des Kurses.
        zeige_note2 (bool): Gibt an, ob die zweite Note angezeigt werden soll.
        zeige_note3 (bool): Gibt an, ob die dritte Note angezeigt werden soll.
    """
    id: str
    name: str
    schwere: str
    ects: str
    anzahl_tage: str
    hoehe_rel: str
    beginn: str
    ende: str
    ist_fertig: bool
    ist_faellig: bool
    ist_aktiv: bool
    note: str
    noten: List[str]
    zeige_note2: bool
    zeige_note3: bool
