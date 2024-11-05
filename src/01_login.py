import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Firebaseの初期化
cred = credentials.Certificate("path/to/firebase_credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Firestoreにカード交換データを追加
def add_card_trade(user_name, card_name, wants_card):
    trades_ref = db.collection("trades")
    trade_data = {
        "user_name": user_name,
        "card_name": card_name,
        "wants_card": wants_card,
        "status": "交換希望中"
    }
    trades_ref.add(trade_data)

# 交換リストを取得
def get_trades():
    trades_ref = db.collection("trades")
    trades = trades_ref.stream()
    return [{"id": trade.id, **trade.to_dict()} for trade in trades]

# 交換済みの状態に更新
def update_trade_status(trade_id):
    trades_ref = db.collection("trades")
    trades_ref.document(trade_id).update({"status": "済み"})

# タイトルの表示
st.title("ポケモンカード交換掲示板")

# 交換希望のカードを追加するフォーム
with st.form(key="add_trade_form"):
    user_name = st.text_input("あなたの名前")
    card_name = st.text_input("交換したいカード名")
    wants_card = st.text_input("欲しいカード名")
    
    submit_button = st.form_submit_button(label="交換希望を追加")
    
    if submit_button:
        if user_name and card_name and wants_card:
            add_card_trade(user_name, card_name, wants_card)
            st.success(f"{user_name}さんの交換希望が追加されました！")
        else:
            st.error("全ての項目を入力してください。")

# 現在の交換掲示板の表示
st.subheader("現在の交換掲示板")

trades = get_trades()

for trade in trades:
    st.write(f"【{trade['user_name']}】")
    st.write(f"交換したいカード: {trade['card_name']}")
    st.write(f"欲しいカード: {trade['wants_card']}")
    st.write(f"状態: {trade['status']}")
    
    if trade['status'] == "交換希望中":
        # 交換が成立した場合「済み」にするボタン
        if st.button(f"交換成立: {trade['user_name']}", key=trade['id']):
            update_trade_status(trade['id'])
            st.success(f"{trade['user_name']}さんとの交換が成立しました。")
