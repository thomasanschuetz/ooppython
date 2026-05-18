from dataclasses import dataclass
from typing import List

@dataclass
class KursView:
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