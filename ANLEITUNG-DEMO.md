# AMB+ – Demo auf dem eigenen Rechner

Alles läuft nur auf Ihrem Rechner. Es werden keine echten E-Mails verschickt und keine Daten nach außen übertragen.

## 1. Einmal vorbereiten (ca. 5 Minuten)
1. **Python installieren**, falls nicht vorhanden: https://www.python.org/downloads/ – beim Installieren unter Windows das Häkchen **„Add python.exe to PATH“** setzen.
2. Den Ordner `AMB-Demo` entpacken, z. B. auf den Desktop.
3. **Windows:** Doppelklick auf `Start-Demo.bat` · **Mac:** Doppelklick auf `start-demo.command` (beim ersten Mal ggf. Rechtsklick → Öffnen).
   Beim ersten Start wird ein Baustein für die PDF-Erzeugung nachinstalliert (Internet nötig). Danach öffnen sich automatisch die **Vorführungsseite** im Browser und der **Demo-Importordner**.

Das schwarze Fenster muss während der Demo offen bleiben. Schließen beendet alles.

## 2. Vorführung (ca. 5 Minuten)
Die Vorführungsseite (`http://127.0.0.1:8080/demo`) führt durch die vier Schritte und zeigt alles, was sonst im Hintergrund passiert.

1. **Patient fordert den Bogen an.** Auf „Anmeldebogen anfordern“ klicken, eine beliebige E-Mail-Adresse eintippen. In der Demo erscheint der Link direkt auf der Seite (im echten Betrieb kommt er per E-Mail).
   Am **Handy** vorführen: Handy ins selbe WLAN, die auf der Vorführungsseite angezeigte Adresse (z. B. `http://192.168.1.23:8080/`) eintippen.
2. **Patient füllt aus.** Link öffnen und den Bogen durchgehen. Für ein schnelles Durchklicken ohne Pflichtfelder `?test=1` an den Link hängen; dort gibt es auch „Springe zu“ und die Verordnung zum Scannen (simuliert). Am Ende „Anmeldung an die Praxis senden“.
3. **Praxis erhält die Anmeldung.** Innerhalb von 15 Sekunden erscheint das PDF im Ordner `Demo-THEORG-IMPORT` (steht für `C:\THEORG\IMPORT`). PDF öffnen: Ampel, Red Flags, Körperschema. In THEORG wäre das: Patient öffnen → E-Akte → Blitzimport.
4. **Praxisportal** öffnen (Benutzer und Passwort stehen auf der Vorführungsseite und im schwarzen Fenster): Liste der Anmeldungen, PDF, Link an Patienten senden.
5. **Goniometer (Therapeut misst).** Auf der Vorführungsseite „Goniometer öffnen“ (am Handy: die angezeigte Adresse mit `/goniometer/`). Patient mit Geburtsdatum eingeben, Gelenke messen, „In E-Akte speichern“. Das Messprotokoll kommt wie eine Anmeldung als PDF in den Importordner (`Nachname_Vorname_TT.MM.JJJJ_Goniometer_JJJJ-MM-TT.pdf`) → Blitzimport.
   Die Bewegungssensoren des Handys funktionieren nur über HTTPS. In der Demo (HTTP im WLAN) die Werte daher von Hand eintippen.

Die Vorführungsseite zeigt unten die „E-Mails“, die im echten Betrieb verschickt würden. Seite neu laden, um den aktuellen Stand zu sehen.

## 3. Zurücksetzen
Fenster schließen, die Ordner `Demo-Daten` und `Demo-THEORG-IMPORT` löschen, neu starten.

## 4. Was die Demo zeigt und was noch fehlt
**Zeigt:** kompletter Ablauf vom Link bis zum PDF im Importordner, Anmeldebogen mit Verordnungs-Scan (simuliert), freiwillige Anamnese nach ICF, Schmerz-Körperschema, Red/Yellow/Green/Blue-Flags, Praxis-PDF, Praxisportal, Connector.
**Fehlt für den echten Betrieb:** Server in Deutschland mit HTTPS, echter E-Mail-Versand, verschlüsselte Ablage, Einwilligungstexte, echte Texterkennung der Verordnung, Test mit dem THEORG-Blitzimport in der Praxis, Anbindung an die TI (Pflicht ab 10/2027).

## Bei Problemen
- „Python ist nicht installiert“ → Schritt 1.
- Seite öffnet sich nicht → im schwarzen Fenster steht die Adresse; von Hand in den Browser kopieren.
- Handy erreicht die Seite nicht → beide Geräte im selben WLAN? Firewall auf dem Rechner fragt beim ersten Start evtl. nach Freigabe für Python → zulassen.
- Fehlerdetails: `Demo-Daten/server.log` und `Demo-Daten/connector.log`.
