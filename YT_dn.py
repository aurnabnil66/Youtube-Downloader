from tkinter import *
from customtkinter import *
from pytube import YouTube
import os

def start_download():
    try:
        yt_link = link.get()
        
        yt_object = YouTube(yt_link, on_progress_callback=on_progress)
            
        title.configure(text=yt_object.title, text_color="white")
        finish_label.configure(text="")
        
        if check_var_audio.get() == "on":
            audio = yt_object.streams.filter(only_audio=True).first()
            out_file = audio.download()
            base, ext = os.path.splitext(out_file)
            new_name = base + ".mp3"
            os.rename(out_file, new_name)
            finish_label.configure(text="Download Completed!", text_color="green") 
            
        if check_var_video.get() == "on":
            video = yt_object.streams.get_highest_resolution()
            video.download()
            finish_label.configure(text="Download Completed!", font=("Arial", 15, "bold"), text_color="green")  
        
    except:
        finish_label.configure(text="This link is invalid", font=("Arial", 15, "bold"), text_color="red")
    

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percent_of_completion = bytes_downloaded / total_size * 100

    per = str(int(percent_of_completion))
    progress_percent.configure(text=per + "%")
    progress_percent.update()
    
    # update the progress bar
    progress_bar.set(float(percent_of_completion) / 100)
    
    
# system settings
set_appearance_mode("System")
set_default_color_theme("blue")

# the app frame
app = CTk()
app.geometry("720x350")
app.title("Youtube Downloader")
app.iconbitmap("app_icon.ico")   # always have to set .ico format images

# add UI elements
title = CTkLabel(app, text="Insert a Youtube Link", font=("Arial", 20, "bold"))
title.pack(padx=10, pady=10)

# link as input
url_var = StringVar()
link = CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()

# choose options 
check_var_audio = StringVar(value="off")
checkBox_audio =  CTkCheckBox(app, text="Audio", font=("Arial", 15, "bold"), variable=check_var_audio, onvalue="on", offvalue="off")
checkBox_audio.pack(padx=10, pady=10)

check_var_video = StringVar(value="off")
checkBox_video =  CTkCheckBox(app, text="Video", font=("Arial", 15, "bold"), variable=check_var_video, onvalue="on", offvalue="off")
checkBox_video.pack(padx=10, pady=10)

# finished download
finish_label = CTkLabel(app, text="")
finish_label.pack()

# show progress bar
progress_percent = CTkLabel(app, text="0%", font=("Arial", 15, "bold"),)
progress_percent.pack()

progress_bar = CTkProgressBar(app, width=400)
progress_bar.set(0)
progress_bar.pack(padx=10, pady=10)

# button to start download
download = CTkButton(app, text="Download", font=("Arial", 15, "bold"), command=start_download)
download.pack(padx=10, pady=10)

# Run app
app.mainloop()
