import tkinter as tk
from tkinter import filedialog, messagebox
import datetime
import time
import threading
import pygame

# Initialize pygame mixer for playing sounds
pygame.mixer.init()

# Global variables
alarm_thread = None
snooze_minutes = 5
alarm_running = False

def play_alarm(tone_path):
    try:
        pygame.mixer.music.load(tone_path)
        pygame.mixer.music.play(-1)  # Loop until stopped
    except Exception as e:
        messagebox.showerror("Error", f"Could not play alarm tone: {e}")

def stop_alarm():
    pygame.mixer.music.stop()

def alarm_loop(alarm_time, tone_path):
    global alarm_running
    while alarm_running:
        now = datetime.datetime.now().strftime("%H:%M")
        if now == alarm_time:
            play_alarm(tone_path)
            # Show snooze/cancel options
            snooze_cancel_popup(tone_path)
            break
        time.sleep(1)

def snooze_cancel_popup(tone_path):
    def snooze():
        stop_alarm()
        popup.destroy()
        snooze_until = (datetime.datetime.now() + datetime.timedelta(minutes=snooze_minutes)).strftime("%H:%M")
        start_alarm_thread(snooze_until, tone_path)
    
    def cancel():
        global alarm_running
        stop_alarm()
        alarm_running = False
        popup.destroy()

    popup = tk.Toplevel()
    popup.title("Alarm!")
    popup.geometry("200x100")
    tk.Label(popup, text="Wake up!").pack(pady=10)
    btn_frame = tk.Frame(popup)
    btn_frame.pack(pady=5)
    tk.Button(btn_frame, text="Snooze", command=snooze, width=10).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Stop", command=cancel, width=10).pack(side="right", padx=5)

def start_alarm_thread(alarm_time, tone_path):
    global alarm_thread, alarm_running
    alarm_running = True
    alarm_thread = threading.Thread(target=alarm_loop, args=(alarm_time, tone_path))
    alarm_thread.daemon = True
    alarm_thread.start()

def browse_tone():
    file_path = filedialog.askopenfilename(
        title="Select Alarm Tone",
        filetypes=[("Audio Files", "*.mp3 *.wav")]
    )
    if file_path:
        tone_var.set(file_path)

def set_alarm():
    hour = hour_var.get()
    minute = minute_var.get()
    tone_path = tone_var.get()
    if not hour.isdigit() or not minute.isdigit():
        messagebox.showerror("Error", "Please enter valid hour and minute.")
        return
    if not (0 <= int(hour) <= 23 and 0 <= int(minute) <= 59):
        messagebox.showerror("Error", "Hour must be 0-23 and minute 0-59.")
        return
    alarm_time = f"{int(hour):02d}:{int(minute):02d}"
    if not tone_path:
        messagebox.showerror("Error", "Please select an alarm tone.")
        return
    start_alarm_thread(alarm_time, tone_path)
    messagebox.showinfo("Alarm Set", f"Alarm set for {alarm_time}")

# GUI setup
root = tk.Tk()
root.title("Python Alarm Clock")
root.geometry("350x220")
root.resizable(False, False)

hour_var = tk.StringVar()
minute_var = tk.StringVar()
tone_var = tk.StringVar()

frame = tk.Frame(root)
frame.pack(pady=15)

tk.Label(frame, text="Set Alarm Time (24h):").grid(row=0, column=0, columnspan=3, pady=5)
tk.Entry(frame, textvariable=hour_var, width=3, justify="center").grid(row=1, column=0)
tk.Label(frame, text=":").grid(row=1, column=1)
tk.Entry(frame, textvariable=minute_var, width=3, justify="center").grid(row=1, column=2)

tk.Button(root, text="Choose Tone", command=browse_tone, width=20).pack(pady=10)
tk.Label(root, textvariable=tone_var, wraplength=300, fg="blue").pack()

tk.Button(root, text="Set Alarm", command=set_alarm, width=20).pack(pady=10)

# Optional: Allow user to set snooze duration
def set_snooze():
    global snooze_minutes
    val = snooze_entry.get()
    if val.isdigit() and int(val) > 0:
        snooze_minutes = int(val)
        messagebox.showinfo("Snooze Set", f"Snooze set to {snooze_minutes} minutes.")
    else:
        messagebox.showerror("Error", "Enter a valid number (minutes).")

snooze_frame = tk.Frame(root)
snooze_frame.pack(pady=5)
tk.Label(snooze_frame, text="Snooze (minutes):").pack(side="left")
snooze_entry = tk.Entry(snooze_frame, width=3)
snooze_entry.insert(0, "5")
snooze_entry.pack(side="left", padx=5)
tk.Button(snooze_frame, text="Set", command=set_snooze).pack(side="left")

root.mainloop()
