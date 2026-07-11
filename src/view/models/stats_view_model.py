from dataclasses import dataclass

@dataclass
class StatsViewModel:
    """View model for statistics information"""
    anzahl_kurse: int
    anzahl_ects: float
    anzahl_kurse_soll: int
    anzahl_ects_soll: float
    kurse_ist: dict[str, int | bool]  # {'anzahl': int, 'ok': bool}
    ects_ist: dict[str, float | bool]  # {'anzahl': float, 'ok': bool}
