import tkinter as tk
import time
from Split import Split


def transform_time(t):
    mil = int((t - int(t)) * 100)
    sec = int(t % 60)
    minutes = int((t // 60) % 60)
    hours = int(t // 3600)

    return f"{hours:02}:{minutes:02}:{sec:02}.{mil:02}"


def actualizar_timer():
    if running:
        t = time.time() - start_time
        timer.config(text=transform_time(t))
        root.after(10, actualizar_timer)


def start_timer():
    global start_time, running

    running = True
    start_time = time.time()
    actualizar_timer()


def stop_timer():
    global running
    running = False

def create_split(name):
    return Split(name)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    root.title("Voyas")

    start_time = 0
    running = False

    boton_start = tk.Button(root, text="Start", command=start_timer)
    boton_start.pack()

    boton_stop = tk.Button(root, text="Stop", command=stop_timer)
    boton_stop.pack()

    timer = tk.Label(root, text = transform_time(0), font=("Helvetica", 24))
    timer.pack()

    root.mainloop()