import streamlit as st
from diffusers import StableDiffusionPipeline
import torch

# Stable Diffusionのパイプラインのロード（GPUを使用する場合）
pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4-original", torch_dtype=torch.float32)
pipe.to("cuda")

def generate_image(prompt):
    image = pipe(prompt).images[0]
    return image

st.title("Stable Diffusion 画像生成アプリ")

prompt = st.text_area("画像を生成するプロンプトを入力してください")

if prompt:
    image = generate_image(prompt)
    st.image(image, caption="生成された画像", use_column_width=True)
