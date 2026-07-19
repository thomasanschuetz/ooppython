from datetime import date

class BaseTransformer:
    def formatiere_note(self, note: float | None) -> str:
        if not note:
            return ''
        return f"{note:.2f}".replace('.', ',')
    
    def formatiere_datum(self, datum: date | None) -> str:
        if not datum:
            return ''
        return datum.isoformat()
