from datetime import date


class Semester:
    """
    Klasse zur Darstellung eines Semesters.
    
    Attribute:
        no (int): Die Nummer des Semesters.
        beginn (date): Der Beginn des Semesters.
        ende (date): Das Ende des Semesters.
    """

    def __init__(self, no:int, beginn:date, ende:date):
        """
        Initialisiert ein Semester.
        
        Args:
            no (int): Die Nummer des Semesters.
            beginn (date): Der Beginn des Semesters.
            ende (date): Das Ende des Semesters.
        """
        self.no = no
        self.beginn = beginn
        self.ende = ende

    def anzahl_tage(self) -> int:
        """
        Berechnet die Anzahl der Tage des Semesters.
        
        Returns:
            int: Die Anzahl der Tage.
        """
        return (self.ende - self.beginn).days
        
    def __str__(self):
        """
        Gibt eine String-Darstellung des Semesters zurück.
        
        Returns:
            str: Die String-Darstellung des Semesters.
        """
        return f"Semester {self.no} {self.beginn} - {self.ende}"