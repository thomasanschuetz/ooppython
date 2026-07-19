from dataclasses import dataclass

@dataclass
class PruefungViewModel:
    name: str
    faellig_seit_tage: int | None = None
    faellig_in_tage: int | None = None
