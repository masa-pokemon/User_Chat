import streamlit as st
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import io

# モデルの読み込み (Stable Diffusion)
@st.cache_resource
def load_model():
    model = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4-original", 
                                                    torch_dtype=torch.float16)
    model.to("cuda")
    return model

# 画像生成関数
def generate_image(prompt):
    model = load_model()
    with torch.no_grad():
        image = model(prompt).images[0]
    return image

# Streamlit アプリのUI作成
st.title("画像生成AI")

# テキストボックスでプロンプトを入力
prompt = st.text_area("画像を生成するためのプロンプトを入力してください:")

if prompt:
    st.write(f"生成中: {prompt}")
    with st.spinner('画像を生成中...'):
        image = generate_image(prompt)
    
    # 生成した画像を表示
    st.image(image, caption="生成された画像", use_column_width=True)
