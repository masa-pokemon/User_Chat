import streamlit as st
from diffusers import StableDiffusionPipeline
import torch

# モデルのロード
st.title("画像生成AI - Stable Diffusion")
st.write("このツールを使って、テキストから画像を生成できます。")

# モデルとデバイスの設定
device = "cuda" if torch.cuda.is_available() else "cpu"
st.write(f"使用するデバイス: {device}")

# Stable Diffusionパイプラインの読み込み
@st.cache_resource
def load_model():
    return StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v-1-4-original", torch_dtype=torch.float32).to(device)

model = load_model()

# ユーザーから入力を受け取る
prompt = st.text_input("画像の内容を入力してください:", "A beautiful landscape with mountains and a sunset")

# 画像生成ボタン
if st.button("画像を生成"):
    with st.spinner("画像を生成しています..."):
        # 画像生成
        generated_image = model(prompt).images[0]

        # 生成した画像を表示
        st.image(generated_image, caption="生成された画像", use_column_width=True)
