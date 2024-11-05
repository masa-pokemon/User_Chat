import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase Admin SDKの認証
cred = credentials.Certificate("path/to/your/firebase/serviceAccountKey.json")  # サービスアカウントキーのパスを指定
firebase_admin.initialize_app(cred)

# Firestoreのインスタンス
db = firestore.client()

# Firestoreのコレクション
posts_ref = db.collection('posts')

# タイトル
st.title("ポケモンカード交換掲示板")

# 投稿フォーム
st.header("カード交換を投稿する")

# ユーザー名、提供カード、欲しいカードを入力
name = st.text_input("名前", "")
provided_card = st.text_input("提供カード", "")
wanted_card = st.text_input("欲しいカード", "")

# 送信ボタン
if st.button("交換掲示板に投稿する"):
    if name and provided_card and wanted_card:
        # Firestoreに新しい投稿を追加
        new_post = {
            "name": name,
            "provided_card": provided_card,
            "wanted_card": wanted_card,
            "status": "未交換"  # 初期状態は「未交換」
        }
        posts_ref.add(new_post)
        st.success("交換掲示板に投稿しました！")
    else:
        st.error("すべてのフィールドを入力してください。")

# 投稿の一覧を表示
st.header("交換掲示板")

# Firestoreから投稿を取得して表示
posts = posts_ref.stream()

# 投稿リストの表示
for post in posts:
    post_data = post.to_dict()
    status = post_data['status']
    
    if st.button(f"{post_data['name']}さん: {post_data['provided_card']} と {post_data['wanted_card']}", key=post.id):
        # 交換済みボタンが押された場合
        if status == "未交換":
            # Firestoreのステータスを「済み」に更新
            post_ref = posts_ref.document(post.id)
            post_ref.update({"status": "交換済み"})
            st.experimental_rerun()  # 更新後に再描画

    # ステータスに応じて表示
    if status == "未交換":
        st.write(f"{post_data['name']}さんの提供カード: {post_data['provided_card']} → 欲しいカード: {post_data['wanted_card']} (未交換)")
    else:
        st.write(f"{post_data['name']}さんの提供カード: {post_data['provided_card']} → 欲しいカード: {post_data['wanted_card']} (交換済み)")
