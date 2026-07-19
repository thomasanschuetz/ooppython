from dataclasses import dataclass

@dataclass
class PruefungViewModel:
    """
    ViewModel für die Darstellung von Prüfungsinformationen.
    
    Attribute:
        name (str): Der Name der Prüfung.
        faellig_seit_tage (int | None): Die Anzahl der Tage, seit der die Prüfung fällig ist.
        faellig_in_tage (int | None): Die Anzahl der Tage, bis die Prüfung fällig ist.
    """
    name: str
    faellig_seit_tage: int | None = None
    faellig_in_tage: int | None = None
