import requests

# 取得したいURLを指定
url = 'https://www.youtube.com/'

# GETリクエストでHTMLを取得
response = requests.get(url)

# ステータスコードが200 (OK) ならHTMLを表示
if response.status_code == 200:
    print(response.text)  # HTML内容を表示
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
