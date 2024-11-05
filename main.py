import csv
import keyboard
import tkinter as tk
from tkinter import messagebox
import time
from Split import Split


def leer_splits(file_path):
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        initial_splits = list(reader)

    for split in initial_splits:
        split[1] = float(split[1])
        split[2] = float(split[2])

    return initial_splits


def escribir_splits(file_path):
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(splits)


def transform_time(t):
    if t == "":
        return ""

    sing = "+"
    if t < 0:
        t = abs(t)
        sing = "-"

    mil = int((t % 1) * 100)
    sec = int(t % 60)
    minutes = int((t // 60) % 60)
    hours = int(t // 3600)

    return f"{sing}{hours:02}:{minutes:02}:{sec:02}.{mil:02}"


def actualizar_timer():
    global runtime

    if running:
        runtime = time.time() - start_time

        if split_actual >= len(splits):
            return
        if runtime < splits[split_actual][2]:
            color = "green"
        else:
            color = "red"

        timer.config(text=transform_time(runtime), fg=color)
        root.after(10, actualizar_timer)


def set_split(index, name, delta, time2):
    bg_color = "#333333" if index % 2 == 0 else "#000000"  # Alterna colores de fondo
    fg_color = "white"

    nombre_label = tk.Label(frame_splits, text=name, anchor="w", bg=bg_color, fg=fg_color)
    nombre_label.grid(row=index, column=0, sticky="nsew")

    if actual_run_times[index][1] < splits[index][1]:
        color = "#b0a527"
    elif actual_run_times[index][2] < splits[index][2]:
        color = "green"
    else:
        color = "red"

    delta_label = tk.Label(frame_splits, text=transform_time(delta), anchor="w", fg=color, bg=bg_color)
    delta_label.grid(row=index, column=1, sticky="nsew")

    best_time_label = tk.Label(frame_splits, text=transform_time(time2), anchor="w", bg=bg_color, fg=fg_color)
    best_time_label.grid(row=index, column=2, sticky="nsew")


def init_split(index, name, time_pb):
    bg_color = "#333333" if index % 2 == 0 else "#000000"  # Alterna colores de fondo
    fg_color = "white"

    nombre_label = tk.Label(frame_splits, text=name, anchor="w", bg=bg_color, fg=fg_color)
    nombre_label.grid(row=index, column=0, sticky="nsew")

    best_time_label = tk.Label(frame_splits, text=transform_time(time_pb), anchor="w", bg=bg_color, fg=fg_color)
    best_time_label.grid(row=index, column=2, sticky="nsew")


def clear_deltas():
    for i in range(len(splits)):
        delta = tk.Label(frame_splits, text="", anchor="w", bg="#333333" if i % 2 == 0 else "#000000", fg="white")
        delta.grid(row=i, column=1, sticky="nsew")


def pasar_split():
    global split_actual, start_time, running, start_split_time
    guardar_split_en_run()

    split = splits[split_actual]

    delta_time = time.time() - (split[2] + start_time)

    set_split(split_actual, split[0], delta_time, runtime)

    split_actual += 1

    start_split_time = time.time()


def guardar_split_en_run():
    global actual_run_times

    time_split = time.time() - start_split_time

    actual_run_times.append([splits[split_actual][0], time_split, runtime])


def guardar_tiempo_de_cada_splits():
    for i in range(len(splits)):
        if actual_run_times[i][1] < splits[i][1]:  # Si el tiempo del split es mejor q el historico se guarda
            splits[i][1] = actual_run_times[i][1]


def check_pb():
    if actual_run_times[-1][2] < splits[-1][2]:
        for i, split_run in enumerate(actual_run_times):
            splits[i][2] = split_run[2]  # Actualiza el tiempo del split


def split_start():
    global running, start_time, split_actual, start_split_time, actual_run_times

    if not running:  # Start
        clear_deltas()

        crear_splits()

        running = True
        split_actual = 0
        start_time = time.time()
        start_split_time = start_time
        actual_run_times = []
        actualizar_timer()
    elif split_actual == len(splits) - 1:  # Split final
        pasar_split()
        running = False

        guardar_tiempo_de_cada_splits()
        check_pb()

    else:  # Split Normal
        pasar_split()


def restart_timer():
    global running
    running = False

    clear_deltas()


def crear_splits():
    for row_index, split in enumerate(splits):
        init_split(row_index, split[0], split[2])


def crear_botones():
    boton_restart = tk.Button(root, text="Restart", command=restart_timer, bg="gray", fg="white")
    boton_restart.pack()

    #Botón para abrir el asistente de creacion de splits
    boton_wizard = tk.Button(root, text="Asistente", command=open_wizard_splits, bg="gray", fg="white")
    boton_wizard.pack()

def open_wizard_splits():
    wizard = tk.Tk()
    wizard.geometry("600x600")
    wizard.title("Wizard")

    wizard.configure(bg="white")
    wizard.protocol("WM_DELETE_WINDOW", lambda: closing_wizard(wizard))


def closing_wizard(wizard):
    if messagebox.askyesno("Salir", "¿Deseas salir del wizard?"):
        wizard.destroy()

def on_closing():
    if messagebox.askyesno("Guardar tiempos", "¿Deseas guardar los tiempos actuales antes de salir?"):
        escribir_splits("splits.csv")
    root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x300")
    root.title("Voyas")

    root.configure(bg="black")  # Fondo negro para la ventana principal
    root.protocol("WM_DELETE_WINDOW", on_closing)

    start_time = float()
    start_split_time = float()
    running = False
    split_actual = int()
    actual_run_times = list()
    runtime = float()

    initial_splits = leer_splits("splits.csv")
    splits = initial_splits

    crear_botones()

    timer = tk.Label(root, text=transform_time(0), font=("Helvetica", 24), bg="black", fg="white")
    timer.pack()

    frame_splits = tk.Frame(root, bg="black")  # Fondo negro para el frame de splits
    frame_splits.pack()

    frame_splits.grid_columnconfigure(0, weight=70, minsize=150)
    frame_splits.grid_columnconfigure(1, weight=15, minsize=75)
    frame_splits.grid_columnconfigure(2, weight=15, minsize=75)

    crear_splits()
    clear_deltas()

    keyboard.add_hotkey(" ", split_start)

    root.mainloop()
