from typing import List, Dict
from datetime import date
from dateutil.relativedelta import relativedelta
import math
import pickle



    




kurse = [Kurs(str(k+1), f"kurs {k+1}", k//6 + 1, 3, 5) for k in range(32)]
kurse[28].ects = 10
kurse[29].semester = 6
kurse[29].ects = 10
kurse[30].ects = 10
kurse[31].ects = 10
studium = Studium("KI", date.today(), 42, 2.0, kurse)

print(studium)
print(f"Durchschnittsnote:{studium.durchschnittsnote()}")


print(f"Zielnote: {studium.ziel_note}, Durchschnittsnote:{studium.durchschnittsnote()}, benötigt:{studium.benoetigte_durchschnittsnote()}")
studium.set_kurs_data('1', 3, 2.0, None)
studium.set_kurs_data('7', 3, 3.0, None)
print(f"Zielnote: {studium.ziel_note}, Durchschnittsnote:{studium.durchschnittsnote()}, benötigt:{studium.benoetigte_durchschnittsnote()}")

datum = date(2026, 7, 4)

print(f"fällige Prüfungen zum {datum}:\n{"\n".join(map(str, studium.faellige_pruefungen(datum, 3)))}")
print(f"nächste reguläre Prüfungen zum {datum}:\n{"\n".join(map(str, studium.naechste_regulaere_pruefungen(datum, 3)))}")


# über semester iterieren
 # über kurse iterieren
  # fertig, todo, überfällig

# für semester
 # start, end von kurs

# über alles
 # durchschnitt
 # im verzug
 # nächste prüfungen


