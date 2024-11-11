import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score

# サンプルデータ
data = {
    "message": [
        "Hello, can you send me the report?",
        "Please confirm your meeting time.",
        "Urgent: The server is down.",
        "Let's schedule a meeting.",
        "Your package has been shipped."
    ],
    "recipient": [
        "sales", "manager", "technical_support", "manager", "customer_service"
    ]
}

df = pd.DataFrame(data)

# 特徴量とラベルの設定
X = df["message"]
y = df["recipient"]

# トレーニングデータとテストデータに分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# モデルのパイプラインを作成
model = make_pipeline(CountVectorizer(), LogisticRegression())
model.fit(X_train, y_train)

# テストデータに対する精度を表示
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Streamlit アプリケーションの設定
st.title("メッセージ宛先予測 AI")

st.write("メッセージに基づいて、宛先を予測します。")
st.write(f"モデルの精度: {accuracy:.2f}")

# セッション状態を使って前回のメッセージを保存
if "previous_message" not in st.session_state:
    st.session_state.previous_message = None
    st.session_state.previous_prediction = None

# ユーザー入力を取得
user_input = st.text_area("メッセージを入力してください:")

# 予測ボタンが押されたとき
if st.button("予測"):
    if user_input:
        # 1つ前のメッセージと現在のメッセージを組み合わせる
        if st.session_state.previous_message:
            combined_input = st.session_state.previous_message + " " + user_input
        else:
            combined_input = user_input
        
        # 予測を行う
        prediction = model.predict([combined_input])[0]

        # 結果を表示
        st.write(f"予測された宛先: {prediction}")
        
        # 現在のメッセージと予測を保存（次回の入力で使う）
        st.session_state.previous_message = user_input
        st.session_state.previous_prediction = prediction
    else:
        st.write("メッセージを入力してください。")

# 前回のメッセージと予測がある場合は表示
if st.session_state.previous_message:
    st.write(f"前回のメッセージ: {st.session_state.previous_message}")
    st.write(f"前回の予測された宛先: {st.session_state.previous_prediction}")
