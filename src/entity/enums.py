from enum import Enum, IntEnum

class KursSchwere(IntEnum):
    EINS = 1
    ZWEI = 2
    DREI = 3
    VIER = 4
    FUENF = 5

class KursStatus(Enum):
    UNGEPLANT = "ungeplant"
    OFFEN = "offen"
    AKTIV = "aktiv"
    FAELLIG = "faellig" # ist dann automatisch aktiv
    FERTIG = "fertig"