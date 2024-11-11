import streamlit as st
from PIL import Image
from diffusers import StableDiffusionPipeline
import torch

# Stable Diffusionのモデルをロード
@st.cache_resource
def load_model():
    model = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2", torch_dtype=torch.float16)
    return model

# モデルを読み込む
pipe = load_model()

# Streamlitのページ設定
st.set_page_config(page_title="画像生成AI", page_icon="🖼️", layout="centered")

# アプリのタイトル
st.title("テキストから画像を生成するAI")

# プロンプト入力フォーム
prompt = st.text_input("画像を生成するためのテキストを入力してください:", "")

# 画像生成ボタン
if st.button("画像を生成"):
    if prompt:
        with st.spinner("画像を生成中..."):
            # プロンプトを使って画像を生成
            image = pipe(prompt).images[0]
            
            # 生成された画像を表示
            st.image(image, caption="生成された画像", use_column_width=True)
    else:
        st.error("プロンプトを入力してください。")
