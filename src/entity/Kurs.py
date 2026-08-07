from dataclasses import dataclass, field
from datetime import date
from src.entity.enums import KursSchwere, KursStatus

@dataclass
class Kurs:
    """
    Klasse zur Darstellung eines Kurses.
    
    Attribute:
        id (str): Eindeutige ID des Kurses.
        name (str): Name des Kurses.
        ects (int): ECTS-Punkte des Kurses.
        schwere (KursSchwere): Schwierigkeit des Kurses.
        noten (list): Liste der Noten des Kurses.
        beginn (date | None): Beginn des Kurses.
        ende (date | None): Ende des Kurses.
    """
    id: str
    name: str = ''
    ects: int = 5
    schwere: KursSchwere = KursSchwere.MITTEL
    noten: list = field(default_factory=list)
    beginn: date|None = None
    ende: date|None = None


    def berechne_status(self, datum: date) -> KursStatus:
        """
        Bestimmt den Status des Kurses basierend auf dem aktuellen Datum.
        
        Args:
            datum (date): Das aktuelle Datum.
            
        Returns:
            KursStatus: Der Status des Kurses.
        """
        if self.beginn is None or self.ende is None:
            return KursStatus.UNGEPLANT
        
        elif self.ist_fertig():
            return KursStatus.FERTIG
        
        elif self.ist_faellig(datum):
            return KursStatus.FAELLIG

        elif self.ist_aktiv(datum): # muss nach ist_faellig bleiben, da faellig -> aktiv impliziert
            return KursStatus.AKTIV
        
        else:
            return KursStatus.OFFEN
     

    @property
    def anzahl_tage(self) -> int|None:
        """
        Berechnet die Anzahl der Tage des Kurses.
        
        Returns:
            int | None: Die Anzahl der Tage oder None, falls Beginn oder Ende nicht gesetzt sind.
        """
        if not self._hat_start_und_ende():
            return None
        
        return (self.ende - self.beginn).days + 1
    

    def faellig_in_tagen(self, datum: date) -> int:
        """
        Berechnet die Anzahl der Tage bis der Kurs fällig ist.
        
        Args:
            datum (date): Das aktuelle Datum.
            
        Returns:
            int: Die Anzahl der Tage bis der Kurs fällig ist.
        """
        if not self._hat_start_und_ende(): 
            return 0
        
        return (self.ende - datum).days
    
    def kann_note_hinzufuegen(self) -> bool:
        """
        Prüft, ob eine weitere Note hinzugefügt werden kann.
        
        Returns:
            bool: True, wenn eine weitere Note hinzugefügt werden kann, False sonst.
        """
        return len(self.noten) < 3 and not self.ist_fertig()
   

    def ist_fertig(self) -> bool:
        """
        Prüft, ob der Kurs erfolgreich abgeschlossen wurde.
        
        Returns:
            bool: True, wenn der Kurs erfolgreich abgeschlossen wurde, False sonst.
        """
        for note in self.noten:
            if note <= 4.0:
                return True

    @property        
    def note(self) -> None|float:
        """
        Gibt die letzte Note des Kurses zurück.
        
        Returns:
            None | float: Die letzte Note oder None, falls keine Noten vorhanden sind.
        """
        if not self.noten:
            return None
        
        return self.noten[-1]
        

    def ist_aktiv(self, datum: date) -> bool:
        """
        Prüft, ob der Kurs aktuell aktiv ist.
        
        Args:
            datum (date): Das aktuelle Datum.
            
        Returns:
            bool: True, wenn der Kurs aktiv ist, False sonst.
        """
        if not self._hat_start_und_ende():
            return False
        return (not self.ist_faellig(datum)) and (not self.ist_fertig()) and self.beginn <= datum and datum <= self.ende


    def ist_faellig(self, datum: date) -> bool:
        """
        Prüft, ob der Kurs fällig ist.
        
        Args:
            datum (date): Das aktuelle Datum.
            
        Returns:
            bool: True, wenn der Kurs fällig ist, False sonst.
        """
        if not self._hat_start_und_ende():
            return False
        return (not self.ist_fertig()) and self.ende < datum
    
    def _hat_start_und_ende(self) -> bool:
        """
        Prüft, ob Beginn und Ende des Kurses gesetzt sind.
        
        Returns:
            bool: True, wenn Beginn und Ende gesetzt sind, False sonst.
        """
        return not(self.beginn is None or self.ende is None)