import streamlit as st
from const import get_trade_posts, add_trade_post

# タイトルとヘッダー
st.title("ポケモンカード トレード掲示板")
st.header("カードのトレードを予約しましょう！")

# トレードの投稿フォーム
st.subheader("新しいトレード投稿")
with st.form(key="trade_form"):
    title = st.text_input("カード名")
    description = st.text_area("カードの説明")
    user_name = st.text_input("あなたの名前")
    get_card = st.text_input("欲しいカード")
    submit_button = st.form_submit_button("投稿")

    if submit_button:
        if title and description and user_name and get_card:
            add_trade_post(title, description, user_name, get_card)
            st.success("投稿が成功しました！")
        else:
            st.error("すべてのフィールドを入力してください。")

# 投稿一覧を表示
st.subheader("トレード掲示板")
trade_posts = get_trade_posts()

if trade_posts:
    for post in trade_posts:
        st.write(f"**{post['title']}**")
        st.write(f"説明: {post['description']}")
        st.write(f"投稿者: {post['user_name']}")
        st.write(f"欲しいカード: {post['get_card']}")
        st.write("---")
else:
    st.write("まだ投稿はありません。")
