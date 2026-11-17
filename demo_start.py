#!/usr/bin/env python3
"""AMB+ – Demo auf dem eigenen Rechner starten.

Startet den AMB+-Server und den Connector zusammen, öffnet die Vorführungsseite
im Browser und den Demo-Importordner im Dateimanager. Beenden mit Strg+C
oder durch Schließen des Fensters.

Aufruf: Doppelklick auf "Start-Demo.bat" (Windows) bzw. "start-demo.command" (Mac)
        oder: python demo_start.py
"""
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
import webbrowser

HIER = os.path.dirname(os.path.abspath(__file__))
DEMO = os.path.join(HIER, 'Demo-Daten')
IMPORT = os.path.join(HIER, 'Demo-THEORG-IMPORT')


def zeile(t=''):
    print(t, flush=True)


def reportlab_pruefen():
    try:
        import reportlab  # noqa: F401
        return True
    except ImportError:
        pass
    zeile('Einmalige Einrichtung: Baustein für die PDF-Erzeugung wird installiert (reportlab) …')
    r = subprocess.run([sys.executable, '-m', 'pip', 'install', '--user', '--disable-pip-version-check', '-q', 'reportlab'])
    if r.returncode != 0:
        zeile('Installation fehlgeschlagen. Bitte Internetverbindung prüfen und erneut starten.')
        zeile('Manuell: %s -m pip install --user reportlab' % sys.executable)
        return False
    import site
    import importlib
    try:
        sys.path.append(site.getusersitepackages())
        importlib.invalidate_caches()
        import reportlab  # noqa: F401,F811
    except ImportError:
        pass
    return True


def freier_port(start=8080):
    for port in range(start, start + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', port))
                return port
            except OSError:
                continue
    raise SystemExit('Kein freier Port zwischen %d und %d gefunden.' % (start, start + 19))


def warte_auf_server(port, sekunden=20):
    ende = time.time() + sekunden
    while time.time() < ende:
        try:
            with urllib.request.urlopen('http://127.0.0.1:%d/' % port, timeout=1):
                return True
        except Exception:
            time.sleep(0.3)
    return False


def ordner_oeffnen(pfad):
    try:
        if sys.platform.startswith('win'):
            os.startfile(pfad)  # noqa
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', pfad])
        else:
            subprocess.Popen(['xdg-open', pfad], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass


def main():
    zeile('=' * 60)
    zeile(' AMB+ – Online-Anmeldung (Demo)')
    zeile('=' * 60)
    if sys.version_info < (3, 8):
        zeile('Python 3.8 oder neuer wird benötigt (gefunden: %s).' % sys.version.split()[0])
        return 1
    if not reportlab_pruefen():
        return 1
    os.makedirs(DEMO, exist_ok=True)
    os.makedirs(IMPORT, exist_ok=True)

    port = freier_port()
    daten = os.path.join(DEMO, 'server')
    server = subprocess.Popen([sys.executable, os.path.join(HIER, 'server', 'amb_server.py'), '--port', str(port),
                               '--data', daten, '--demo', '--demo-import', IMPORT],
                              stdout=open(os.path.join(DEMO, 'server.log'), 'a', encoding='utf-8'), stderr=subprocess.STDOUT)
    if not warte_auf_server(port):
        zeile('Der Server ist nicht gestartet. Details: %s' % os.path.join(DEMO, 'server.log'))
        server.terminate()
        return 1

    with open(os.path.join(daten, 'praxen.json'), encoding='utf-8') as f:
        pid, praxis = next(iter(json.load(f).items()))
    ini = os.path.join(DEMO, 'connector.ini')
    with open(ini, 'w', encoding='utf-8') as f:
        f.write('[connector]\nserver = http://127.0.0.1:%d\npraxis_schluessel = %s\nimportordner = %s\n'
                'intervall_minuten = 0.25\naufraeumen_nach_tagen = 30\nerledigt_ordner = erledigt\nprotokoll = %s\n'
                % (port, praxis['schluessel'], IMPORT, os.path.join(DEMO, 'connector.log')))
    connector = subprocess.Popen([sys.executable, os.path.join(HIER, 'connector', 'amb_connector.py'), '--config', ini],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    from importlib import util
    spec = util.spec_from_file_location('amb_server', os.path.join(HIER, 'server', 'amb_server.py'))
    lan = '127.0.0.1'
    try:
        mod = util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        lan = mod.lan_ip()
    except Exception:
        pass

    zeile()
    zeile(' Läuft. Bitte dieses Fenster offen lassen.')
    zeile()
    zeile(' Vorführungsseite:   http://127.0.0.1:%d/demo' % port)
    zeile(' Am Handy (WLAN):    http://%s:%d/' % (lan, port))
    zeile(' Praxisportal:       http://127.0.0.1:%d/portal' % port)
    zeile('   Benutzer:         %s' % pid)
    zeile('   Passwort:         %s' % praxis['schluessel'])
    zeile(' Goniometer (Handy): http://%s:%d/goniometer/' % (lan, port))
    zeile(' Importordner:       %s' % IMPORT)
    zeile()
    zeile(' Beenden: Strg+C drücken oder Fenster schließen.')
    zeile('=' * 60)
    webbrowser.open('http://127.0.0.1:%d/demo' % port)
    ordner_oeffnen(IMPORT)
    try:
        while server.poll() is None:
            time.sleep(1)
        zeile('Der Server wurde beendet. Details: %s' % os.path.join(DEMO, 'server.log'))
    except KeyboardInterrupt:
        zeile('Wird beendet …')
    finally:
        for p in (connector, server):
            if p.poll() is None:
                p.terminate()
    return 0


if __name__ == '__main__':
    sys.exit(main())
