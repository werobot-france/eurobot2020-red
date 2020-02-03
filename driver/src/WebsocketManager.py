from threading import Thread
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from bottle import request, Bottle, abort
from geventwebsocket import WebSocketServer, WebSocketApplication, Resource, WebSocketError
from collections import OrderedDict
import json

class InputExecutor(Thread):
    def __init__(self, robot, params):
        print('hey1')
        self.robot = robot
        self.params = params
        Thread.__init__(self)

    def run(self):
        self.robot.goTo(*self.params)

class WebsocketManager(Thread):
    def __init__(self):
        self.context = None
        self.robot = None
        self.online = False
        Thread.__init__(self)
        
    def setRobot(self, robot):
        self.robot = robot
 
    def setContext(self, context):
        self.context = context
    
    def emit(self, event, data):
        rawJson = json.dumps({ "event": event, "data": data })
        if self.context != None:
            for client in self.context.handler.server.clients.values():
                client.ws.send(rawJson)
        
    def isOnline(self):
        return self.online
    
    def run(self):
        self.online = True
        manager = self
        class MainApplication(WebSocketApplication):
            def on_open(self):
                print("Connection opened")
                manager.setContext(self.ws)
            
            def on_message(self, message):
                print(message)
                data = json.loads(message)
                cmd = data["cmd"]
                if "args" in data:
                    args = data["args"]
                else:
                    args = None
                if cmd == 'goto':
                    print('I will goto', data["args"]["x"], data["args"]["y"])
                    executor = InputExecutor(manager.robot, [data["args"]["y"], data["args"]["x"], 20, True])
                    executor.start()
                elif cmd == 'stop':
                    print('Stop command received')
                    manager.robot.cancelOperations()
                    manager.robot.stopMotors()
                    print('STOOOOP')
                elif cmd == 'reset_pos':
                    print('Reset pos command')
                    manager.robot.positionWatcher.reset()
                elif cmd == 'start_position_trace':
                    print('LOG# > Enabled position trace')
                elif cmd == 'stop_position_trace':
                    print('LOG# > Disabled position trace')
                else:
                    print("Command not recognized")
        
        print('Start a websocket server on 0.0.0.0:8080')
        WebSocketServer(
            ('0.0.0.0', 8080),
            Resource(OrderedDict([('/', MainApplication)]))
        ).serve_forever()

