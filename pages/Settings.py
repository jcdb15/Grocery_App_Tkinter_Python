# Settings.py
import tkinter as tk

def show_settings_page(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="Settings", font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(content_frame, text="Settings page is under construction.").pack(pady=20)
