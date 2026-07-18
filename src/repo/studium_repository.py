from src.entity.studium import Studium
from src.entity.kurs import Kurs
from src.entity.enums import KursSchwere, KursStatus
import json
from pathlib import Path
from datetime import date
from typing import Dict, Any

class StudiumRepository:
    def __init__(self, file_name: str):
        self.path: Path = Path(file_name)

    def speichere_studium(self, studium: Studium) -> None:
        data = self._studium_to_dict(studium)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def lade_studium(self) -> Studium | None:
        if not self.path.exists():
            return None
        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return self._dict_to_studium(data)

    def _studium_to_dict(self, studium: Studium) -> Dict[str, Any]:
        return {
            "name": studium.name,
            "beginn": studium.beginn.isoformat(),
            "ziel_note": studium.ziel_note,
            "ziel_monate": studium.ziel_monate,
            "kurse": [self._kurs_to_dict(kurs) for kurs in studium.kurse]
        }

    def _kurs_to_dict(self, kurs: Kurs) -> Dict[str, Any]:
        return {
            "id": kurs.id,
            "name": kurs.name,
            "ects": kurs.ects,
            "schwere": kurs.schwere,
            "noten": kurs.noten,
            "beginn": kurs.beginn.isoformat() if kurs.beginn else None,
            "ende": kurs.ende.isoformat() if kurs.ende else None
        }

    def _dict_to_studium(self, data: Dict[str, Any]) -> Studium:
        studium = Studium(
            name=data["name"],
            beginn=date.fromisoformat(data["beginn"]),
            ziel_note=data["ziel_note"],
            ziel_monate=data["ziel_monate"]
        )
        studium._kurse = [self._dict_to_kurs(kurs_data) for kurs_data in data["kurse"]]
        return studium

    def _dict_to_kurs(self, data: Dict[str, Any]) -> Kurs:
        return Kurs(
            id=data["id"],
            name=data["name"],
            ects=data["ects"],
            schwere=KursSchwere(data["schwere"]),
            noten=data["noten"],
            beginn=date.fromisoformat(data["beginn"]) if data["beginn"] else None,
            ende=date.fromisoformat(data["ende"]) if data["ende"] else None
        )
