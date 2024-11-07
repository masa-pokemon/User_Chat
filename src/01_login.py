import streamlit as st
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image

# Stable Diffusionパイプラインの初期化
@st.cache_resource
def load_model():
    model = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4-original", torch_dtype=torch.float16)
    model.to("cuda")
    return model

# モデルの読み込み
model = load_model()

# StreamlitのUIを作成
st.title("Stable Diffusion 画像生成")
st.write("テキストを入力して画像を生成しましょう！")

# ユーザーからのテキスト入力を取得
prompt = st.text_input("生成したい画像の説明を入力してください:")

if prompt:
    # 画像生成
    with st.spinner("画像生成中..."):
        image = model(prompt).images[0]

    # 生成した画像を表示
    st.image(image, caption="生成された画像", use_column_width=True)

