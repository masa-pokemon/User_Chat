import streamlit as st
import yt_dlp

#最高の画質と音質を動画をダウンロードする
ydl_opts = {
    'format': 'best',
    'outtmpl':'video.%(ext)s',
}
text = st.text_input("URL：")
if text:
    #動画のURLを指定
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(text)

        video_file = open("video.mp4", "rb")
        video_bytes = video_file.read()

        st.video(video_bytes)
