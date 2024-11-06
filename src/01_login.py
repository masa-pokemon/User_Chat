import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Firebaseの認証設定
cred = credentials.Certificate("src/seat-change-optimization-firebase-adminsdk-bjgkk-481de3bcde.json")  # Firebase秘密鍵のパス
firebase_admin.initialize_app(cred)

# Firestoreクライアントの初期化
db = firestore.client()

# トレード予約のフォーム
def create_trade_post():
    st.title('ポケモンカード トレード掲示板')

    st.subheader('トレード予約の投稿')
    card_name = st.text_input("カード名")
    trade_type = st.selectbox("交換希望", ["カードを渡したい", "カードを受け取りたい"])
    user_name = st.text_input("ユーザー名")
    trade_date = st.date_input("希望交換日")
    description = st.text_area("その他の情報")

    if st.button('予約を投稿'):
        if card_name and trade_type and user_name and description:
            # Firestoreに投稿を保存
            post_ref = db.collection('trade_posts').add({
                'card_name': card_name,
                'trade_type': trade_type,
                'user_name': user_name,
                'trade_date': trade_date.strftime("%Y-%m-%d"),
                'description': description,
                'created_at': firestore.SERVER_TIMESTAMP
            })
            st.success("トレード予約が投稿されました！")
        else:
            st.error("すべてのフィールドを入力してください。")

# トレード予約の掲示板表示
def display_trade_posts():
    st.subheader('最新のトレード予約')
    trade_posts_ref = db.collection('trade_posts').order_by('created_at', direction=firestore.Query.DESCENDING).limit(10)
    posts = trade_posts_ref.stream()

    for post in posts:
        data = post.to_dict()
        st.write(f"**カード名**: {data['card_name']}")
        st.write(f"**交換希望**: {data['trade_type']}")
        st.write(f"**ユーザー名**: {data['user_name']}")
        st.write(f"**希望交換日**: {data['trade_date']}")
        st.write(f"**説明**: {data['description']}")
        st.markdown("---")

# アプリの実行
def main():
    st.sidebar.title("ポケモンカード トレード掲示板")
    selection = st.sidebar.radio("メニュー", ["トレード予約投稿", "掲示板を見る"])

    if selection == "トレード予約投稿":
        create_trade_post()
    elif selection == "掲示板を見る":
        display_trade_posts()

if __name__ == "__main__":
    main()
