import streamlit as st

import requests # URLからHTMLを取得するための外部ライブラリ
page = requests.get("https://www.google.com/") # URLを指定してHTTPレスポンスを取得
print(page)

st.html(page)
