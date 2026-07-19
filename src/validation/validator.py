from src.entity.enums import KursSchwere

class Validator:
    @staticmethod
    def validiere_studium(name, beginn, ziel_note, ziel_monate):
        errors = []
        if not name or len(name.strip()) == 0:
            errors.append("Name ist erforderlich.")
        if not beginn:
            errors.append("Beginn ist erforderlich.")
        if ziel_note is None or ziel_note < 1 or ziel_note > 6:
            errors.append("Ziel-Note muss zwischen 1 und 6 liegen.")
        if ziel_monate is None or ziel_monate < 1 or ziel_monate > 120:
            errors.append("Ziel-Monate muss zwischen 1 und 120 liegen.")
        return errors

    @staticmethod
    def validiere_kurs(name, ects, schwere):
        errors = []
        if not name or len(name.strip()) == 0:
            errors.append("Name ist erforderlich.")
        if ects is None or ects < 1 or ects > 20:
            errors.append("ECTS muss zwischen 1 und 20 liegen.")
        if schwere is None or schwere not in {item.value for item in KursSchwere}:
            errors.append(f"Schwere muss zwischen {min(item.value for item in KursSchwere)} und {max(item.value for item in KursSchwere)} liegen.")
        return errors

    @staticmethod
    def validiere_noten(noten) -> list:
        errors = []
        for note in noten:
            if note is not None and (note < 1 or note > 6):
                errors.append(f"Note muss zwischen 1 und 6 liegen.")
                break
        return errors
    
    def validiere_note(note) -> list:
        errors = []
        if note < 1 or note > 6:
            errors.append(f"Note muss zwischen 1 und 6 liegen.")
        return errors
