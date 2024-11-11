import streamlit as st
from diffusers import StableDiffusionPipeline
import torch

# モデルのロード
@st.cache_resource
def load_model():
    # Stable Diffusionのパイプラインをロード（Hugging FaceのAPIキーが必要）
    model = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4-original", 
                                                    torch_dtype=torch.float16)
    model.to("cuda")  # GPUを使う
    return model

# 画像生成関数
def generate_image(prompt):
    model = load_model()
    image = model(prompt).images[0]
    return image

# StreamlitのUI
st.title("画像生成AI")
st.write("プロンプトを入力してください:")

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
