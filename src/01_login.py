import asyncio
import logging
import email
from email.header import decode_header

# IMAPサーバーの基本設定
HOST = 'localhost'
PORT = 1223  # IMAPの標準ポートは143ですが、こちらをテスト用に変更しています
MAILBOX = 'inbox'

# ログ設定
logging.basicConfig(level=logging.DEBUG)

class SimpleIMAPServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.transport = None
        self.buffer = b""
        self.state = 'waiting'

    def connection_made(self, transport):
        self.transport = transport
        logging.info("Client connected")
        self.transport.write(b"* OK IMAP4rev1 Server Ready\r\n")

    def data_received(self, data):
        self.buffer += data
        self.process_request()

    def process_request(self):
        # リクエストを処理する（簡略化のため、単純なレスポンスを返します）
        if self.buffer.endswith(b"\r\n"):
            request = self.buffer.decode('utf-8').strip()
            self.buffer = b""
            logging.info(f"Received request: {request}")
            
            if request.startswith('A001 LOGIN'):
                # ユーザー認証処理（簡略化）
                self.transport.write(b"A001 OK LOGIN completed\r\n")
            elif request.startswith('A002 LIST'):
                # メールボックスのリスト（例: inbox）
                self.transport.write(b"A002 * LIST (\"\" \"\") \"inbox\"\r\n")
                self.transport.write(b"A002 OK LIST completed\r\n")
            elif request.startswith('A003 SELECT'):
                # メールボックスの選択（例: inbox）
                self.transport.write(b"A003 * FLAGS (\\Seen \\Answered \\Flagged \\Deleted \\Draft \\Recent)\r\n")
                self.transport.write(b"A003 * OK [PERMANENTFLAGS (\\Seen \\Answered \\Flagged \\Deleted \\Draft \\Recent)]\r\n")
                self.transport.write(b"A003 OK [UIDVALIDITY 1] SELECT completed\r\n")
            elif request.startswith('A004 FETCH'):
                # メールデータのフェッチ（ここでは単純なダミーデータ）
                message = email.message_from_string("Subject: Test Email\r\nFrom: test@example.com\r\n\r\nThis is a test email body.")
                subject, encoding = decode_header(message["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                email_data = f"Subject: {subject}\r\nFrom: {message['From']}\r\n\r\n{message.get_payload()}"
                self.transport.write(f"A004 * FETCH (UID 1 BODY[TEXT] {{{len(email_data)}}}\r\n".encode())
                self.transport.write(email_data.encode())
                self.transport.write(b"A004 OK FETCH completed\r\n")
            elif request.startswith('A005 LOGOUT'):
                # ログアウト
                self.transport.write(b"A005 OK LOGOUT completed\r\n")
                self.transport.close()
            else:
                self.transport.write(b"BAD command\r\n")

async def main():
    # サーバーの作成と実行
    loop = asyncio.get_event_loop()
    server = await loop.create_server(
        lambda: SimpleIMAPServerProtocol(),
        HOST, PORT
    )
    logging.info(f'Serving on {HOST}:{PORT}')
    try:
        # サーバーが停止するまで待機
        await server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Server stopped")

if __name__ == '__main__':
    asyncio.run(main())
