import datetime

class Course:

    def __init__(self, name:str, semester:int, deadline:datetime):
        self.name = name
        self.semester = semester
        self.deadline = deadline