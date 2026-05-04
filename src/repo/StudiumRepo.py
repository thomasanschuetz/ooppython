from src.entity.Studium import Studium
import pickle
from pathlib import Path
from datetime import date

class StudiumRepo:
    def __init__(self, file_name: str):
        self.path : Path = Path(file_name)

    def save(self, studium: Studium) -> None:
        with open(self.path, "wb") as f:
            pickle.dump(studium, f)

    def load(self) -> Studium:
        #todo handle non readable path
        if not self.path.exists():
            return Studium(date.today(), 'Mein Studium', 1.0, 36, [])
        with open(self.path, "rb") as f:
            return pickle.load(f)
