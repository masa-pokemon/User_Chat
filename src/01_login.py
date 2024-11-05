import streamlit as st
import pandas as pd

# 初期データ
if 'posts' not in st.session_state:
    st.session_state.posts = pd.DataFrame(columns=["ユーザー名", "交換希望カード", "ステータス"])

# ユーザー名と交換希望カードの入力フォーム
st.title("ポケモンカード交換掲示板")

# 投稿フォーム
with st.form(key='post_form'):
    username = st.text_input("あなたの名前", "")
    card_to_trade = st.text_input("交換希望カード", "")
    submit_button = st.form_submit_button(label="投稿")

    if submit_button:
        # 投稿内容を保存
        new_post = pd.DataFrame([[username, card_to_trade, "未交換"]],
                                columns=["ユーザー名", "交換希望カード", "ステータス"])
        st.session_state.posts = pd.concat([st.session_state.posts, new_post], ignore_index=True)
        st.success("投稿が完了しました!")

# 現在の掲示板の状態
st.subheader("現在の投稿一覧")

# 投稿された内容を表示
if not st.session_state.posts.empty:
    for i, row in st.session_state.posts.iterrows():
        with st.expander(f"{row['ユーザー名']} さんの交換希望カード"):
            st.write(f"交換希望カード: {row['交換希望カード']}")
            st.write(f"状態: {row['ステータス']}")
            
            # 交換済みにするボタン
            if st.button(f"交換完了 - {row['ユーザー名']}", key=f"btn_{i}"):
                st.session_state.posts.at[i, 'ステータス'] = "交換済み"
                st.experimental_rerun()  # 再描画して更新された状態を反映
else:
    st.write("現在投稿はありません。")
