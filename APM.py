import tkinter as tk
from tkinter import ttk
from pynput import keyboard
import time

# Global variables to keep track of keystrokes and time
keystrokes = 0
start_time = time.time()

def on_key_release(key):
    global keystrokes
    if hasattr(key, 'char'):
        keystrokes += 1

def calculate_kpm(total_keystrokes, elapsed_time):
    return total_keystrokes / (elapsed_time / 60)

# Create a keyboard listener
keyboard_listener = keyboard.Listener(on_release=on_key_release)
keyboard_listener.start()

# Create the GUI window
window = tk.Tk()
window.title("Keyboard Inputs Per Minute")

# Label to display KPM
kpm_label = ttk.Label(window, text="KPM: 0.00")
kpm_label.pack(padx=20, pady=20)

def update_kpm_label():
    while True:
        # Calculate elapsed time
        current_time = time.time()
        elapsed_time = current_time - start_time

        # Calculate KPM
        kpm = calculate_kpm(keystrokes, elapsed_time)
        kpm_label.config(text=f"KPM: {kpm:.2f}")

        # Update the label every second
        window.update()
        time.sleep(1)

# Start a separate thread to update the KPM label
import threading
kpm_thread = threading.Thread(target=update_kpm_label)
kpm_thread.daemon = True
kpm_thread.start()

# Main loop to keep the GUI window open
window.mainloop()

# Gracefully exit the script on window close
keyboard_listener.stop()
