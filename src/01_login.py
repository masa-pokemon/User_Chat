import requests
from bs4 import BeautifulSoup
import urllib.request 
import csv
import re
import streamlit as st

def fetch_html(url: str) -> str:
    with urllib.request.urlopen(url) as res:
        html = res.read().decode()
    return html

st.html(fetch_html('https://www.youtube.com/'))
