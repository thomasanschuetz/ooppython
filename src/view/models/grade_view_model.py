from dataclasses import dataclass

@dataclass
class GradeViewModel:
    """View model for grade/note information"""
    ziel: str
    aktuell: dict[str, str | bool]  # {'note': str, 'ok': bool}
    benoetigt: dict[str, str | bool]  # {'note': str, 'ok': bool}
