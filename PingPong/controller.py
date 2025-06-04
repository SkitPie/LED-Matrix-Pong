"""Simple controller that runs the Pong game using one gamepad.

This script spawns a :class:`~gameEngine.GameEngine` instance and
maps basic gamepad events to paddle movements.  It is intended for a
single player controlling both paddles for testing purposes.
"""

import threading
import time
from inputs import get_gamepad
from gameEngine import GameEngine, GameObject

def main():
    """Start the game and handle input in a background thread."""

    engine = GameEngine()
    ball = GameObject(15, 3, 1, 1, vx=0.5, vy=0.3)
  
    paddle_left = GameObject(1, 2, 1, 4)
    paddle_left.is_static = True

    paddle_right = GameObject(30, 2, 1, 4)
    paddle_right.is_static = True

    engine.add_object(ball)
    engine.add_object(paddle_left)
    engine.add_object(paddle_right)

    def gamepad_input():
        """Poll the gamepad and adjust paddle positions."""

        print("Gamepad-Thread gestartet")
        while engine.running:
            events = get_gamepad()
            for event in events:
                if event.ev_type == "Key" and event.code == "BTN_THUMB":
                    if event.state == 1:
                        print("Gamepad BTN_THUMB gedrückt")
                        if paddle_left.y > 0:
                            paddle_left.y -= 1
                if event.ev_type == "Key" and event.code == "BTN_THUMB2":
                    if event.state == 1:
                        print("Gamepad BTN_TOP gedrückt")
                        if paddle_left.y < engine.height - paddle_left.height:
                            paddle_left.y += 1

                if event.ev_type == "Key" and event.code == "BTN_TRIGGER":
                    if event.state == 1:
                        print("Gamepad BTN_TRIGGER gedrückt")
                        if paddle_right.y > 0:
                            paddle_right.y -= 1
                if event.ev_type == "Key" and event.code == "BTN_TOP":
                    if event.state == 1:
                        print("Gamepad BTN_TOP gedrückt")
                        if paddle_right.y < engine.height - paddle_right.height:
                            paddle_right.y += 1

    # Start polling the gamepad in a separate thread
    gamepad_thread = threading.Thread(target=gamepad_input, daemon=True)





    try:
        engine.start()
        gamepad_thread.start()

        print("Pong-Spiel läuft! Drücke Ctrl+C zum Beenden")

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        engine.stop()
        print("\nSpiel gestoppt")

main()
