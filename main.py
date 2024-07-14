import tkinter as tk
from tkinter import Frame
from tkinter import filedialog
import pygame
from PIL import Image, ImageTk
import os

# GUI of the Music Player
GUI = tk.Tk()
GUI.title("Music Player")
GUI.geometry("350x350")
GUI.config(bg="cadetblue2")

pygame.mixer.init()

menu_space = tk.Menu(GUI)
GUI.config(menu=menu_space)
playlist = tk.Menu(menu_space, tearoff=False)
menu_space.add_cascade(label="Playlist", menu=playlist)

screen = tk.Listbox(GUI, bg="azure3", fg="black", width=54, height=15)
screen.grid(row=0, column=0, padx=10, pady=(10, 0))

# Functions
def resize_img(path, size):
    image = Image.open(path)
    image = image.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(image)

song_list = []
current = ""
paused = False
playing = False

def load_music():
    global current
    GUI.directory = filedialog.askdirectory()

    # Add only mp3 files to the song_list
    for song in os.listdir(GUI.directory):
        name, ext = os.path.splitext(song)
        if ext == '.mp3':
            song_list.append(song)

    for song in song_list:
        screen.insert("end", song)
    screen.select_set(0)
    current = song_list[screen.curselection()[0]]

def toggle_play_pause():
    global current, paused, playing

    if not playing:
        pygame.mixer.music.load(os.path.join(GUI.directory, current))
        pygame.mixer.music.play()
        play_btn.config(image=img_pause)
        playing = True
        paused = False
    elif paused:
        pygame.mixer.music.unpause()
        play_btn.config(image=img_pause)
        paused = False
    else:
        pygame.mixer.music.pause()
        play_btn.config(image=img_play)
        paused = True

def go_next():
    global current, playing, paused

    try:
        screen.selection_clear(0, 'end')
        screen.selection_set(song_list.index(current) + 1)
        current = song_list[screen.curselection()[0]]
        pygame.mixer.music.load(os.path.join(GUI.directory, current))
        pygame.mixer.music.play()
        play_btn.config(image=img_pause)
        playing = True
        paused = False
    except:
        pass

def previous():
    global current, playing, paused

    try:
        screen.selection_clear(0, 'end')
        screen.selection_set(song_list.index(current) - 1)
        current = song_list[screen.curselection()[0]]
        pygame.mixer.music.load(os.path.join(GUI.directory, current))
        pygame.mixer.music.play()
        play_btn.config(image=img_pause)
        playing = True
        paused = False
    except:
        pass

# Buttons
playlist.add_command(label="Select Folder", command=load_music)

img_play = resize_img('play.png', (30, 30))
img_pause = resize_img('pause.png', (30, 30))
img_previous = resize_img('previous.png', (30, 30))
img_next = resize_img('next.png', (30, 30))

button_space = Frame(GUI, bg="cadetblue2", width=54, height=5)
button_space.grid(row=1, column=0, pady=10, padx=10)

play_btn = tk.Button(button_space, image=img_play, bg="azure3", command=toggle_play_pause)
play_btn.grid(row=0, column=1, padx=7, pady=10)
previous_btn = tk.Button(button_space, image=img_previous, bg="azure3", command=previous)
previous_btn.grid(row=0, column=0, padx=7, pady=10)
next_btn = tk.Button(button_space, image=img_next, bg="azure3", command=go_next)
next_btn.grid(row=0, column=2, padx=7, pady=10)

GUI.mainloop()
