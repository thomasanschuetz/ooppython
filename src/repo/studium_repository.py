from src.entity.studium import Studium
import pickle
from pathlib import Path
from datetime import date

class StudiumRepository:
    def __init__(self, file_name: str):
        self.path : Path = Path(file_name)

    def speichere_studium(self, studium: Studium) -> None:
        with open(self.path, "wb") as f:
            pickle.dump(studium, f)

    def lade_studium(self) -> Studium|None:
        #todo handle non readable path
        if not self.path.exists():
            return None
        with open(self.path, "rb") as f:
            return pickle.load(f)
