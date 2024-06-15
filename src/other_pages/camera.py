import streamlit as st  # Streamlitライブラリをインポート
import edge_tts  # Edge TTSライブラリをインポート
import os  # OSライブラリをインポート（ファイル操作用）
import asyncio  # 非同期処理を行うためのライブラリ
import speech_recognition as sr  # 音声認識のためのライブラリ

# Streamlitウェブアプリのタイトルを設定
st.title('音声作成アプリ')

# 音声認識を行う関数の定義
def recognize_speech():
    r = sr.Recognizer()  # 音声認識器のインスタンスを作成
    mic = sr.Microphone()  # マイクロフォンのインスタンスを作成
    with mic as source:  # マイクロフォンを音声入力ソースとして使用
        audio = r.listen(source)  # 音声を聞いて、オーディオデータを取得
        try:
            # Googleの音声認識サービスを使用して日本語のテキストに変換
            return r.recognize_google(audio, language="ja-JP")
        except sr.UnknownValueError:
            # 音声が認識できなかった場合
            return ""
        except sr.RequestError:
            # 音声認識サービスへのリクエストに失敗した場合
            return ""

# 音声認識を実行するボタンを追加
if st.button('Record Speech'):
    recognized_text = recognize_speech()  # 音声認識関数を呼び出し、結果を取得
else:
    # セッション状態から以前の認識テキストを取得
    recognized_text = st.session_state.get('recognized_text', "")

# テキスト入力フィールドを追加。認識されたテキストをデフォルト値として設定
text = st.text_area('Text', recognized_text)

# 音声の声質を選択するためのドロップダウンメニューを追加
voice = st.selectbox(
    'Voice', 
    ['ja-JP-KeitaNeural', 'ja-JP-NanamiNeural', 'en-US-JessaNeural', 
     'zh-CN-XiaoxiaoNeural', 'zh-CN-YunyangNeural', 'ko-KR-SunHiNeural']
)

# 音声の速度を調整するためのスライダーを追加
rate = st.slider('Rate', -100, 100, 20)

# 音声のピッチを調整するためのスライダーを追加
pitch = st.slider('Pitch', -100, 100, 0)

# 音声ファイルの出力名を設定
output_file = 'output.mp3'

# 音声生成を実行するボタンを追加
if st.button('Generate Speech'):
    rate_str = f"{rate:+}%"  # 速度の設定を文字列に変換
    pitch_str = f"{pitch:+}Hz"  # ピッチの設定を文字列に変換
    # 音声合成の設定を行い、ファイルに保存
    communicate = edge_tts.Communicate(text, voice, rate=rate_str, pitch=pitch_str)
    asyncio.run(communicate.save(output_file))
    # 生成された音声をウェブアプリ上で再生
    st.audio(output_file)

# 音声ファイルが存在する場合、削除ボタンを追加
if os.path.exists(output_file):
    if st.button('Delete File'):
        os.remove(output_file)  # ファイルを削除

# 認識されたテキストをセッション状態に保存
st.session_state['recognized_text'] = recognized_text
