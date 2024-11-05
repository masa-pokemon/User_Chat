import streamlit as st
import pandas as pd

# 初期データの読み込み（データがない場合は空のDataFrameを作成）
if 'posts' not in st.session_state:
    st.session_state.posts = pd.DataFrame(columns=["ユーザー名", "交換したいカード", "提供できるカード", "メッセージ"])

# サイドバーに投稿フォームを作成
st.sidebar.title("ポケモンカード交換掲示板")

# ユーザー名
username = st.sidebar.text_input("ユーザー名", "")

# 交換したいカード
wanted_card = st.sidebar.text_input("交換したいカード", "")

# 提供できるカード
offered_card = st.sidebar.text_input("提供できるカード", "")

# メッセージ
message = st.sidebar.text_area("メッセージ", "")

# 投稿ボタン
if st.sidebar.button("投稿する"):
    if username and wanted_card and offered_card:
        # 新しい投稿をDataFrameに追加
        new_post = {
            "ユーザー名": username,
            "交換したいカード": wanted_card,
            "提供できるカード": offered_card,
            "メッセージ": message
        }
        st.session_state.posts = st.session_state.posts.append(new_post, ignore_index=True)
        st.success("投稿が成功しました！")
    else:
        st.error("ユーザー名、交換したいカード、提供できるカードをすべて入力してください。")

# メインエリアに掲示板の投稿を表示
st.title("ポケモンカード交換掲示板")

if len(st.session_state.posts) > 0:
    # 投稿がある場合
    for idx, post in st.session_state.posts.iterrows():
        st.subheader(f"投稿者: {post['ユーザー名']}")
        st.write(f"**交換したいカード**: {post['交換したいカード']}")
        st.write(f"**提供できるカード**: {post['提供できるカード']}")
        if post['メッセージ']:
            st.write(f"**メッセージ**: {post['メッセージ']}")
        st.write("---")
else:
    st.write("現在、投稿はありません。")
