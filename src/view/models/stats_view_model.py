from dataclasses import dataclass

@dataclass
class StatsViewModel:
    """
    ViewModel für die Darstellung von Statistikinformationen.
    
    Attribute:
        anzahl_kurse (int): Die Gesamtanzahl der Kurse.
        anzahl_ects (float): Die Gesamtanzahl der ECTS-Punkte.
        anzahl_kurse_soll (int): Die geplante Anzahl der Kurse.
        anzahl_ects_soll (float): Die geplante Anzahl der ECTS-Punkte.
        kurse_ist (dict[str, int | bool]): Die tatsächliche Anzahl der Kurse und ob sie okay ist.
        ects_ist (dict[str, float | bool]): Die tatsächliche Anzahl der ECTS-Punkte und ob sie okay ist.
    """
    anzahl_kurse: int
    anzahl_ects: float
    anzahl_kurse_soll: int
    anzahl_ects_soll: float
    kurse_ist: dict[str, int | bool]  # {'anzahl': int, 'ok': bool}
    ects_ist: dict[str, float | bool]  # {'anzahl': float, 'ok': bool}
