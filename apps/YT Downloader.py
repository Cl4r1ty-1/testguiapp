import tkinter
import customtkinter
from pytube import YouTube
from pytube import exceptions
from tkinter import filedialog

def startDownload():
    try:
        progress.set(0)
        download.configure(state='disabled')
        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        video = ytObject.streams.get_by_resolution(resolution=chooseResolution.get())
        title.configure(text=ytObject.title, text_color='white')
        finishLabel.configure(text='')

        video.download(output_path=file_path)
        finishLabel.configure(text="Download Complete!", text_color='white')
        download.configure(state='normal')
    except AttributeError:
        finishLabel.configure(text="Try either 720p or 360p.", text_color='red')
        download.configure(state='normal')
    except exceptions.RegexMatchError:
        finishLabel.configure(text="YouTube link is invalid!", text_color='red')
        download.configure(state='normal')
    except NameError:
        finishLabel.configure(text="No/invalid directory selected", text_color='red')
        download.configure(state='normal')

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    pPercent.configure(text=per + '%')
    pPercent.update()

    progress.set(float(percentage_of_completion) / 100)

def select_folder():
    global file_path
    file_path = filedialog.askdirectory()
    folder_chosen.configure(text=file_path)

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("720x480")
app.title("YT Downloader")

title = customtkinter.CTkLabel(app, text="Insert a YouTube Link")
title.pack(padx=10, pady=10)

url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack(pady=5)

resolution = tkinter.StringVar()
chooseResolution = customtkinter.CTkOptionMenu(app, values=["720p", "480p", "360p", "240p", "144p"])
chooseResolution.pack(padx=10, pady=10)

choosefolder = customtkinter.CTkButton(app, text="Choose where to download", command=select_folder)
choosefolder.pack(padx=10, pady=10)

folder_chosen = customtkinter.CTkLabel(app, text='')
folder_chosen.pack()

download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.pack(padx=10, pady=5)

finishLabel = customtkinter.CTkLabel(app, text='')
finishLabel.pack()

pPercent = customtkinter.CTkLabel(app, text="0%")
pPercent.pack()

progress = customtkinter.CTkProgressBar(app, width=400)
progress.set(0)
progress.pack(padx=10, pady=10)


app.mainloop()
