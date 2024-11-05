import streamlit as st
import pandas as pd

# 初期データの設定（実際のデータはDBに保存することも可能ですが、今回は簡易的にデータフレームを使います）
if 'posts' not in st.session_state:
    st.session_state['posts'] = pd.DataFrame(columns=["名前", "提供カード", "欲しいカード", "ステータス"])

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
        # 投稿内容をデータフレームに追加
        new_post = pd.DataFrame([[name, provided_card, wanted_card, "未交換"]], columns=["名前", "提供カード", "欲しいカード", "ステータス"])
        st.session_state['posts'] = pd.concat([st.session_state['posts'], new_post], ignore_index=True)
        st.success("交換掲示板に投稿しました！")
    else:
        st.error("すべてのフィールドを入力してください。")

# 投稿の一覧を表示
st.header("交換掲示板")

# 交換済みのユーザーは「済み」と表示
for i, row in st.session_state['posts'].iterrows():
    status = row['ステータス']
    if st.button(f"{row['名前']}さん: {row['提供カード']} と {row['欲しいカード']}", key=f"btn_{i}"):
        if status == "未交換":
            st.session_state['posts'].at[i, 'ステータス'] = "済み"
            st.experimental_rerun()  # 更新後に再描画

    # ステータス表示
    if status == "未交換":
        st.write(f"{row['名前']}さんの提供カード: {row['提供カード']} → 欲しいカード: {row['欲しいカード']} (未交換)")
    else:
        st.write(f"{row['名前']}さんの提供カード: {row['提供カード']} → 欲しいカード: {row['欲しいカード']} (交換済み)")

