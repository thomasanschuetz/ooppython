from typing import List

class Course:
    
    def __init__(self, name:str, semester:int):
        self.name = name
        self.semester = semester

class Studies:

    def __init__(self, name:str, courses:List[Course]):
        self.courses = []
        self.name = name