import tkinter as tk
from tkinter import scrolledtext
import keyboard
import threading
from utils import llm_chatter
import pystray
from PIL import Image
import os
# Hide the console
if os.name == 'nt':
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
else:
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
llm_chatter = llm_chatter()

# Function to handle user input and generate a reply
def on_enter_pressed(event=None):
    user_input = entry.get()
    if user_input:
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, f"You: {user_input}\n")
        entry.delete(0, tk.END)

        # Generate the reply
        reply = generate_reply(user_input)
        chat_log.insert(tk.END, f"Bot: {reply}\n")
        chat_log.yview(tk.END)
        chat_log.config(state=tk.DISABLED)

# Function to generate a reply
def generate_reply(input_text):
    return llm_chatter.communicate(input_text)

# Function to create the chat window
def create_chat_window():
    chat_window = tk.Toplevel()
    chat_window.title("Chat Bot")

    # Setting up the chat log (display area)
    global chat_log
    chat_log = scrolledtext.ScrolledText(chat_window, state=tk.DISABLED, wrap=tk.WORD, height=20)
    chat_log.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

    # Setting up the entry field (input area)
    global entry
    entry = tk.Entry(chat_window)
    entry.pack(padx=10, pady=5, fill=tk.X)
    entry.bind("<Return>", on_enter_pressed)

    # Center the window
    window_width = 400
    window_height = 450
    screen_width = chat_window.winfo_screenwidth()
    screen_height = chat_window.winfo_screenheight()
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)

    chat_window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
    chat_window.lift()
    chat_window.focus_force()
    entry.focus()


def exit_application(icon, item):
    try:
        exit()
        root.after(0, root.quit)
    except SystemExit:
        icon.stop()
        root.after(0, root.quit)


# Function to start the chat window
def start_chat_window():
    llm_chatter.msg_history = []
    root.after(0, create_chat_window)

# Function to create the system tray icon
def create_system_tray_icon():
    image = Image.open("assets/icon.png")  # Replace with the path to your icon

    menu = pystray.Menu(
        pystray.MenuItem("Open", lambda icon, item: root.after(0, start_chat_window)),
        pystray.MenuItem("Exit", exit_application)
    )
    icon = pystray.Icon("name", image, "My System Tray Icon", menu)
    icon.run()

# Setting up the key combination
root = tk.Tk()
root.withdraw()

# Adding the hotkey
keyboard.add_hotkey('alt+d', lambda: root.after(0, start_chat_window))

# Create the system tray icon in a new thread
icon_thread = threading.Thread(target=create_system_tray_icon)
icon_thread.start()

# Start the main Tkinter event loop
root.mainloop()
