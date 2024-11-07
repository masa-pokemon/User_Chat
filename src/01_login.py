import streamlit as st
from diffusers import StableDiffusionPipeline
import torch

# Stable Diffusionのパイプラインをロード
@st.cache_resource
def load_model():
    model = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4-original", torch_dtype=torch.float16)
    model.to("cuda")  # GPUを使用する場合
    return model

model = load_model()

# Streamlit アプリケーション
st.title("画像生成AI")

st.write("テキストを入力してください、画像を生成します。")

# テキストの入力
prompt = st.text_input("生成したい画像の説明を入力してください:")

# 生成ボタンが押された場合
if st.button("画像生成"):
    if prompt:
        with st.spinner("画像を生成中..."):
            # 画像生成
            image = model(prompt).images[0]
            
            # 生成された画像を表示
            st.image(image, caption="生成された画像", use_column_width=True)
    else:
        st.error("説明文を入力してください。")
