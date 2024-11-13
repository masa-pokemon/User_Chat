import urllib.request 
import streamlit as st

def fetch_html(url: str) -> str:
    with urllib.request.urlopen(url) as res:
        html = res.read().decode()
    return html

st.html(fetch_html('https://www.youtube.com/'))
