import requests
import streamlit as st

# 取得したいURLを指定
url = 'https://www.youtube.com/'

# GETリクエストでHTMLを取得
response = requests.get(url)

# ステータスコードが200 (OK) ならHTMLを表示
if response.status_code == 200:
    st.html(response.text)  # HTML内容を表示
else:
    st.html(f"Failed to retrieve the page. Status code: {response.status_code}")
