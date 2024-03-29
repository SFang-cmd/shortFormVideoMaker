import tkinter as tk

window = tk.Tk()
label = tk.Label(text="Generate Reddit Vids")
subreddit = tk.Label(text="Which subreddit?")
number = tk.Label(text="How many videos?")
videos = tk.Label(text="How many videos?")
number_vids = tk.Entry()
tk.Frame()


label.pack()
subreddit.pack()
number.pack()
videos.pack()
number_vids.pack()

window.mainloop()