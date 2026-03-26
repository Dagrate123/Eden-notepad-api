# Eden-notepad-api

sett opp prosjektet:

først må du clone prosjektet

så må du sette opp at venv(virtual enviorment) ved å skrive python3 -m venv .venv

deretter må du starte venv-en ved å skrive source .venv/bin/activate

deretter laster du ned requests og freesimpleGui med pip install requests, freesimpleGui

bruker-tips:

høyreklikk for å legge til enten en to-do liste, gi nytt navn eller slette et notat

begrunnelse:

jeg har valgt å bruke freesimplegui fordi det er en lett, men kan fortsatt utvides en del. jeg valgte å ha en sidebar siden det ser mye bedrre ut en tabs. tabs blir veldig fort veldig rotete. til "2.utkast" skal jeg legge til at notat_navnet blir automatisk en tittel. da blir det mye finere. 

det er null api elementer. når jeg skulle hoste serveren så fikk jeg plutselig ikke lov til å ssh meg in(broken pipe). så det skal jeg også legge til neste gang.

notatene blir lagret i en databse, og egentlig ville jeg ha brukt mariaDB for scaleability, men sqlite er mye enklere og i denne problemstillingen, så funker den. 
