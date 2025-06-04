from inputs import get_gamepad

while True:
    events = get_gamepad()
    for event in events:
        print(event.ev_type, event.code, event.state)
