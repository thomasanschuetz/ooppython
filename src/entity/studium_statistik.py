from dataclasses import dataclass

@dataclass
class StudiumStatistik:
    anzahl_kurse: int
    anzahl_kurse_soll: int
    anzahl_kurse_ist: int
    anzahl_ects: float
    anzahl_ects_soll: float
    anzahl_ects_ist: float
    durchnitt_note: float
    benoetigt_note: float
