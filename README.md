EiP Praktikum WS 2022/2023
==========================

Ziel
----

Implementieren Sie in Python ein rundenbasiertes Gesellschaftsspiel für 2 oder
mehr Mitspieler mit Hilfe des vorgegebenen Frameworks.
Das vorgegebene Framework erlaubt sowohl die lokale Ausführung als auch die Ausführung
über das Internet.
Ein Beispielprogramm `TicTacToe.py` ist vorgegeben, an dem Sie sich orientieren können.
Es enthält ausgiebige Kommentare zu den Methoden, die Sie implementieren müssen.
Die letzte auszuführende Codezeile in Ihrem Programm muss immer mit

    GamePlayer.run(...

beginnen!
Der Aufruf startet die Ausführung über das Framework und kehrt erst zurück,
wenn das Spiel beendet wurde.


Ausführung
----------

Sie können `TicTacToe.py` oder ein von Ihnen programmiertes Spiel direkt ausführen.
Alternativ können Sie auch `GamePlayer.py` ausführen.
Dieses Programm erkennt alle Spieldateien im Verzeichnis und erlaubt sowohl das
lokale Spielen als auch das Spielen über das Internet über einen entsprechenden Dialog.

Die einfachste Methode, in Visual Studio Code ein Python Skript auszuführen, ist,
die entsprechende Datei zu öffnen, `F5` zu drücken und in der oben erscheinenden Auswahlbox
anzuklicken, dass die aktuelle Datei ausgeführt werden soll.


Aufgaben
--------

### Aufgabe 0 - Versionskontrolle Git
Richten Sie wie auf der [Wiki-Seite](https://gitlab.rlp.net/groups/eip_praktikum_23/-/wikis/home)
beschrieben Ihre Arbeitsumgebung ein.

### Aufgabe 1 - Vier Gewinnt
Implementieren Sie das Spiel `Vier gewinnt` für 2 Spieler und führen Sie es zunächst
nur lokal aus.
Wenn dies funktioniert, testen Sie, ob es auch über das Internet funktioniert.
Erstellen Sie dazu eine Datei `VierGewinnt.py` in Ihrem Repository.
Eine ausführliche Spielbeschreibung finden Sie in der [Wikipedia]().
Zur Umsetzung können Sie z.B. folgendermaßen vorgehen:

1. Überlegen Sie sich, wie den Spielzustand über eine globale Variable darstellen wollen
und initialisieren Sie diese im globalen Scope oder über die `initGame` Funktion.
2. Implementieren Sie die `paintGame` Funktion.
Das Programm sollte sich anschließend starten lassen und das Spielfeld darstellen.
3. Implementieren Sie die Zuglogik in der `makeMove` Funktion und geben Sie immer den Index
desjenigen Spielers zurück, der gerade nicht am Zug war.
4. Implementieren Sie die Überprüfung, ob ein Spieler gewonnen hat, sodass die
`makeMove` Funktion korrekt -1 zurückgeben kann, falls ein Spieler gewonnen hat.


#### Aufgabe 2 - Implementierung eines Spiels nach Wahl
Implementieren Sie ein Spiel Ihrer Wahl.
Besprechen Sie Ihre Spielidee mit einer Betreuer*in, bevor Sie mit der Implementierung
beginnen.
In verschiedenen entsprechend benannten Ordner in Ihrem Repository finden Sie bereits
Karten und Spielsteine für diverse Spiele, die Sie verwenden können.
Außerdem gibt im UTF-8 Zeichensatz sehr viele Symbole, die Sie direkt in Ihren Code
einfügen und genauso wie ganz normalen Text darstellen können.
Am zweiten Praktikumstag wird erläutert, wie Sie Bilddateien in Ihrem Programm laden können,
sodass die Ausführung über das Netzwerk funktioniert, auch wenn die Dateien nicht auf den
anderen PCs an gleicher Stelle zur Verfügung stehen.

Überlegen Sie, wie sie schrittweise vorgehen können.
Spätestens nach zwei Stunden programmieren, sollte es möglich sein, geschriebenen Code
auszuführen und anhand dessen die Funktion zu überprüfen.
Vermeiden Sie stundenlanges Programmieren, ohne über ausführbaren Code zu verfügen,
weil dies das Risiko birgt, dass sich so viele Fehler ansammeln oder man einen
Denkfehler begeht, sodass sich der Code nicht mehr korrigieren lässt.

Erstellen Sie außerdem regelmäßig neue Commits als Sicherung funktionierender Spielzustände
und laden Sie diese durch einen Git Push auf den Server hoch.
