import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(); // Firebase初期化
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ポケモンカード交換掲示板',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: ExchangeBoard(),
    );
  }
}

class ExchangeBoard extends StatefulWidget {
  @override
  _ExchangeBoardState createState() => _ExchangeBoardState();
}

class _ExchangeBoardState extends State<ExchangeBoard> {
  final TextEditingController _cardController = TextEditingController();
  final TextEditingController _nameController = TextEditingController();

  // Firestoreインスタンス
  final FirebaseFirestore _firestore = FirebaseFirestore.instance;

  // 新しい交換リクエストをFirestoreに追加
  Future<void> _addExchangeRequest() async {
    String card = _cardController.text.trim();
    String name = _nameController.text.trim();

    if (card.isNotEmpty && name.isNotEmpty) {
      await _firestore.collection('exchanges').add({
        'name': name,
        'card': card,
        'status': 'pending', // 初期状態は「交換待ち」
      });

      // フィールドをクリア
      _cardController.clear();
      _nameController.clear();
    }
  }

  // 交換リクエストの状態を更新
  Future<void> _markAsCompleted(String docId) async {
    await _firestore.collection('exchanges').doc(docId).update({
      'status': 'completed',
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('ポケモンカード交換掲示板'),
      ),
      body: Column(
        children: [
          // 名前入力フィールド
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: TextField(
              controller: _nameController,
              decoration: InputDecoration(labelText: 'あなたの名前'),
            ),
          ),
          // カード名入力フィールド
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: TextField(
              controller: _cardController,
              decoration: InputDecoration(labelText: '交換したいカード'),
            ),
          ),
          // 交換リクエスト投稿ボタン
          ElevatedButton(
            onPressed: _addExchangeRequest,
            child: Text('交換リクエストを投稿'),
          ),
          // 交換リクエストリスト
          Expanded(
            child: StreamBuilder<QuerySnapshot>(
              stream: _firestore.collection('exchanges').snapshots(),
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return Center(child: CircularProgressIndicator());
                }

                if (!snapshot.hasData || snapshot.data!.docs.isEmpty) {
                  return Center(child: Text('交換リクエストはありません。'));
                }

                var exchangeRequests = snapshot.data!.docs;
                return ListView.builder(
                  itemCount: exchangeRequests.length,
                  itemBuilder: (context, index) {
                    var exchange = exchangeRequests[index];
                    return ListTile(
                      title: Text(exchange['name'] + ' さん'),
                      subtitle: Text(exchange['card']),
                      trailing: exchange['status'] == 'completed'
                          ? Icon(Icons.check, color: Colors.green) // 完了時にチェックアイコン
                          : ElevatedButton(
                              onPressed: () {
                                _markAsCompleted(exchange.id); // 交換完了ボタン
                              },
                              child: Text('交換済み'),
                            ),
                    );
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
