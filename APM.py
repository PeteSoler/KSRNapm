import tkinter as tk
from tkinter import ttk
from pynput import keyboard
import time
import atexit

# Global variables to keep track of keystrokes, time, 'q' key presses, and 'Shift' key presses
keystrokes = 0
shift_key_counter = 0
start_time = time.time()
q_key_counter = 0
elapsed_time = 0
kpm = 0

def on_key_release(key):
    global keystrokes, shift_key_counter, q_key_counter
    if hasattr(key, 'char'):
        keystrokes += 1
        if key.char == 'q':
            q_key_counter += 1
    if hasattr(key, 'name'):
        if key.name == 'shift':
            shift_key_counter += 1

def calculate_kpm(total_keystrokes, elapsed_time):
    return total_keystrokes / (elapsed_time / 60)

# Create a keyboard listener
keyboard_listener = keyboard.Listener(on_release=on_key_release)
keyboard_listener.start()

# Create the GUI window
window = tk.Tk()
window.title("Keyboard Inputs Per Minute")

# Timer label at the top
timer_label = ttk.Label(window, text="00:00:00")
timer_label.pack(padx=20, pady=10)

# Label to display KPM
kpm_label = ttk.Label(window, text="KPM: 0.00")
kpm_label.pack(padx=20, pady=10)

# Label to display 'q' key counter
q_key_label = ttk.Label(window, text="'q' Key Presses: 0")
q_key_label.pack(padx=20, pady=10)

# Label to display 'Shift' key counter
shift_key_label = ttk.Label(window, text="'Shift' Key Presses: 0")
shift_key_label.pack(padx=20, pady=10)

# File to save data
data_file = open("keyboard_data.txt", "w")

def update_labels():
    global elapsed_time, kpm
    while True:
        # Calculate elapsed time
        current_time = time.time()
        elapsed_time = current_time - start_time

        # Format the elapsed time as HH:MM:SS
        formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        timer_label.config(text=formatted_time)

        # Calculate KPM
        kpm = calculate_kpm(keystrokes, elapsed_time)
        kpm_label.config(text=f"KPM: {kpm:.2f}")

        # Update 'q' key counter
        q_key_label.config(text=f"'q' Key Presses: {q_key_counter}")

        # Update 'Shift' key counter
        shift_key_label.config(text=f"'Shift' Key Presses: {shift_key_counter}")

        # Update the labels every second
        window.update()
        time.sleep(1)

# Register a function to save data when the script exits
@atexit.register
def save_data_to_file():
    data_file.write(f"Total Keystrokes: {keystrokes}\n")
    data_file.write(f"'q' Key Presses: {q_key_counter}\n")
    data_file.write(f"'Shift' Key Presses: {shift_key_counter}\n")
    data_file.write(f"Total Time: {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}\n")
    data_file.write(f"KPM: {kpm:.2f}\n")
    data_file.close()

# Start a separate thread to update the labels
import threading
update_thread = threading.Thread(target=update_labels)
update_thread.daemon = True
update_thread.start()

# Main loop to keep the GUI window open
window.mainloop()

# Gracefully exit the script on window close
keyboard_listener.stop()
