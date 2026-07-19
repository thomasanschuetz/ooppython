from dataclasses import dataclass

@dataclass
class NotenViewModel:
    """
    ViewModel für die Darstellung von Noteninformationen.
    
    Attribute:
        ziel (str): Die angestrebte Durchschnittsnote.
        aktuell (dict[str, str | bool]): Die aktuelle Durchschnittsnote und ob sie okay ist.
        benoetigt (dict[str, str | bool]): Die benötigte Durchschnittsnote und ob sie okay ist.
    """
    ziel: str
    aktuell: dict[str, str | bool]  # {'note': str, 'ok': bool}
    benoetigt: dict[str, str | bool]  # {'note': str, 'ok': bool}
