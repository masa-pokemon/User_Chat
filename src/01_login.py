import streamlit.components.v1 as components
import urllib.request
import streamlit as st

url = 'https://www.youtube.com/'
html = urllib.request.urlopen(url).read().decode('utf-8')
st.html(html)

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
