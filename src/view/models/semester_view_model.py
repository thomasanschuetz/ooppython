from dataclasses import dataclass

@dataclass
class SemesterViewModel:
    """
    ViewModel für die Darstellung von Semesterinformationen.
    
    Attribute:
        name (str): Der Name des Semesters.
        hoehe_rel (int): Die relative Höhe des Semesters.
    """
    name: str
    hoehe_rel: int
