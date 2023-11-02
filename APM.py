import tkinter as tk
import keyboard
import time

class KeyboardMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Keyboard Monitor")
        
        self.shift_count = 0
        self.key_count = 0
        self.apm = 0

        self.shift_label = tk.Label(root, text="Shift Inputs: 0")
        self.apm_label = tk.Label(root, text="APM: 0")
        
        self.shift_label.pack()
        self.apm_label.pack()
        
        keyboard.on_press(self.key_pressed)

        self.start_time = time.time()
        self.update_apm()

    def key_pressed(self, e):
        self.key_count += 1
        if 'shift' in keyboard._pressed_events:
            self.shift_count += 1

        self.update_labels()

    def update_labels(self):
        self.shift_label.config(text=f"Shift Inputs: {self.shift_count}")
        self.apm_label.config(text=f"APM: {self.apm:.2f}")

    def update_apm(self):
        elapsed_time = time.time() - self.start_time
        self.apm = (self.key_count / elapsed_time) * 60
        self.update_labels()
        self.root.after(1000, self.update_apm)

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyboardMonitorApp(root)
    root.mainloop()