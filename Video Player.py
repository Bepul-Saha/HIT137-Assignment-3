import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2

# Initialize the Tkinter window
root = tk.Tk()
root.title("Tkinter Video Player")
root.geometry("800x600")

# Create a label to display the video frames
video_label = tk.Label(root)
video_label.pack()

# Global variables
cap = None
paused = False

def open_video():
    global cap
    file_path = filedialog.askopenfilename(
        filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")]
    )
    if file_path:
        cap = cv2.VideoCapture(file_path)
        play_video()

def play_video():
    if cap is not None and not paused:
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.config(image=imgtk)
            video_label.image = imgtk
            video_label.after(10, play_video)

def pause_video():
    global paused
    paused = not paused
    if not paused:
        play_video()

def stop_video():
    global cap
    if cap:
        cap.release()
        cap = None
    video_label.config(image='')

def on_closing():
    global cap
    if cap:
        cap.release()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Control buttons
control_frame = tk.Frame(root)
control_frame.pack()

open_button = tk.Button(control_frame, text="Open", command=open_video)
open_button.grid(row=0, column=0, padx=5, pady=5)

play_button = tk.Button(control_frame, text="Play", command=play_video)
play_button.grid(row=0, column=1, padx=5, pady=5)

pause_button = tk.Button(control_frame, text="Pause/Resume", command=pause_video)
pause_button.grid(row=0, column=2, padx=5, pady=5)

stop_button = tk.Button(control_frame, text="Stop", command=stop_video)
stop_button.grid(row=0, column=3, padx=5, pady=5)

# Run the application
root.mainloop()
