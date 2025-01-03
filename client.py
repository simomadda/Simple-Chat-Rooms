import tkinter as tk
import customtkinter as ctk
from tkinter import scrolledtext
import socketio

# Connect to the server
sio = socketio.Client()

def connect_to_server():
    try:
        sio.connect('https://99a6fb10-f9cf-4a43-a9a3-20f6890b9b6d-00-2k3c696iv73ye.spock.replit.dev/')  # Replace with your Replit URL
        chat_window.insert(tk.END, "Connected to the server.\n")
    except Exception as e:
        chat_window.insert(tk.END, f"Error connecting to server: {e}\n")

@sio.on('room_created')
def on_room_created(data):
    chat_window.insert(tk.END, f"{data['message']}\n")

@sio.on('room_joined')
def on_room_joined(data):
    chat_window.insert(tk.END, f"{data['message']}\n")
    send_button.configure(state=ctk.NORMAL)  # Enable sending messages

@sio.on('room_error')
def on_room_error(data):
    chat_window.insert(tk.END, f"Error: {data['message']}\n")

@sio.on('receive_message')
def on_receive_message(data):
    chat_window.insert(tk.END, f"{data['username']}: {data['message']}\n")
    chat_window.yview_moveto(1.0)  # Scroll to the latest message

def create_room():
    username = username_entry.get()
    room = room_entry.get()
    code = code_entry.get()
    if username and room and code:
        sio.emit('create_or_join', {'username': username, 'room': room, 'code': code, 'is_new_room': True})
    else:
        chat_window.insert(tk.END, "Enter username, room name, and code to create a room.\n")

def join_room():
    username = username_entry.get()
    room = room_entry.get()
    code = code_entry.get()
    if username and room and code:
        sio.emit('create_or_join', {'username': username, 'room': room, 'code': code, 'is_new_room': False})
    else:
        chat_window.insert(tk.END, "Enter username, room name, and code to join a room.\n")

def send_message(event=None):
    username = username_entry.get()
    room = room_entry.get()
    message = message_entry.get()
    if username and room and message:
        sio.emit('send_message', {'username': username, 'room': room, 'message': message})
        message_entry.delete(0, ctk.END)
    else:
        chat_window.insert(tk.END, "Enter a message to send.\n")

# Set up CustomTkinter Appearance
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

# Create the GUI
root = ctk.CTk()
root.title("3DS PRIVATE LINE")
root.geometry("600x500")

# Frame to hold entry fields and buttons
frame = ctk.CTkFrame(root)
frame.pack(pady=10, padx=10, fill="x")

username_label = ctk.CTkLabel(frame, text="Username:")
username_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
username_entry = ctk.CTkEntry(frame, width=200)
username_entry.grid(row=0, column=1, padx=5, pady=5)

room_label = ctk.CTkLabel(frame, text="Room:")
room_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
room_entry = ctk.CTkEntry(frame, width=200)
room_entry.grid(row=1, column=1, padx=5, pady=5)

code_label = ctk.CTkLabel(frame, text="Room Code:")
code_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
code_entry = ctk.CTkEntry(frame, width=200, show="*")
code_entry.grid(row=2, column=1, padx=5, pady=5)

create_button = ctk.CTkButton(frame, text="Create Room", command=create_room)
create_button.grid(row=3, column=0, padx=5, pady=10)
join_button = ctk.CTkButton(frame, text="Join Room", command=join_room)
join_button.grid(row=3, column=1, padx=5, pady=10)

# Chat window to display messages
chat_window = scrolledtext.ScrolledText(root, wrap="word", height=15, width=70)
chat_window.pack(padx=10, pady=10, fill="both", expand=True)
chat_window.insert(tk.END, "Welcome to 3DS PRIVATE LINE!\n")

# Add the message entry box
message_entry = ctk.CTkEntry(root, placeholder_text="Type your message here...")
message_entry.pack(padx=10, pady=10, fill="x")

# Bind the "Enter" key to the send_message function
message_entry.bind('<Return>', send_message)

# Add the send button
send_button = ctk.CTkButton(root, text="Send", command=send_message, state=ctk.DISABLED)
send_button.pack(padx=10, pady=10)

# Connect to the server after setting up the GUI
connect_to_server()

root.mainloop()
