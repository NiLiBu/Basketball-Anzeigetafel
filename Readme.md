# Basketball-Anzeigetafel

created by Niklas Linsler (für TSV Buchen Basketball)

Zu Nutzung mit einem Laptop/Windows Tablet mit einem externen Display oder Beamer
Die Idee ist dieses Tool als Backup zu nutzen, wenn die Spielanzeige nicht funktioniert.

Eine digitale Basketball-Anzeigetafel mit getrenntem **Controller** und
**Display**. Der Controller verwaltet den Spielstand und alle Timer. Das
Display empfängt die Daten vom Controller und zeigt sie an.

## Funktionen

- Punkte für Heim- und Auswärtsteam
  - Punktänderungen um -1, +1, +2 und +3
  - Wertebereich von 0 bis 999
- Foulanzeige für beide Teams
  - Fouls von 0 bis 4
  - Rote-Karte-Anzeige
- Spieluhr
  - Starten, pausieren und stoppen
  - Anpassung in 0,1-Sekunden-Schritten
  - Automatischer Signalton bei Ablauf
- Timeout und Viertelpause
  - Timeout mit 1 Minute
  - Viertelpause mit 2 Minuten
  - Automatisches Ausblenden des Displays bei `00:00.0`
- Viertelverwaltung
  - `1`, `2`, Halbzeit (`HT`), `3`, `4` und Verlängerung (`E`)
  - Dialog zur Bestätigung des Viertelende
  - Automatische Vorbereitung der nächsten Spielphase
- Aktionsverlauf im Controller
- Manueller Buzzer mit `Buzzer_Sound.mp3`
- Optionales Dark Theme, das ausschließlich im Display aktiviert oder
  deaktiviert werden kann
- Controller und Display werden als separate Fenster angezeigt

## Tastenkürzel

| Aktion                         | Taste                         |
| ------------------------------ | ----------------------------- |
| Heimteam -1                    | `Q`                           |
| Heimteam +1 / +2 / +3          | `1` / `2` / `3`               |
| Auswärtsteam -1                | `O`                           |
| Auswärtsteam +1 / +2 / +3      | `0` / `9` / `8`               |
| Fouls Heimteam -1 / +1         | `X` / `Y`                     |
| Fouls Auswärtsteam -1 / +1     | `M` / `N`                     |
| Spielzeit +0,1 / -0,1 Sekunden | `Pfeil hoch` / `Pfeil runter` |
| Timer starten/stoppen          | `Leertaste`                   |
| Timer stoppen                  | `Esc`                         |

Die Tastenkürzel gelten, wenn das Controller-Fenster aktiv ist.

## Voraussetzungen

- Python 3.15
- PySide6

Optional für eine Windows-Executable (Ist in den Relases als exe verfügbar):

- PyInstaller

## Starten

```powershell
python main.py
```

Falls eine virtuelle Umgebung verwendet wird:

```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

## Windows-Executable erstellen

Das Projekt enthält eine PyInstaller-Konfiguration für eine einzelne
Executable-Datei. Die Audiodatei `Buzzer_Sound.mp3` wird automatisch mit
eingebunden.

```powershell
.\build.ps1
```

Die fertige Datei wird unter folgendem Pfad erzeugt:

```text
dist\Basketball-Anzeigetafel.exe
```

## Projektstruktur

- `main.py` – startet Controller und Display und verbindet ihre Signale
- `scoreboard_controller.py` – Spielstand, Timer, Eingaben und Verlauf
- `scoreboard_display.py` – reine Anzeige inklusive Dark Theme
- `custum_spin_box.py` – wiederverwendbares Auswahlfeld für Fouls und Viertel
- `time_dialog.py` – Dialog zum Einstellen der Spielzeit
- `update_quarter_dialog.py` – Bestätigung beim Viertelende
- `Buzzer_Sound.mp3` – Audiodatei für den Buzzer
- `scoreboard.spec` – PyInstaller-Konfiguration
- `build.ps1` – Build-Skript für Windows
