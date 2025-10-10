import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pygame
import cv2
import threading

class MultimediaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Multimedia Application")
        self.img_label = tk.Label(root)
        self.img_label.pack()
        self.btn_img = tk.Button(root, text="Load Image", command=self.load_image)
        self.btn_img.pack()
        self.btn_sound = tk.Button(root, text="Play Sound", command=self.play_sound)
        self.btn_sound.pack()
        self.btn_video = tk.Button(root, text="Play Video", command=self.play_video)
        self.btn_video.pack()
        pygame.mixer.init()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            img = Image.open(file_path)
            img = img.resize((300, 300))
            img_tk = ImageTk.PhotoImage(img)
            self.img_label.config(image=img_tk)
            self.img_label.image = img_tk

    def play_sound(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
        if file_path:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()

    def play_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi")])
        if file_path:
            threading.Thread(target=self._play_video_thread, args=(file_path,), daemon=True).start()

    def _play_video_thread(self, file_path):
        cap = cv2.VideoCapture(file_path)
        cv2.namedWindow("Video", cv2.WINDOW_NORMAL)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Video", frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = MultimediaApp(root)
    root.mainloop()