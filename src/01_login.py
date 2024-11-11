import streamlit as st
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image

# GPUが使用可能な場合はGPUを使う
device = "cuda" if torch.cuda.is_available() else "cpu"

# Stable Diffusion Pipelineの準備
@st.cache_resource
def load_model():
    model = StableDiffusionPipeline.from_pretrained("stable-diffusion-2-1", torch_dtype=torch.float16)
    model.to(device)
    return model

model = load_model()

# Streamlitアプリケーション
st.title("画像生成AI - Stable Diffusion")
st.write("テキストから画像を生成するAIアプリケーションです。")

# テキスト入力を受け取る
prompt = st.text_input("生成したい画像の説明を入力してください:")

if st.button("画像を生成"):
    if prompt:
        with st.spinner('画像を生成中...'):
            # テキストプロンプトを使って画像生成
            image = model(prompt).images[0]

            # 画像を表示
            st.image(image, caption="生成された画像", use_column_width=True)
    else:
        st.warning("画像を生成するためにはテキストを入力してください。")
