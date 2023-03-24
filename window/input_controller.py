# Standard
import multiprocessing as mp
import inputs
import time


class InputController:

    def __init__(self, queue: mp.Queue):

        self.queue: mp.Queue = queue

    def run(self):

        while True:

            try:
                events: list[inputs.InputEvent] = inputs.get_gamepad()
            except (inputs.UnpluggedError, OSError):
                inputs.devices = inputs.DeviceManager()
                time.sleep(1)
                continue

            for event in events:
                device: inputs.GamePad = event.device
                self.queue.put((event.code, event.state, device.get_number()))


def run(queue: mp.Queue):

    controller = InputController(queue)
    controller.run()


# TODO Debug
if __name__ == '__main__':
    q = mp.Queue()
    mp.Process(target=run, args=(q,), daemon=True).start()
    while True:
        print(q.get())
