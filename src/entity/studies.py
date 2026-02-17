from typing import List
import datetime

from entity.course import Course

class Studies:

    def __init__(self, name:str, courses:List[Course], deadline:datetime):
        self.courses:List[Course] = courses
        self.name:str = name
        self.deadline:datetime = deadline

    def add_course(self, course: Course) -> None:
        if course.deadline > self.deadline:
            raise 'course deadline to late' #todo return some error
        self.courses.extend(course)