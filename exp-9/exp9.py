import socket
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext
from PIL import Image, ImageTk
import pygame
import os

HOST = '127.0.0.1'  # Change to server IP for client
PORT = 5001

class MultimediaChat:
    def __init__(self, root, is_server):
        self.root = root
        self.root.title("Multimedia Chat")
        self.text_area = scrolledtext.ScrolledText(root, width=40, height=10)
        self.text_area.pack()
        self.entry = tk.Entry(root, width=30)
        self.entry.pack()
        self.btn_send = tk.Button(root, text="Send Text", command=self.send_text)
        self.btn_send.pack()
        self.btn_img = tk.Button(root, text="Send Image", command=self.send_image)
        self.btn_img.pack()
        self.btn_audio = tk.Button(root, text="Send Audio", command=self.send_audio)
        self.btn_audio.pack()
        self.img_label = tk.Label(root)
        self.img_label.pack()
        pygame.mixer.init()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_server = is_server
        self.setup_connection()
        threading.Thread(target=self.receive, daemon=True).start()

    def setup_connection(self):
        if self.is_server:
            self.sock.bind((HOST, PORT))
            self.sock.listen(1)
            self.text_area.insert(tk.END, "Waiting for connection...\n")
            self.conn, _ = self.sock.accept()
            self.text_area.insert(tk.END, "Connected!\n")
        else:
            self.sock.connect((HOST, PORT))
            self.conn = self.sock

    def send_text(self):
        msg = self.entry.get()
        if msg:
            self.conn.sendall(b'TEXT:' + msg.encode())
            self.text_area.insert(tk.END, "You: " + msg + "\n")
            self.entry.delete(0, tk.END)

    def send_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            with open(file_path, 'rb') as f:
                data = f.read()
            filename = os.path.basename(file_path)
            self.conn.sendall(b'IMAGE:' + filename.encode() + b':' + data)
            self.text_area.insert(tk.END, "You sent an image: " + filename + "\n")

    def send_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
        if file_path:
            with open(file_path, 'rb') as f:
                data = f.read()
            filename = os.path.basename(file_path)
            self.conn.sendall(b'AUDIO:' + filename.encode() + b':' + data)
            self.text_area.insert(tk.END, "You sent audio: " + filename + "\n")

    def receive(self):
        while True:
            try:
                data = self.conn.recv(4096)
                if not data:
                    break
                if data.startswith(b'TEXT:'):
                    msg = data[5:].decode()
                    self.text_area.insert(tk.END, "Peer: " + msg + "\n")
                elif data.startswith(b'IMAGE:'):
                    parts = data.split(b':', 2)
                    filename = parts[1].decode()
                    img_data = parts[2]
                    with open('received_' + filename, 'wb') as f:
                        f.write(img_data)
                    img = Image.open('received_' + filename)
                    img = img.resize((150, 150))
                    img_tk = ImageTk.PhotoImage(img)
                    self.img_label.config(image=img_tk)
                    self.img_label.image = img_tk
                    self.text_area.insert(tk.END, "Received image: " + filename + "\n")
                elif data.startswith(b'AUDIO:'):
                    parts = data.split(b':', 2)
                    filename = parts[1].decode()
                    audio_data = parts[2]
                    with open('received_' + filename, 'wb') as f:
                        f.write(audio_data)
                    pygame.mixer.music.load('received_' + filename)
                    pygame.mixer.music.play()
                    self.text_area.insert(tk.END, "Received audio: " + filename + "\n")
            except Exception as e:
                self.text_area.insert(tk.END, "Error: " + str(e) + "\n")
                break

if __name__ == "__main__":
    is_server = tk.messagebox.askyesno("Server or Client", "Run as server?")
    root = tk.Tk()
    app = MultimediaChat(root, is_server)
    root.mainloop()