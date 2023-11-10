import http.server
import ssl
import signal
import sys
from flask import Flask, request


class AuthServer:
    def __init__(self):
        self.server_address = ('localhost', 4000)
        self.app = Flask(__name__)
        
        self.add_endpoints()
        signal.signal(signal.SIGINT, self.cleanup)
    
    def add_endpoints(self):
        self.app.add_url_rule('/signin', 'signin', self.signin, methods=['POST'])

    def listen(self):
        print(f"Serving at {self.server_address}...")
        context = ('snakeoil.pem', 'snakeoil.key')
        self.app.run('localhost', debug=True, port=4000, ssl_context=context)

    def signin(self):
        data = request.json
        return f"Hello user {data['username']}"

    def cleanup(self, sig, frame):
        sys.exit(0)

    def run(self):
        self.listen()

if __name__ == "__main__":
    auth_server = AuthServer()
    auth_server.run()
