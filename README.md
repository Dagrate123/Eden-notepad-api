# Prosjekt README

## Oppsett av prosjektet

Følg disse stegene for å sette opp prosjektet lokalt:

1. **Clone prosjektet**
   ```bash
   git clone <repo-url>
   cd <prosjekt-mappe>
   ```

2. **Opprett et virtuelt miljø**
   ```bash
   python3 -m venv .venv
   ```

3. **Aktiver det virtuelle miljøet**
   ```bash
   source .venv/bin/activate
   ```

4. **Installer nødvendige pakker**
   ```bash
   pip install requests FreeSimpleGUI
   ```

---

## Hvordan kjøre prosjektet

Prosjektet består av to deler:

### 1. Start serveren
```bash
python server.py
```

Du skal se:
```
Server running on http://192.168.20.74:8000/notes
```

### 2. Start klienten (GUI)
Åpne et nytt terminalvindu og kjør:
```bash
python client.py
```

---

## Funksjonalitet

- Opprette nye notater
- Redigere og lagre notater
- Slette notater
- Navigere mellom notater via sidebar
- Data lagres i database via API
- oprette to-do lister

---

## Bruker-tips

* Velg et notat i sidebaren for å åpne det
* Trykk **Save** for å lagre endringer
* Trykk **New Note** for å lage et nytt notat
* Trykk **Delete** for å slette valgt notat

---

## Teknologier brukt

- **Python**
- **FreeSimpleGUI** (GUI)
- **SQLite** (database)
- **HTTPServer** (backend API)
- **Requests** (klient → server kommunikasjon)

---

## Arkitektur

Prosjektet bruker en enkel klient–server-modell:

```
GUI (client) → HTTP API → SQLite database
```

- Klienten sender HTTP-requests til serveren
- Serveren håndterer logikk og database
- Databasen lagrer brukere og notater

---

## Sikkerhet

- Passord lagres som hash (SHA-256)
- API er beskyttet med en enkel API-nøkkel

---

## Begrunnelse for valg

* **GUI-bibliotek:** Jeg har valgt å bruke **FreeSimpleGUI** fordi det er lettvekt og enkelt å jobbe med.
* **Sidebar vs. tabs:** En sidebar gir et mer oversiktlig og skalerbart grensesnitt.
* **Database:** SQLite er enkelt å sette opp og tilstrekkelig for dette prosjektet.
* **API:** Prosjektet bruker en egen HTTP-server for å skille frontend og backend, noe som gjør løsningen mer fleksibel og realistisk.

---

## Videre arbeid

Mulige forbedringer:

- Implementere innlogging i GUI
- Legge til flere brukere (multi-user system)
- Bedre feilhåndtering
---

## Kjente problemer

- Ingen ekte autentisering (kun API-key)
- Ikke optimalisert for flere samtidige brukere
- Enkel HTTP-server (ikke egnet for produksjon)

