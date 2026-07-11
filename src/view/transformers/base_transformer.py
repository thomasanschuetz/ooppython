from datetime import date

class BaseTransformer:
    """Base class for all transformers with common utility methods"""
    
    def formatiere_note(self, note: float | None) -> str:
        """Format a grade/note for display"""
        if not note:
            return ''
        return f"{note:.2f}".replace('.', ',')
    
    def format_date(self, datum: date | None) -> str:
        """Format a date for display"""
        if not datum:
            return ''
        return datum.isoformat()
