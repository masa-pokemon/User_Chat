import streamlit as st
from diffusers import StableDiffusionPipeline
import torch

# モデルをキャッシュしてロード
@st.cache_resource
def load_model():
    # Hugging FaceのStable Diffusionモデルをロード
    model = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4-original")
    model.to("cuda" if torch.cuda.is_available() else "cpu")
    return model

# 画像生成関数
def generate_image(prompt):
    model = load_model()
    image = model(prompt).images[0]
    return image

# StreamlitのUI
st.title("Stable Diffusion 画像生成")
st.write("生成したい画像のプロンプトを入力してください:")

# ユーザーからプロンプトを取得
prompt = st.text_input("プロンプト")

if st.button("画像を生成"):
    if prompt:
        # 画像生成
        with st.spinner("生成中..."):
            image = generate_image(prompt)
            st.image(image, caption="生成された画像", use_column_width=True)
    else:
        st.error("プロンプトを入力してください！")
