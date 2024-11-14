import streamlit as st
import urllib.request

def fetch_html(url: str) -> str:
    with urllib.request.urlopen(url) as res:
        html = res.read().decode()
    return html

html = fetch_html('https://www.youtube.com/')
st.markdown(html,unsafe_allow_html=True)
