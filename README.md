````markdown
# Prosjekt README

## Oppsett av prosjektet

Følg disse stegene for å sette opp prosjektet lokalt:

1. **Clone prosjektet**
   ```bash
   git clone <repo-url>
   cd <prosjekt-mappe>
````

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
   pip install requests freesimpleGui
   ```

---

## Bruker-tips

* **Høyreklikk på et notat** for å:

  * Legge til en to-do-liste
  * Gi nytt navn til notatet
  * Slette notatet

* Notater lagres lokalt i en database. For enkelhet brukes SQLite, men for større skalerbarhet kunne MariaDB vært et alternativ.

---

## Begrunnelse for valg

* **GUI-bibliotek:** Jeg har valgt å bruke **freesimpleGui** fordi det er lettvekt, men fortsatt fleksibelt og kan utvides ved behov.
* **Sidebar vs. tabs:** En sidebar gir et ryddigere grensesnitt enn tabs, som fort blir rotete.
* **Automatiske titler:** I neste versjon (2. utkast) vil notat-navnet automatisk brukes som tittel, noe som gjør notatene mer oversiktlige.
* **Database:** Selv om MariaDB er mer skalerbart, er SQLite tilstrekkelig for denne problemstillingen og mye enklere å sette opp.
* **API:** Prosjektet har ingen API-elementer. Under testing fikk jeg problemer med SSH (broken pipe), så det blir lagt til i neste versjon.
