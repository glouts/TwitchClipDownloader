import tkinter as tk
from tkinter import filedialog
import requests
import urllib.request


PATH = "./"


def downloadClip():
    url = textInput.get("1.0","end")
    url = url.split("\n")

    CLIENT_SECRET = "" # Paste here your client_secret from your twitch app
    CLIENT_ID = "" # Paste here your client_id from your twitch app


    OAUTH_TOKEN = requests.post("https://id.twitch.tv/oauth2/token?client_id="+ CLIENT_ID +"&client_secret="+ CLIENT_SECRET +"&grant_type=client_credentials").json()
    OAUTH_TOKEN = "Bearer " + str(OAUTH_TOKEN["access_token"])


    HEADERS = {"Client-ID": CLIENT_ID, "Authorization": OAUTH_TOKEN}


    for i in range(len(url)):
        if(url[i] != ""):
            clipId = url[i].split("clip/", -1)[1]
            clipId = clipId.split("?", 1)[0]
            r = requests.get("https://api.twitch.tv/helix/clips?id="+ clipId, headers = HEADERS).json()
            
            for items in r['data']:
                clipTitle = items['title']
                downloadUrl = items['thumbnail_url']
                
            if(downloadUrl):
                finalUrl = downloadUrl.split("-preview", 1)[0]
                finalUrl += ".mp4"
                
            else:
                print("Failed to get the download url")
                
            if(clipTitle):
                try:
                    clipTitle = removeSpecialChars(clipTitle)
                    print("Downloading " + clipTitle)
                    clipTitle += ".mp4"
                    urllib.request.urlretrieve(finalUrl, PATH + clipTitle)
                    print("Succesfully downloaded")

                except Exception as e:
                    print(e)

            else:
                print("Failed to get the clip title, assigning standard title and downloading...")
                urllib.request.urlretrieve(finalUrl, PATH + "download" + i + ".mp4")
                print("Downloaded")


def removeSpecialChars(string):
    string = string.replace(":", "")
    string = string.replace(";", "")
    string = string.replace("|", "")
    string = string.replace("?", "")
    string = string.replace(",", "")
    string = string.replace("*", "")
    string = string.replace('"', "")
    string = string.replace("/", "")
    string = string.replace("<", "")
    string = string.replace(">", "")
    string = string.replace("[", "")
    string = string.replace("]", "")

    return string


def pathSelector():
    global PATH
    PATH = filedialog.askdirectory()
    PATH += "/"
    

# Tkinter GUI

root = tk.Tk()
root.title("Twitch Clip Downloader - Glouts")
root.geometry("1280x720")
root.configure(background="#b380ff")


titleLabel = tk.Label(root,text="Twitch Clip Downloader",font="Times 32 bold" ,width=20,height=1,background="#b380ff")
titleLabel.pack()


helpLabel = tk.Label(root,text="Select path, paste your clips here and press download button",font="Times 14",width=50,height=3,background="#b380ff")
helpLabel.pack()


pathBtn = tk.Button(root,height=1,width=10, text="Select Path", background="#e0ccff", command=lambda:pathSelector())
pathBtn.pack()


spaceLabel = tk.Label(root,text="",height=1,background="#b380ff")
spaceLabel.pack()


textInput = tk.Text(root,height=30,background="#e0ccff")
textInput.pack()


spaceLabel = tk.Label(root,text="",height=1,background="#b380ff")
spaceLabel.pack()


btnRead = tk.Button(root,height=1,width=10, text="Download", background="#e0ccff", command=lambda:downloadClip())
btnRead.pack()


spaceLabel = tk.Label(root,text="https://github.com/glouts",font="Times 14",width=20,background="#b380ff")
spaceLabel.pack(side="right")


root.mainloop()
