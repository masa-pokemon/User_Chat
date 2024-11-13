import streamlit as st
import yt_dlp
ydl_opts = {'format': 'best','outtmpl':'video.%(ext)s',}
text = st.text_input("URL：")
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
