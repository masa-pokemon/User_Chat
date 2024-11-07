import streamlit as st
from PIL import Image
from diffusers import StableDiffusionPipeline
import torch

# モデルのロード
@st.cache_resource
def load_model():
    pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v-1-4-original", torch_dtype=torch.float16)
    pipe.to("cuda")
    return pipe

# モデルのロード
pipe = load_model()

# アプリのタイトル
st.title("AI画像生成器")

# ユーザーからのテキスト入力
prompt = st.text_input("生成したい画像の説明を入力してください:")

# 画像生成ボタン
if st.button("画像を生成"):
    if prompt:
        with st.spinner("画像を生成中..."):
            # 画像を生成
            image = pipe(prompt).images[0]
            
            # 生成された画像を表示
            st.image(image, caption="生成された画像", use_column_width=True)
    else:
        st.warning("画像生成のために、プロンプトを入力してください。")
