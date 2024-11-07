import streamlit as st
import random
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase初期化
if not firebase_admin._apps:
    cred = credentials.Certificate("src/seat-change-optimization-firebase-adminsdk-bjgkk-481de3bcde.json")  # Firebaseの認証情報
    firebase_admin.initialize_app(cred)

# Firestoreのインスタンス
db = firestore.client()

# 宝くじチケット購入処理
def buy_lottery_ticket(user_name, user_email):
    ticket_number = random.randint(100000, 999999)  # ランダムなチケット番号を生成
    ticket_data = {
        'user_name': user_name,
        'user_email': user_email,
        'ticket_number': ticket_number,
        'status': '未当選'  # 初期状態
    }

    # Firestoreにチケットデータを保存
    db.collection('lottery_tickets').add(ticket_data)

    return ticket_number

# 当選結果を更新
def update_ticket_status(ticket_number, status):
    ticket_ref = db.collection('lottery_tickets').where('ticket_number', '==', ticket_number).limit(1)
    ticket_docs = ticket_ref.stream()

    for ticket in ticket_docs:
        ticket_ref = db.collection('lottery_tickets').document(ticket.id)
        ticket_ref.update({
            'status': status
        })

# 当選判定
def check_lottery_result(ticket_number):
    # 例えば、固定の当選番号を決める（ここでは123456が当選）
    winning_number = 123456
    if ticket_number == winning_number:
        return '当選'
    else:
        return '外れ'

# StreamlitアプリのUI
st.title("宝くじアプリ")
st.write("宝くじのチケットを購入して、当選を確認しましょう！")

# ユーザー情報入力フォーム
with st.form(key='ticket_form'):
    user_name = st.text_input("名前")
    user_email = st.text_input("メールアドレス")
    submit_button = st.form_submit_button("チケットを購入")

if submit_button:
    if user_name and user_email:
        ticket_number = buy_lottery_ticket(user_name, user_email)
        st.write(f"購入が完了しました！あなたのチケット番号は {ticket_number} です。")
        
        # 当選確認ボタン
        if st.button("当選結果を確認"):
            result = check_lottery_result(ticket_number)
            update_ticket_status(ticket_number, result)
            st.write(f"あなたの結果は: {result}！")
    else:
        st.error("名前とメールアドレスを入力してください。")

# Firebase 初期化（すでに初期化されていない場合のみ実行）
