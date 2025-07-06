# api/index.py

from app.main import app
from asgiref.wsgi import WsgiToAsgi

asgi_app = WsgiToAsgi(app)

def handler(environ, start_response):
    return asgi_app(environ, start_response)