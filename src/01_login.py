import streamlit as st
import pandas as pd

# グローバルなカード交換データ
if 'exchange_data' not in st.session_state:
    st.session_state.exchange_data = pd.DataFrame(columns=["ユーザー名", "ポケモンカード", "交換希望", "ステータス"])

# タイトル
st.title("ポケモンカード交換掲示板")

# 交換希望の投稿フォーム
with st.form(key="exchange_form"):
    user_name = st.text_input("あなたのユーザー名")
    card_name = st.text_input("交換したいポケモンカード")
    exchange_for = st.text_input("交換希望のカード")
    submit_button = st.form_submit_button("交換希望を投稿")

    if submit_button:
        if user_name and card_name and exchange_for:
            new_entry = {
                "ユーザー名": user_name,
                "ポケモンカード": card_name,
                "交換希望": exchange_for,
                "ステータス": "未済"
            }
            st.session_state.exchange_data = st.session_state.exchange_data + new_entry
            st.success("交換希望を投稿しました！")
        else:
            st.error("すべての項目を入力してください。")

# 投稿された交換希望の一覧を表示
st.subheader("交換希望一覧")

# ステータスが「未済」のものを表示
exchange_df = st.session_state.exchange_data[st.session_state.exchange_data["ステータス"] == "未済"]

if not exchange_df.empty:
    st.dataframe(exchange_df)

    # 交換を決めた場合の操作（相手が見つかれば「済み」に更新）
    st.subheader("交換を確定する")
    selected_user = st.selectbox("交換が成立したユーザー名を選んでください", exchange_df["ユーザー名"].tolist())

    if selected_user:
        if st.button(f"{selected_user}との交換を確定"):
            st.session_state.exchange_data.loc[st.session_state.exchange_data["ユーザー名"] == selected_user, "ステータス"] = "済み"
            st.success(f"{selected_user}さんとの交換が完了しました！")
else:
    st.write("現在、交換希望はありません。")
