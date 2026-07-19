from enum import Enum, IntEnum

class KursSchwere(IntEnum):
    """
    Enum für die Schwierigkeit eines Kurses.
    
    Attribute:
        SEHR_LEICHT (int): Sehr leicht.
        LEICHT (int): Leicht.
        MITTEL (int): Mittel.
        SCHWER (int): Schwer.
        SEHR_SCHWER (int): Sehr schwer.
    """
    SEHR_LEICHT = 1
    LEICHT = 2
    MITTEL = 3
    SCHWER = 4
    SEHR_SCHWER = 5

class KursStatus(Enum):
    """
    Enum für den Status eines Kurses.
    
    Attribute:
        UNGEPLANT (str): Der Kurs ist noch nicht geplant.
        OFFEN (str): Der Kurs ist geplant, aber noch nicht aktiv.
        AKTIV (str): Der Kurs ist aktuell aktiv.
        FAELLIG (str): Der Kurs ist fällig und automatisch aktiv.
        FERTIG (str): Der Kurs ist abgeschlossen.
    """
    UNGEPLANT = "ungeplant"
    OFFEN = "offen"
    AKTIV = "aktiv"
    FAELLIG = "faellig" # ist dann automatisch aktiv
    FERTIG = "fertig"