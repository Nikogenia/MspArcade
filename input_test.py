import inputs


while True:

    events: list[inputs.InputEvent] = inputs.get_gamepad()

    for event in events:
        print(event.code, event.state, event.device, event.ev_type, event.timestamp)
