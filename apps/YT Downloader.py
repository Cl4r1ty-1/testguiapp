import tkinter
import customtkinter
from pytube import YouTube

def startDownload():
    try:
        progress.set(0)
        download.configure(state='disabled')
        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        video = ytObject.streams.get_highest_resolution()

        title.configure(text=ytObject.title, text_color='white')
        finishLabel.configure(text='')

        video.download()
        finishLabel.configure(text="Download Complete!")
        download.configure(state='normal')
    except:
        finishLabel.configure(text="YouTube link is invalid", text_color='red')


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    pPercent.configure(text=per + '%')
    pPercent.update()

    progress.set(float(percentage_of_completion) / 100)

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("720x480")
app.title("YT Downloader")

title = customtkinter.CTkLabel(app, text="Insert a YouTube Link")
title.pack(padx=10, pady=10)

url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()


finishLabel = customtkinter.CTkLabel(app, text='')
finishLabel.pack()

pPercent = customtkinter.CTkLabel(app, text="0%")
pPercent.pack()

progress = customtkinter.CTkProgressBar(app, width=400)
progress.set(0)
progress.pack(padx=10, pady=10)

download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.pack(padx=10, pady=10)



app.mainloop()
