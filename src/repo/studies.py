from entity.studies import Studies as StudiesEntity
import pickle
from pathlib import Path
from typing import List

class Studies:
    def __init__(self, file_name: str):
        self.path:Path = Path(file_name)

    def save(self, studies: List[StudiesEntity]) -> None:
        with open(self.file_name, "wb") as f:
            pickle.dump(studies)

    def load(self) -> List[StudiesEntity]:
        if not self.path.exists() or not self.path.is_r:
            return []
        with open(self.file_name, "rb") as f:
            studies = pickle.load(f)
        return studies