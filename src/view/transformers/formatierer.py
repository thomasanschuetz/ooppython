from datetime import date

class Formatierer:
    """
    Grundlegende Methoden zur Formatierung von Daten.
    """
    def formatiere_note(self, note: float | None) -> str:
        """
        Formatiert eine Note als String.
        
        Args:
            note (float | None): Die zu formatierende Note.
            
        Returns:
            str: Die formatierte Note oder ein leerer String, falls die Note None ist.
        """
        if not note:
            return ''
        return f"{note:.2f}".replace('.', ',')
    
    
    def formatiere_datum(self, datum: date | None) -> str:
        """
        Formatiert ein Datum als String.
        
        Args:
            datum (date | None): Das zu formatierende Datum.
            
        Returns:
            str: Das formatierte Datum oder ein leerer String, falls das Datum None ist.
        """
        if not datum:
            return ''
        return datum.isoformat()
