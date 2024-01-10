# Standard
import multiprocessing as mp
from pynput.keyboard import Listener


class InputController:

    def __init__(self, queue: mp.Queue):

        self.queue: mp.Queue = queue

    def on_press(self, key):
        try:
            self.queue.put((True, key.char))
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            self.queue.put((False, key.char))
        except AttributeError:
            pass

    def run(self):

        with Listener(on_press=self.on_press, on_release=self.on_release, daemon=True) as listener:
            listener.join()


def run(queue: mp.Queue):

    controller = InputController(queue)
    controller.run()


# TEST
if __name__ == '__main__':
    q = mp.Queue()
    mp.Process(target=run, args=(q,), daemon=True).start()
    while True:
        print(q.get())
