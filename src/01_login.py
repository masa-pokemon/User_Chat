import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 初期化（すでに初期化されていない場合のみ実行）
if not firebase_admin._apps:
    cred = credentials.Certificate("src/seat-change-optimization-firebase-adminsdk-bjgkk-481de3bcde.json")  # Firebaseの認証情報
    firebase_admin.initialize_app(cred)

# Firestore インスタンスを取得
db = firestore.client()

# カード情報をFirestoreから取得
def get_cards():
    cards_ref = db.collection("cards")
    docs = cards_ref.stream()
    cards = []
    for doc in docs:
        card = doc.to_dict()
        card['id'] = doc.id  # ドキュメントID（カードID）を追加
        cards.append(card)
    return cards

# 新しいカードをFirestoreに追加
def add_card(name, price, image_url, quantity):
    db.collection("cards").add({
        "name": name,
        "price": price,
        "image_url": image_url,
        "quantity": quantity,
        "buyers": []  # 初期状態では購入者は空のリスト
    })

# カードの購入処理
def purchase_card(card_id, buyer_name):
    card_ref = db.collection("cards").document(card_id)
    card = card_ref.get().to_dict()
    
    if card["quantity"] > 0:
        # 残り数量を1減らす
        new_quantity = card["quantity"] - 1
        # 購入者リストに追加
        buyers = card["buyers"] + [buyer_name]
        # Firestoreを更新
        card_ref.update({
            "quantity": new_quantity,
            "buyers": buyers
        })
        return True
    else:
        return False

# Streamlit アプリの構成
st.title('ポケカ販売サイト')

# 新しいカードを追加するフォーム
with st.form(key='add_card_form'):
    name = st.text_input('カード名')
    price = st.text_input('価格を入力 or 交換して欲しいカードを入力')
    image_url = st.text_input('画像URL')
    quantity = st.number_input('残りの数量', min_value=1)
    submit_button = st.form_submit_button(label='カードを追加')

    if submit_button:
        if name and price and image_url and quantity:
            add_card(name, price, image_url, quantity)
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
        st.write(f"価格 or 求めているカード: {card['price']}")
        st.write(f"残り数量: {card['quantity']}枚")
        st.write(f"購入者: {', '.join(card['buyers']) if card['buyers'] else 'まだ購入者なし'}")
        
        # 購入ボタン
        with st.form(key=f"purchase_form_{card['id']}"):
            buyer_name = st.text_input('購入者名', key=f'buyer_name_{card["id"]}')
            purchase_button = st.form_submit_button(label=f"{card['name']} を購入")

            if purchase_button:
                if buyer_name:
                    if purchase_card(card['id'], buyer_name):
                        st.success(f"{card['name']} を購入しました！")
                    else:
                        st.error("在庫がありません。")
                else:
                    st.error("購入者名を入力してください。")
else:
    st.write("現在販売中のカードはありません。")
