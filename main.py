import tkinter as tk
from tkinter import scrolledtext
import keyboard
import threading
from utils import llm_chatter



llm_chatter = llm_chatter()

# Function to handle user input and generate a reply
def on_enter_pressed(event=None):
    user_input = entry.get()
    if user_input:
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, f"You: {user_input}\n")
        entry.delete(0, tk.END)

        # Generate the reply (currently always "Hello")
        reply = generate_reply(user_input)
        chat_log.insert(tk.END, f"Bot: {reply}\n")
        chat_log.yview(tk.END)
        chat_log.config(state=tk.DISABLED)

# Function to generate a reply, currently returns "Hello"
def generate_reply(input_text):
    return llm_chatter.communicate(input_text)

# Function to create the chat window
def create_chat_window():
    chat_window = tk.Tk()
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

    chat_window.geometry("400x450")
    entry.focus()
    chat_window.mainloop()

# Function to start the chat window in a new thread
def start_chat_window():
    chat_thread = threading.Thread(target=create_chat_window)
    chat_thread.start()

# Setting up the key combination
keyboard.add_hotkey('alt+d', start_chat_window)

# Keep the program running
keyboard.wait('esc')  # The program will keep running until you press 'esc'
