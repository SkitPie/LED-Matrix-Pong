import threading
import time
from inputs import devices
from gameEngine import GameEngine, GameObject

def main():
    engine = GameEngine()
    ball = GameObject(15, 3, 1, 1, vx=0.5, vy=0.3)
  
    paddle_left = GameObject(2, 2, 1, 4)
    paddle_left.is_static = True

    paddle_right = GameObject(29, 2, 1, 4)
    paddle_right.is_static = True

    def gameover(obj):
        print("Game Over")
        if obj:
            ball.setPos(15, 3)
        time.sleep(5)

    left_death = GameObject(0, 0, 1, 8, trigger=gameover)
    left_death.is_static = True

    right_death = GameObject(31, 0, 1, 8, trigger=gameover)
    right_death.is_static = True

    engine.add_object(ball)
    engine.add_object(paddle_left)
    engine.add_object(paddle_right)
    engine.add_object(left_death)
    engine.add_object(right_death)
        
    left_death.is_trigger = True
    right_death.is_trigger = True

    if len(devices.gamepads) < 2:
        print("Bitte zwei Gamepads anschließen.")
        return

    gamepad1 = devices.gamepads[0]  # Steuerung für paddle_left
    gamepad2 = devices.gamepads[1]  # Steuerung für paddle_right

    def gamepad_input_left():
        print("Gamepad 1 Thread gestartet")
        while engine.running:
            events = gamepad1.read()
            for event in events:
                if event.ev_type == "Key" and (event.code == "BTN_THUMB" or event.code == "BTN_PINKIE"):
                    if event.state == 1 and paddle_left.y > 0:
                        paddle_left.y -= 1
                if event.ev_type == "Key" and (event.code == "BTN_THUMB2" or event.code == "BTN_TOP2"):
                    if event.state == 1 and paddle_left.y < engine.height - paddle_left.height:
                        paddle_left.y += 1

    def gamepad_input_right():
        print("Gamepad 2 Thread gestartet")
        while engine.running:
            events = gamepad2.read()
            for event in events:
                if event.ev_type == "Key" and (event.code == "BTN_THUMB" or event.code == "BTN_PINKIE"):
                    if event.state == 1 and paddle_right.y > 0:
                        paddle_right.y -= 1
                if event.ev_type == "Key" and (event.code == "BTN_THUMB2" or event.code == "BTN_TOP2"):
                    if event.state == 1 and paddle_right.y < engine.height - paddle_right.height:
                        paddle_right.y += 1

    thread_left = threading.Thread(target=gamepad_input_left, daemon=True)
    thread_right = threading.Thread(target=gamepad_input_right, daemon=True)

    try:
        engine.start()
        thread_left.start()
        thread_right.start()

        print("Pong-Spiel läuft! Drücke Ctrl+C zum Beenden")

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        engine.stop()
        print("\nSpiel gestoppt")

main()
