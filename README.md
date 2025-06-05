Projektübersicht: LED-Matrix-Pong

Dieses Repository enthält ein einfaches Pong-Spiel, das auf einer aus vier MAX7219 LED-Matrizen bestehenden 32x8 Anzeige läuft. Die Steuerung erfolgt über USB‑Gamepads.
Verzeichnisstruktur

    PingPong/ – enthält den gesamten Python-Code.
        controller.py – Startskript für einen Spieler mit einem Gamepad.
        controllergameover.py – Variante für zwei Spieler mit einfacher Game‑Over-Logik.
        gameEngine.py – Kleine Spiel-Engine zur Verwaltung der Spiellogik und zum Rendern auf der Matrix.
        led_display.py – Funktionen für die SPI-Ansteuerung der LED-Matrizen.
        test.py – Hilfsskript zum Anzeigen von Gamepad-Eingaben.

Voraussetzungen

    Python 3
    Bibliotheken: inputs, spidev
    Vier miteinander verbundene MAX7219 LED-Matrizen (insgesamt 32x8 Pixel)

Spielprinzip

Das Spiel verwendet die GameEngine aus gameEngine.py, um Objekte wie Ball und Schläger zu verwalten. Die Engine kümmert sich um Kollisionen mit den Wänden und zwischen den Objekten. Über die Funktionen in led_display.py werden die aktuellen Positionen auf die LED‑Matrix geschrieben.
Steuerung

    In controller.py steuert ein einzelnes Gamepad beide Schläger. Dies ist vor allem zum Testen gedacht.
    controllergameover.py erwartet zwei Gamepads und setzt das Spiel zurück, sobald der Ball eine der beiden Seiten berührt.

Verwendung

    Benötigte Bibliotheken installieren (z. B. via pip install inputs spidev).
    LED-Matrizen gemäß den Vorgaben des MAX7219 verbinden.
    Eines der Controller-Skripte aus dem Verzeichnis PingPong starten.

python PingPong/controller.py

oder

python PingPong/controllergameover.py

Mit test.py lässt sich überprüfen, ob die angeschlossenen Gamepads korrekt erkannt werden.
Hinweise

Die Skripte sind bewusst kompakt gehalten und sollen vor allem zeigen, wie man die LED‑Matrix über SPI ansteuert und einfache Spiellogik implementiert. Weitere Verbesserungen wie ein Punktesystem oder ein umfangreicheres Menü können leicht ergänzt werden.
