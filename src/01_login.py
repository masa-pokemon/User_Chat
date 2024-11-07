import streamlit as st
from audio_recorder_streamlit import audio_recorder

if st.button("録音スタート")audio_bytes = audio_recorder()

if st.button("録音保存"):
    with open("recorded_audio.wav", "wb") as f:
        f.write(audio_bytes)
    st.success("Recording saved!")
