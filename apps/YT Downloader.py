import os
import tkinter
import customtkinter
from pytubefix import YouTube
from pytubefix import exceptions
from tkinter import filedialog
from datetime import datetime
from moviepy.editor import VideoFileClip, AudioFileClip


def startDownload():
    try:
        progress.set(0)
        download.configure(state='disabled')
        downloadmp3.configure(state='disabled')
        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        if chooseResolution.get() == '1080p':
            for i in ytObject.streams.filter(resolution='1080p'):
                if i.mime_type == 'video/mp4':
                    streamId = i.itag
            video = ytObject.streams.get_by_itag(streamId)
            title.configure(text=ytObject.title, text_color='white')
            finishLabel.configure(text='')
            video_file = video.download(output_path=file_path, filename_prefix='video_')
            for i in ytObject.streams.filter(only_audio=True):
                if i.mime_type == "audio/mp4":
                    audioStreamId = i.itag
            audio = ytObject.streams.get_by_itag(audioStreamId)
            audio_file = audio.download(output_path=file_path, filename_prefix='audio_')
            video_clip = VideoFileClip(video_file)
            audio_clip = AudioFileClip(audio_file)
            final_clip = video_clip.set_audio(audio_clip)
            now = datetime.now()
            dt_string = now.strftime(" %d%m%Y %H%M%S")
            final_clip.write_videofile(file_path + '/' + 'YouTubeDownload' + dt_string + '.mp4')
            os.remove(audio_file)
            os.remove(video_file)

        else:
            video = ytObject.streams.get_by_resolution(resolution=chooseResolution.get())
            title.configure(text=ytObject.title, text_color='white')
            finishLabel.configure(text='')

            video.download(output_path=file_path)
        finishLabel.configure(text="Download Complete!", text_color='white')
        downloadmp3.configure(state='normal')
        download.configure(state='normal')
    except AttributeError:
        finishLabel.configure(text="Try either 720p or 360p. If 720p is selected it may not be avaliable for download for this video, please try 1080p (may take a few minutes) or 360p", text_color='red')
        download.configure(state='normal')
        downloadmp3.configure(state='normal')
    except exceptions.RegexMatchError:
        finishLabel.configure(text="YouTube link is invalid!", text_color='red')
        download.configure(state='normal')
        downloadmp3.configure(state='normal')
    except NameError:
        finishLabel.configure(text="No/invalid directory selected", text_color='red')
        download.configure(state='normal')
        downloadmp3.configure(state='normal')
    except:
        finishLabel.configure(text="An unknown error occurred. Please contact devs.", text_color='red')
        download.configure(state='normal')
        downloadmp3.configure(state='normal')


def startAudioDownload():
    try: 
        progress.set(0)
        downloadmp3.configure(state='disabled')
        download.configure(state='disabled')
        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        for i in ytObject.streams.filter(only_audio=True):
            if i.mime_type == "audio/mp4":
                streamId = i.itag
        video = ytObject.streams.get_by_itag(streamId)
        title.configure(text=ytObject.title, text_color='white')
        finishLabel.configure(text='')

        out_file = video.download(output_path=file_path, filename_prefix='audio_')
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

        finishLabel.configure(text="Download Complete!", text_color='white')
        download.configure(state='normal')
        downloadmp3.configure(state='normal')
    except exceptions.RegexMatchError:
        finishLabel.configure(text="YouTube link is invalid!", text_color='red')
        download.configure(state='normal')
        downloadmp3.configure(state='normal')
    except NameError:
        finishLabel.configure(text="No/invalid directory selected", text_color='red')
        download.configure(state='normal')
        downloadmp3.configure(state='normal')
    except:
        finishLabel.configure(text="An unknown error occurred. Please contact devs.", text_color='red')
        download.configure(state='normal')
        downloadmp3.configure(state='normal')

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

print("Welcome to YTDownloader! The purpose of this console window is to show you the progress of 1080p downloads, other than that you can pretty much ignore it.")
print()
print("Loading...")

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("870x550")
app.title("YT Downloader")

title = customtkinter.CTkLabel(app, text="Insert a YouTube Link")
title.pack(padx=10, pady=10)

url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=400, height=40, textvariable=url_var)
link.pack(pady=5)

resolution = tkinter.StringVar()
chooseResolution = customtkinter.CTkOptionMenu(app, values=["720p", "480p", "360p", "240p", "144p", "1080p"])
chooseResolution.pack(padx=10, pady=10)

warningText = customtkinter.CTkLabel(app, text='Warning: 1080p downloads take a long time as there are many more steps to getting a 1080p YouTube video than just \ndownloading, please consider downloading 720p unless you absolutely have to get 1080p video. \nA 1080p download is complete when the download buttons are no longer greyed-out.\nIf app freezes, this is normal, once it starts responding again after a while the download will most likey be done.', text_color='orange')
warningText.pack()

choosefolder = customtkinter.CTkButton(app, text="Choose where to download", command=select_folder)
choosefolder.pack(padx=10, pady=10)

folder_chosen = customtkinter.CTkLabel(app, text='')
folder_chosen.pack()

download = customtkinter.CTkButton(app, text="Download", command=startDownload)
download.pack(padx=10, pady=5)

info_text = customtkinter.CTkLabel(app, text="If downloading audio only, don't worry about changing resolution.")
info_text.pack(padx=10, pady=5)

downloadmp3 = customtkinter.CTkButton(app, text="Download MP3 (Audio only)", command=startAudioDownload)
downloadmp3.pack(padx=10, pady=5)

finishLabel = customtkinter.CTkLabel(app, text='')
finishLabel.pack()

pPercent = customtkinter.CTkLabel(app, text="0%")
pPercent.pack()

progress = customtkinter.CTkProgressBar(app, width=400)
progress.set(0)
progress.pack(padx=10, pady=10)


app.mainloop()
