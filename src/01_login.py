import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase初期化（既に初期化されていない場合のみ実行）
if not firebase_admin._apps:
    cred = credentials.Certificate("src/seat-change-optimization-firebase-adminsdk-bjgkk-481de3bcde.json")
    firebase_admin.initialize_app(cred)

# Firestoreインスタンスを取得
db = firestore.client()

# カード情報をFirestoreから取得
def get_cards():
    cards_ref = db.collection("cards")
    docs = cards_ref.stream()
    cards = []
    for doc in docs:
        cards.append(doc.to_dict())
    return cards

# 新しいカードをFirestoreに追加
def add_card(name, price, image_url):
    db.collection("cards").add({
        "name": name,
        "price": price,
        "image_url": image_url
    })

# Streamlitアプリの構成
st.title('ポケカ販売サイト')

# 新しいカードを追加するフォーム
with st.form(key='add_card_form'):
    name = st.text_input('カード名')
    price = st.number_input('価格', min_value=1)
    image_url = st.text_input('画像URL')
    submit_button = st.form_submit_button(label='カードを追加')

    if submit_button:
        if name and price and image_url:
            add_card(name, price, image_url)
            st.success(f'{name} が追加されました！')
        else:
            st.error('すべてのフィールドを入力してください。')

# 販売中のカードを表示
st.header("販売中のポケカ")
cards = get_cards()
if cards:
    for card in cards:
        st.subheader(card['name'])
        st.image(card['image_url'], width=200)
        st.write(f"価格: {card['price']}円")
        if st.button(f"購入 {card['name']}", key=card['name']):
            st.write(f"{card['name']} を購入しました！")
else:
    st.write("現在販売中のカードはありません。")
