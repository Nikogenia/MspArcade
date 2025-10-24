# Standard
import tkinter as tk
import multiprocessing as mp
from queue import Empty
import time


class InfoDisplay:

    def __init__(self, queue: mp.Queue):

        self.root: tk.Tk = tk.Tk()
        self.queue: mp.Queue = queue

        self.root.overrideredirect(True)
        self.root.configure(background="black")
        self.root.geometry("200x265+1692+70")  # TODO adjust position
        self.root.wm_attributes("-topmost", 1)

        self.canvas = tk.Canvas(self.root, width=198, height=263, background="black")
        self.canvas.place(x=0, y=0)

        self.title = tk.Label(self.root, text="Zeit", background="black", foreground="white",
                              font=("Arial", 38))
        self.title.pack(pady=(8, 0))
        self.time = tk.Label(self.root, text="00:00:00", background="black", foreground="white",
                             font=("Arial", 30))
        self.time.pack(pady=(2, 0))

        self.hint1 = tk.Label(self.root, text="Spiel beenden", background="black", foreground="white",
                              font=("Arial", 20))
        self.hint1.pack(pady=(20, 4))
        self.hint2 = tk.Label(self.root, text="RESET", background="white", foreground="black",
                              font=("Arial", 28))
        self.hint2.pack(ipadx=6, pady=(1, 1))

    def run(self):

        self.root.after(10, self.update)

        self.root.mainloop()

    def update(self):

        try:
            cmd = self.queue.get(True, timeout=5)
        except Empty:
            self.root.destroy()
            return

        if cmd == "QUIT":
            self.root.destroy()
            return

        time_left = f"{cmd // 3600:02d}:{cmd % 3600 // 60:02d}:{cmd % 60:02d}"
        self.time["text"] = time_left

        self.root.after(200, self.update)


def run(queue: mp.Queue):

    display = InfoDisplay(queue)
    display.run()


# TEST
if __name__ == '__main__':
    q = mp.Queue()
    mp.Process(target=run, args=(q,), daemon=True).start()
    for i in range(20):
        q.put(20 - i)
        time.sleep(1)
    q.put("QUIT")
