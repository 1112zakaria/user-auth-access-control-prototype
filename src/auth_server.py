import http.server
import ssl
import signal
import sys



class AuthServer:
    def __init__(self):
        self.server_address = ('localhost', 4000)
        self.server = http.server.HTTPServer(self.server_address, http.server.SimpleHTTPRequestHandler)
        self.server.socket = ssl.wrap_socket(self.server.socket,
                                             server_side=True,
                                             certfile='localhost.pem',
                                             ssl_version=ssl.PROTOCOL_TLS)
        
        signal.signal(signal.SIGINT, self.cleanup)

    def listen(self):
        print(f"Serving at {self.server_address}...")
        self.server.serve_forever()

    def cleanup(self):
        sys.exit(0)

    def run(self):
        self.listen()

if __name__ == "__main__":
    auth_server = AuthServer()
    auth_server.run()
