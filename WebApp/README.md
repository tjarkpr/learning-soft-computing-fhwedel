# Web-Applikation zum KRR-Modell zur Sarkasmuserkennung
**Wichtige Informationen und Vorraussetzungen:**
- NodeJS und explizit NPM müssen vorinstalliert sein
- Im Root Verzeichnis der Web-Applikation den Befehl `npm i` ausführen
- In dem Pfad `./child_process/` wechseln und `python -m venv ./venv` ausführen
- Anschließend den Befehl `source ./venv/bin/activate` ausführen (Nun sind wir im virtuellen Python Environment)

**Bitte folgende Befehle im `(venv)` ausführen:**
- `pip install joblib`
- `pip install numpy`
- `pip install pandas`
- `pip install nltk`
- `pip install sklearn`
Das `(venv)` kann über den Befehl `deactivate` verlassen werden.

**Nun kann die Web-Applikation gestartet werden:**
- In das Root Verzeichnis des Projekts zurückkehren
- `npm start` ausführen
- `localhost:3000` öffnen
