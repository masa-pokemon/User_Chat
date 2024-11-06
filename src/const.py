import firebase_admin
from firebase_admin import credentials, firestore

# Firebaseのサービスアカウントキーのパスを指定
cred = credentials.Certificate('src/seat-change-optimization-firebase-adminsdk-bjgkk-481de3bcde.json')

# Firebase Admin SDKの初期化
firebase_admin.initialize_app(cred)

# Firestoreデータベースの参照
db = firestore.client()

def get_trade_posts():
    """Firestoreからトレード掲示板の投稿を取得"""
    posts_ref = db.collection('trade_posts')
    docs = posts_ref.stream()
    posts = []
    for doc in docs:
        posts.append(doc.to_dict())
    return posts

def add_trade_post(title, description, user_name):
    """新しいトレード投稿をFirestoreに追加"""
    posts_ref = db.collection('trade_posts')
    post_data = {
        'title': title,
        'description': description,
        'user_name': user_name,
        'created_at': firestore.SERVER_TIMESTAMP
    }
    posts_ref.add(post_data)
