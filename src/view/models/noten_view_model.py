from dataclasses import dataclass

@dataclass
class NotenViewModel:
    ziel: str
    aktuell: dict[str, str | bool]  # {'note': str, 'ok': bool}
    benoetigt: dict[str, str | bool]  # {'note': str, 'ok': bool}
