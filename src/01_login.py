import streamlit as st
from PIL import Image
import torch
from transformers import pipeline

# 画像生成モデルの初期化（例：Stable Diffusion）
generator = pipeline('image-generation', model='CompVis/stable-diffusion-v1-4')

# Streamlitのタイトル
st.title("画像生成AI")

# テキスト入力
prompt = st.text_input("生成したい画像の説明を入力してください:")

# 画像生成ボタン
if st.button("画像生成"):
    if prompt:
        with st.spinner("画像を生成中..."):
            # 画像生成
            images = generator(prompt, num_return_sequences=1)
            generated_image = images[0]['image']

            # 画像を表示
            st.image(generated_image, caption="生成された画像", use_column_width=True)
    else:
        st.warning("画像の説明を入力してください。")
