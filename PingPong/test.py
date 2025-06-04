"""Small helper script printing raw gamepad events."""

from inputs import devices
import threading

def handle_gamepad(gamepad, id):
    """Continuously read events from a gamepad and print them."""
    while True:
        events = gamepad.read()
        for event in events:
            print(f"Gamepad {id}:", event.ev_type, event.code, event.state)

def main():
    """Start threads for two connected gamepads."""

    gamepad1 = devices.gamepads[0]
    gamepad2 = devices.gamepads[1]

    thread1 = threading.Thread(target=handle_gamepad, args=(gamepad1, 1))
    thread2 = threading.Thread(target=handle_gamepad, args=(gamepad2, 2))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

if __name__ == "__main__":
    main()
