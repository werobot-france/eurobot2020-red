import asyncio
import websockets
from time import sleep
from threading import Thread
from bottle import request, Bottle, abort

globalWs = None

def getter():
	print(globalWs)
	return globalWs

def thread():
	x = 0
	while True:
		x += 1
		print(request.environ.get('wsgi.websocket'), x)
		sleep(1)

aThread = Thread(target=thread)
#aThread.start()

app = Bottle()
@app.route('/websocket')
def handle_websocket():
	wsock = request.environ.get('wsgi.websocket')
	print(wsock)
	while True:
		try:
			message = wsock.receive()
			wsock.send("Your message was: %r" % message)
		except WebSocketError:
			break

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

server = WSGIServer(("0.0.0.0", 8080), app,
handler_class=WebSocketHandler)
server.serve_forever()
