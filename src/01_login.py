import streamlit as st
from PIL import Image
from diffusers import StableDiffusionPipeline
import torch

# モデルのロード（Stable Diffusion v2）
@st.cache_resource
def load_model():
    model = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1-base", torch_dtype=torch.float16)
    model.to("cuda")  # GPUを使用する場合
    return model

# StreamlitのUI設定
st.title("画像生成AI with Stable Diffusion")
st.write("プロンプトを入力して画像を生成してください。")

# ユーザーからの入力
prompt = st.text_input("画像生成プロンプト", "a futuristic city skyline at sunset")

# モデルの読み込み
model = load_model()

# 画像生成ボタン
if st.button("生成する"):
    with st.spinner("画像生成中..."):
        # プロンプトを使用して画像を生成
        image = model(prompt).images[0]
        
        # 生成した画像をStreamlitで表示
        st.image(image, caption="生成された画像", use_column_width=True)
