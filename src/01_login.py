
import streamlit as st
import random
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase初期化
if not firebase_admin._apps:
    cred = credentials.Certificate("src/seat-change-optimization-firebase-adminsdk-bjgkk-481de3bcde.json")  # Firebaseの認証情報
    firebase_admin.initialize_app(cred)

# Firestoreにアクセス
db = firestore.client()

# StreamlitのUIを作成
st.title("ランダムな色の丸ゲーム")

# ランダムで色を生成する関数
def generate_random_circle():
    colors = ['赤', '赤', '緑', '青', '青', '青', '黄色','黄色', '黄色', '黄色', '紫', '紫', '紫', '紫', '紫']
    chosen_color = random.choice(colors)
    return chosen_color

# ゲームの実行
if st.button("ランダムな丸を出す"):
    color = generate_random_circle()
    
    if color == '緑':
        result = "スコヴィランex！"
    elif color == '赤':
        result = "カウンターキャッチャー！"
    elif color == '青':
        result = "旧裏カード"
    elif color == '黄色':
        result = "ar1枚"
    else:
        result = "はずれ"

    # 結果を表示
    st.write(f"出た色: {color}")
    st.write(result)

    # Firebaseに結果を保存
    data = {
        'color': color,
        'result': result
    }
    db.collection('game_results').add(data)

    st.write("結果はFirebaseに保存されました！")

# Firebaseから過去の結果を取得して表示
st.subheader("過去の結果")

# 過去のゲーム結果をFirestoreから取得
results_ref = db.collection('game_results')
results = results_ref.stream()

for result in results:
    data = result.to_dict()
    st.write(f"色: {data['color']} - 結果: {data['result']}")
