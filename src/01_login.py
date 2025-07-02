import streamlit as st
from yt_dlp import YoutubeDL
import os

def download_video(url, output_path="./downloads"):
    """
    指定されたURLからYouTube動画をダウンロードします。
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ydl_opts = {
        'format': 'best',  # 最適な品質をダウンロード
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # ファイル名フォーマット
        'noplaylist': True,  # プレイリストはダウンロードしない
        'progress_hooks': [lambda d: st.info(f"ダウンロード状況: {d['status']}")] # ダウンロード状況を表示
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=True)
            st.success(f"ダウンロード完了: {info_dict['title']}")
            return True
        except Exception as e:
            st.error(f"ダウンロード中にエラーが発生しました: {e}")
            return False

st.title("YouTube動画ダウンローダー")

youtube_url = st.text_input("YouTube動画のURLを入力してください:", "")

if st.button("ダウンロード"):
    if youtube_url:
        st.info("ダウンロードを開始します...")
        download_video(youtube_url)
    else:
        st.warning("URLを入力してください。")

st.subheader("ダウンロード済みファイル")
# ダウンロードディレクトリが存在しない場合は作成
if not os.path.exists("./downloads"):
    os.makedirs("./downloads")

# ダウンロードディレクトリ内のファイルを表示
downloaded_files = [f for f in os.listdir("./downloads") if os.path.isfile(os.path.join("./downloads", f))]

if downloaded_files:
    for file_name in downloaded_files:
        file_path = os.path.join("./downloads", file_name)
        with open(file_path, "rb") as f:
            st.download_button(
                label=f"ダウンロード: {file_name}",
                data=f.read(),
                file_name=file_name,
                mime="application/octet-stream"
            )
else:
    st.info("まだダウンロードされたファイルはありません。")
