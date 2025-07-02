import streamlit as st
import yt_dlp
import os
import shutil # ファイル操作のためにインポート

def download_youtube_video(url, download_path):
    """
    指定されたURLのYouTube動画をダウンロードします。
    ダウンロードパスは一時的な場所を使用し、ダウンロード後にStreamlitで表示します。
    """
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', 'Unknown Title')
            video_ext = info_dict.get('ext', 'mp4') # 確実な拡張子を取得
            
            # yt-dlpが実際に保存したファイルパスを特定する
            # info_dict['requested_downloads'][0]['filepath'] などで取得できる場合もあるが、
            # シンプルにouttmplのパターンとinfo_dictのタイトル・拡張子から推測
            downloaded_file_path = os.path.join(download_path, f"{video_title}.{video_ext}")
            
            # ダウンロードが完了しているか最終確認
            if not os.path.exists(downloaded_file_path):
                # マージなどでファイル名が変わる可能性を考慮し、ダウンロードディレクトリをスキャン
                # これは一般的な対処法ですが、yt-dlpの出力から正確なパスを得るのが理想です。
                # 例: ダウンロードされた最初のmp4ファイルを探す
                found_files = [f for f in os.listdir(download_path) if f.startswith(video_title) and f.endswith('.mp4')]
                if found_files:
                    downloaded_file_path = os.path.join(download_path, found_files[0])
                else:
                    raise FileNotFoundError("ダウンロードされた動画ファイルが見つかりませんでした。")
            
            st.success(f"ダウンロードが完了しました: **{video_title}.mp4**")
            return downloaded_file_path

    except yt_dlp.DownloadError as e:
        st.error(f"ダウンロードエラーが発生しました: {e}")
        return None
    except FileNotFoundError as e:
        st.error(f"ファイルシステムエラー: {e}")
        return None
    except Exception as e:
        st.error(f"予期せぬエラーが発生しました: {e}")
        return None

def main():
    st.set_page_config(page_title="YouTube動画ダウンローダー", layout="centered")
    st.title("📺 YouTube動画ダウンローダー")
    st.markdown("""
    このアプリは、YouTubeの動画を簡単にダウンロードし、プレビューできます。
    動画のURLを入力して「ダウンロード」ボタンを押してください。
    """)

    video_url = st.text_input("YouTube動画のURLを入力してください:", key="url_input")

    # 一時的なダウンロードディレクトリを作成
    temp_download_dir = "./temp_downloads"
    os.makedirs(temp_download_dir, exist_ok=True)

    if st.button("ダウンロード", key="download_button") and video_url:
        with st.spinner("動画情報を取得し、ダウンロードしています... しばらくお待ちください。"):
            downloaded_file = download_youtube_video(video_url, temp_download_dir)
            
            if downloaded_file and os.path.exists(downloaded_file):
                # ダウンロードした動画をStreamlitのdownloadボタンで提供
                st.markdown("---")
                st.subheader("ダウンロードされた動画")
                
                # ファイル名からタイトルを推測（拡張子を除去）
                file_name_with_ext = os.path.basename(downloaded_file)
                file_name_without_ext, file_ext = os.path.splitext(file_name_with_ext)
                
                # ここで st.video を使って動画をプレビュー表示します
                st.video(downloaded_file)
                
                with open(downloaded_file, "rb") as file:
                    st.download_button(
                        label=f"「{file_name_without_ext}.{file_ext[1:]}」をダウンロード", # .を削除
                        data=file,
                        file_name=file_name_with_ext,
                        mime=f"video/{file_ext[1:]}"
                    )
                
                st.info("ダウンロードが完了しました。上記でプレビューを確認し、ボタンからファイルを保存してください。")
            elif downloaded_file: # ダウンロード処理は成功したがファイルが見つからない場合
                st.error("動画はダウンロードされましたが、ファイルが見つかりませんでした。")
            
    st.markdown("---")
    st.markdown("開発者: あなたの名前/GitHubリンクなど")

if __name__ == "__main__":
    main()

    # アプリケーションが終了する際に一時ファイルをクリーンアップするロジック（オプション）
    # Streamlitの性質上、セッションごとの起動なので、確実なクリーンアップは難しいです。
    # ここでは、アプリが再起動した際に前回の残骸があれば削除する程度の意味合いです。
    temp_download_dir_for_cleanup = "./temp_downloads"
    if os.path.exists(temp_download_dir_for_cleanup):
        try:
            # shutil.rmtree(temp_download_dir_for_cleanup)
            # print(f"Temporary directory '{temp_download_dir_for_cleanup}' cleaned up.")
            pass # Streamlitの実行中は削除しない方が良い場合が多い
        except OSError as e:
            print(f"Error removing temporary directory: {e}")
