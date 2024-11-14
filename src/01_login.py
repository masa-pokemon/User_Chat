import streamlit as st
import urllib.request

def fetch_html(url: str) -> str:
    with urllib.request.urlopen(url) as res:
        html = res.read().decode()
    return html

st.markdown(fetch_html('https://www.google.co.jp/'),unsafe_allow_html=True)
