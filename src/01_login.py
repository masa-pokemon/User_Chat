from diffusers import StableDiffusionPipeline
import torch

# Stable Diffusionモデルの読み込み
model_id = "CompVis/stable-diffusion-v1-4-original"
pipe = StableDiffusionPipeline.from_pretrained(model_id)
pipe.to("cuda")  # GPUがある場合はGPUを使用

import streamlit as st
from PIL import Image

# Streamlitのページ設定
st.set_page_config(page_title="画像生成AI", page_icon="🎨", layout="centered")

# タイトル
st.title("画像生成AI - テキストから画像を生成")

# プロンプト入力フォーム
prompt = st.text_input("画像を生成するためのテキストを入力してください:", "")

# 画像生成ボタン
if st.button("画像生成"):
    if prompt:
        with st.spinner("画像を生成中..."):
            # プロンプトに基づいて画像を生成
            image = pipe(prompt).images[0]
            
            # 生成した画像を表示
            st.image(image, caption="生成された画像", use_column_width=True)
    else:
        st.error("プロンプトを入力してください。")
