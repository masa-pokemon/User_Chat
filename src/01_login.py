import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# データ読み込み
@st.cache_data
def load_data():
    # CSVファイルをアップロード
    uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        return data
    return None

# モデルのトレーニング
def train_model(data):
    # メッセージと宛先を分割
    X = data['message']
    y = data['recipient']

    # テキストデータの特徴量化
    vectorizer = TfidfVectorizer(max_features=5000)
    X_vec = vectorizer.fit_transform(X)

    # トレーニングデータとテストデータに分割
    X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

    # ランダムフォレスト分類器を使用
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # テストデータで予測
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    st.write(f"モデルの精度: {accuracy:.2f}")

    # モデルとベクトライザーを保存
    joblib.dump(clf, 'message_recipient_model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')

    return clf, vectorizer

# メッセージの予測
def predict_recipient(message, clf, vectorizer):
    message_vec = vectorizer.transform([message])
    prediction = clf.predict(message_vec)
    return prediction[0]

# Streamlit UIの設定
def main():
    st.title("メッセージ予測AI")
    
    # データの読み込み
    data = load_data()
    if data is not None:
        st.write(data.head())

        # モデルのトレーニング
        if st.button('モデルをトレーニング'):
            clf, vectorizer = train_model(data)
            st.success("モデルのトレーニングが完了しました！")
        
        # メッセージの入力と予測
        message_input = st.text_area("予測するメッセージを入力してください")
        if message_input:
            if 'clf' in globals() and 'vectorizer' in globals():
                recipient = predict_recipient(message_input, clf, vectorizer)
                st.write(f"予測された受取人: {recipient}")
            else:
                st.warning("まずモデルをトレーニングしてください")
    else:
        st.warning("CSVファイルをアップロードしてください")

if __name__ == "__main__":
    main()
