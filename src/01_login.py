import streamlit as st
import yt_dlp
ydl_opts = {'format': 'best','outtmpl':'video.%(ext)s',}
text = st.text_input("youtube")
text1 = ""
if text != text1:
    import os
    if os.path.isfile('video.mp4'):
        os.remove('video.mp4')
    text1 = text
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(text)
        video_file = open("video.mp4", "rb")
        video_bytes = video_file.read()
        st.video(video_bytes)

import niconico_dl
text2 = st.text_input("niconico")
# Normal
def start():
    text2
    link = niconico_dl.NicoNicoVideoAsync.get_download_link()
    print(link)
    st.video(link)

if text2 != text1:
    start()
