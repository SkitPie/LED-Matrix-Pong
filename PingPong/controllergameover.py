import threading
import time
from inputs import get_gamepad
from gameEngine import GameEngine, GameObject

def main():
    engine = GameEngine()
    ball = GameObject(15, 3, 1, 1, vx=0.5, vy=0.3)
  
    paddle_left = GameObject(2, 2, 1, 4)
    paddle_left.is_static = True

    paddle_right = GameObject(29, 2, 1, 4)
    paddle_right.is_static = True

    left_death = GameObject(0, 0, 1, 8)
    left_death.is_static = True

    right_death = GameObject(31, 0, 1, 8)
    right_death.is_static = True

    engine.add_object(ball)
    engine.add_object(paddle_left)
    engine.add_object(paddle_right)
    engine.add_object(left_death)
    engine.add_object(right_death)

    def gameover():
        print("Game Over")
        
    left_death.is_trigger = True
    left_death.trigger = gameover()

    

    def gamepad_input():
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
                        print("Gamepad BTN_THUMB gedrückt")
                        if paddle_right.y > 0:
                            paddle_right.y -= 1
                if event.ev_type == "Key" and event.code == "BTN_TOP":
                    if event.state == 1:
                        print("Gamepad BTN_TOP gedrückt")
                        if paddle_right.y < engine.height - paddle_right.height:
                            paddle_right.y += 1

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
