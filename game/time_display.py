# Standard
import tkinter as tk
import multiprocessing as mp
from queue import Empty


class TimeDisplay(mp.Process):

    def __init__(self, queue: mp.Queue):

        super(TimeDisplay, self).__init__(name="Time Display")

        self.root: tk.Tk = tk.Tk()
        self.queue: mp.Queue = queue

        self.root.overrideredirect(True)
        self.root.configure(background="black")
        self.root.geometry("200x160+28+70")
        self.root.wm_attributes("-topmost", 1)

        self.title1 = tk.Label(self.root, text="Zeit", background="black", foreground="white",
                               font=("Arial", 28))
        self.title1.pack(pady=(6, 0))
        self.title2 = tk.Label(self.root, text="übrig", background="black", foreground="white",
                               font=("Arial", 28))
        self.title2.pack(pady=(0, 0))
        self.time = tk.Label(self.root, text="Hi", background="black", foreground="white",
                             font=("Arial", 28))
        self.time.pack(pady=(3, 0))

    def run(self):

        self.root.after(10, self.update)

        self.root.mainloop()

    def update(self):

        try:
            cmd = self.queue.get(True, timeout=3)
        except Empty:
            self.root.destroy()
            self.close()
            return

        if cmd == "QUIT":
            self.root.destroy()
            self.close()
            return

        time_left = f"{cmd // 3600:02d}:{cmd // 60:02d}:{cmd % 60:02d}"
        self.time["text"] = time_left

        self.root.after(200, self.update)
