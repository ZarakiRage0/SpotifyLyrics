#!/usr/bin/python
import tkinter as tk
import tkinter.scrolledtext
from songGenius import *
import spotify
from PIL import Image, ImageTk
from urllib.request import urlopen
import io


def setup_root():
    root.wm_iconbitmap('lyrics.ico')
    root.resizable(height=None, width=None)
    root.title("LyricsGUI")
    root.geometry("1000x600")
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)


def write_lyrics(lyrics, title):
    text.delete("1.0", tk.END)
    title_box.delete("1.0", tk.END)
    title_box.insert(tk.INSERT, title, "title")
    text.insert(tk.END, lyrics)


def write_image(album_uri):
    album_info = spotify_client.album(album_id=album_uri)
    image_url = album_info["images"][0]["url"]
    global my_page, my_picture, pil_img, tk_img
    my_page = urlopen(image_url)
    my_picture = io.BytesIO(my_page.read())
    pil_img = Image.open(my_picture)
    width, height = pil_img.size
    pil_img = pil_img.resize((round(200 / height * width), round(200)), Image.ANTIALIAS)
    tk_img = ImageTk.PhotoImage(pil_img)
    l1.configure(image=tk_img)
    l1.image = tk_img


def display():
    title, artists, album, image = spotify.get_song(spotify_client)
    title = get_song_title_without_parentheses(title=title)
    if not song.title_compare(title=title):
        song.search_lyrics(title=title, artist=artists[0]["name"], album=album, image=image)
        write_lyrics(song.get_lyrics(), song.get_song_title())
        write_image(song.get_album_uri())
    root.after(delay * 1000, display)


spotify_client = spotify.set_up_spotify()
song = Song()
delay = 1  # delay in seconds
root = tk.Tk()

setup_root()
text = tk.scrolledtext.ScrolledText(root, font=("JetBrains Mono", 13), padx=50, pady=1, fg="#A9B7C6", bg="#2B2B2B",
                                    spacing3=1.2, wrap=tk.WORD, relief="flat")
title_box = tk.Text(root, font=("JetBrains Mono", 13), padx=10, pady=10, fg="#A9B7C6", bg="#2B2B2B",
                    spacing3=1.2, wrap=tk.WORD, relief="flat")
title_box.configure(height=2)

text.tag_configure("center", justify="center")
text.tag_configure("title", justify="center", font=("JetBrains Mono", 20))
title_box.tag_configure("center", justify="center")
title_box.tag_configure("title", justify="center", font=("JetBrains Mono", 20))

text.pack(expand=tk.YES, fill=tk.BOTH, side=tk.BOTTOM)
title_box.pack(fill=tk.BOTH, side=tk.TOP)

url = "https://i.scdn.co/image/ab67616d0000b27308a1b1e0674086d3f1995e1b"
my_page = urlopen(url)
my_picture = io.BytesIO(my_page.read())
pil_img = Image.open(my_picture)
tk_img = ImageTk.PhotoImage(pil_img)

l1 = tk.Label(text, image=tk_img, relief="flat")
l1.configure(width=200, height=200)
l1.pack(side=tk.BOTTOM, anchor=tk.SE)

display()
root.mainloop()
