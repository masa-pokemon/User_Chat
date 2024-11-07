import streamlit as st
import time
import io
from pydub import AudioSegment
from io import BytesIO

# 音声録音用のJavaScriptコードを実行
def audio_recorder():
    # JavaScriptコードを使ってブラウザで音声録音を行う
    st.markdown(
        """
        <script>
        let audioBlob = null;
        let recorder;
        let audioChunks = [];

        const startRecording = async () => {
            audioChunks = [];
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            recorder = new MediaRecorder(stream);
            recorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };
            recorder.onstop = () => {
                audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const audioUrl = URL.createObjectURL(audioBlob);
                const audio = new Audio(audioUrl);
                audio.controls = true;
                document.getElementById('audioPlayer').src = audioUrl;
                document.getElementById('audioPlayer').style.display = 'block';
            };
            recorder.start();
        };

        const stopRecording = () => {
            recorder.stop();
        };
        </script>
        """,
        unsafe_allow_html=True
    )

    # 録音開始ボタン
    start_button = st.button("録音開始")
    if start_button:
        st.markdown('<script>startRecording();</script>', unsafe_allow_html=True)
    
    # 録音停止ボタン
    stop_button = st.button("録音停止")
    if stop_button:
        st.markdown('<script>stopRecording();</script>', unsafe_allow_html=True)
    
    # 録音した音声を表示
    st.markdown('<audio id="audioPlayer" style="display:none;" controls></audio>', unsafe_allow_html=True)

    # 音声ファイルを保存する処理（録音後）
    if stop_button:
        time.sleep(2)  # 少し待ってから処理を開始
        st.audio("audio.wav", format="audio/wav")

audio_recorder()
