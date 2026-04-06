from datetime import date
class Semester:

    def __init__(self, no:int, beginn:date, ende:date):
        self.no = no
        self.beginn = beginn
        self.ende = ende

    def anzahl_tage(self) -> int:
        return (self.ende - self.beginn).days
        
    def __str__(self):
        return f"Semester {self.no} {self.beginn} - {self.ende}"