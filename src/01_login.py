import streamlit as st
import requests
from bs4 import BeautifulSoup
import streamlit.components.v1 as stc
# Webページを取得して解析する

load_url = "https://www.ymori.com/books/python2nen/test1.html"
html = requests.get(load_url)
soup = BeautifulSoup(html.content, "html.parser")
st.components.v1.html(soup)
