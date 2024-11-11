import streamlit as st
import torch
from PIL import Image
from torchvision import transforms
from taming.models.vqgan import VQModel
from clip import clip
import numpy as np

# VQGANモデルのロード
@st.cache_resource
def load_vqgan_model():
    model = VQModel.from_pretrained('vqgan_imagenet_f16_1024')
    model.eval()
    return model

# CLIPモデルのロード
@st.cache_resource
def load_clip_model():
    model, preprocess = clip.load("ViT-B/32", device="cuda" if torch.cuda.is_available() else "cpu")
    return model, preprocess

# 画像生成関数
def generate_image(prompt, num_iterations=50, step_size=0.05):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # モデルのロード
    vqgan_model = load_vqgan_model().to(device)
    clip_model, preprocess = load_clip_model()

    # プロンプトのテキストをCLIPに渡して、テキスト特徴量を取得
    text = clip.tokenize([prompt]).to(device)
    text_features = clip_model.encode_text(text)

    # 初期ノイズを生成
    z = torch.randn((1, 256, 16, 16)).to(device)

    # 最適化の設定
    z.requires_grad = True
    optimizer = torch.optim.Adam([z], lr=step_size)

    for i in range(num_iterations):
        optimizer.zero_grad()

        # VQGANで画像を生成
        x = vqgan_model.decode(z)

        # 画像をCLIPに渡して、テキスト特徴量との類似度を計算
        image_features = clip_model.encode_image(preprocess(x).unsqueeze(0).to(device))
        loss = -torch.cosine_similarity(text_features, image_features).mean()

        # 誤差逆伝播と最適化
        loss.backward()
        optimizer.step()

        # 途中経過を表示
        if i % 10 == 0:
            st.write(f"Iteration {i}/{num_iterations} - Loss: {loss.item():.4f}")
            img = x[0].cpu().detach().clamp(0, 1).permute(1, 2, 0).numpy()
            img = (img * 255).astype(np.uint8)
            st.image(img, caption=f"Step {i}", use_column_width=True)

    # 最終的な画像を返す
    img = x[0].cpu().detach().clamp(0, 1).permute(1, 2, 0).numpy()
    img = (img * 255).astype(np.uint8)
    return Image.fromarray(img)

# StreamlitのUI
st.title("VQGAN + CLIPによる画像生成")
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
