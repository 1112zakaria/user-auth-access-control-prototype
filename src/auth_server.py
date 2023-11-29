import http.server
import ssl
import signal
import sys
from flask import Flask, request
from problem4a import AuthServer

if __name__ == "__main__":
    auth_server = AuthServer()
    auth_server.run()
