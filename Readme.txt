# Web Fuzzing Tool

Dieses Python-basierte Tool führt Web-Fuzzing-Tests durch, um Sicherheitslücken in Webanwendungen zu erkennen. Es testet verschiedene Payloads auf Basis der angegebenen Programmiersprache und Version oder verwendet benutzerdefinierte Payloads. Das Tool kann auch nach Exploits in Exploit-DB und Metasploit suchen, wenn ein funktionierender Payload gefunden wird.

## Features

- Unterstützung für mehrere Programmiersprachen (PHP, JavaScript, Python, MySQL, PostgreSQL, WordPress).
- Möglichkeit, benutzerdefinierte Payloads und Angriffsarten hinzuzufügen.
- Automatische Suche nach Exploits in Exploit-DB und Metasploit (via `searchsploit`).
- Loggt alle Ergebnisse in einer Textdatei (`fuzzing_log.txt`).
- Banner- und Terminalschnittstelle mit ASCII-Schriftzug.

## Installation

### Voraussetzungen

Stellen Sie sicher, dass Sie Python 3.13 auf Ihrem System installiert haben. Falls nicht, laden Sie es von [python.org](https://www.python.org/downloads/) herunter.

### Abhängigkeiten installieren

Um das Tool auszuführen, benötigen Sie einige Python-Bibliotheken. Installieren Sie diese, indem Sie die folgenden Schritte ausführen:

1. Klonen Sie das Repository oder laden Sie die Dateien herunter.

   ```bash
   git clone https://github.com/USERNAME/REPOSITORY_NAME.git
   cd REPOSITORY_NAME

2.Erstellen Sie eine virtuelle Umgebung (optional, aber empfohlen):

python3 -m venv venv
source venv/bin/activate  # Auf Linux/macOS
venv\Scripts\activate  # Auf Windows


4. Installieren Sie alle erforderlichen Bibliotheken:

pip install -r requirements.txt
sudo apt install exploitdb

5. Starten

python3 fuzzing_tool.py

