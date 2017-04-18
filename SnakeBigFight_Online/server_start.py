import socket
import threading
import json
import time
from snake.gameState import GameState

client_list = []
client_id_list = {}
gameState_list = []
server_read_thread_list = {}
server_write_thread_list = {}


class GameServer(object):
    def __init__(self):
        self.HOST, self.PORT = '', 8888
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.HOST, self.PORT))
        self.server.listen()
        self.snake_count = 0

    def server_forever(self):
        while True:
            client, client_address = self.server.accept()
            # 添加到用户列表
            client_list.append(client)
            server_read_thread = ServerReadThread(client)
            server_read_thread.start()
            server_read_thread_list[client] = server_read_thread
            server_write_thread = ServerWriteThread(client)
            server_write_thread.start()
            server_write_thread_list[client] = server_write_thread


class ServerReadThread(threading.Thread):  # 读取从客户端发送过来的消息
    def __init__(self, client):
        super(ServerReadThread, self).__init__()
        self.client = client
        self.forever = True

    def run(self):
        while self.forever:
            buffer = self.client.recv(1024).decode()
            buffer = buffer.split('#')
            for item in buffer:
                if item is None or len(item) <= 0:
                    continue
                try:
                    decode_json = json.loads(item)
                    if decode_json['type'] == 'client_state':
                        data = decode_json['data']
                        if data['id'] in client_id_list:
                            for state in gameState_list:
                                if state.id == data['id']:
                                    state.update(score=data['score'], rotation=data['rotation'], length=data['length'],
                                                 position=data['position'])
                                    break
                    elif decode_json['type'] == 'new_client':
                        data = decode_json['data']
                        gameState = GameState(id=data['id'], score=data['score'], rotation=data['rotation'],
                                                  length=data['length'], color=data['color'], position=data['position'])
                        gameState_list.append(gameState)
                        client_id_list[data['id']] = self.client
                    elif decode_json['type'] == 'client_dead':
                        dead_id = decode_json['data']['id']
                        self.send_msg(dead_id, 'dead')
                        if dead_id in client_id_list:
                            dead_client = client_id_list[dead_id]
                            client_id_list.pop(dead_id)
                            if dead_client in server_read_thread_list:
                                server_read_thread_list[dead_client].forver = False
                                server_read_thread_list.pop(dead_client)
                            if dead_client in server_write_thread_list:
                                server_write_thread_list[dead_client].forver = False
                                server_write_thread_list.pop(dead_client)
                            if dead_client in client_list:
                                client_list.remove(dead_client)
                        for state in gameState_list:
                            if state.id == dead_id:
                                gameState_list.remove(state)
                except json.decoder.JSONDecodeError:
                    continue

    def send_msg(self, sid, msg_type):
        if msg_type == 'dead':
            dead_dict = {'id': sid, 'is_dead': True}
            msg_dict = {'type': 'client_dead', 'data': dead_dict}
            encode_json = json.dumps(msg_dict) + '#'
            for client in client_list:
                client.sendall(encode_json.encode())
            for state in gameState_list:
                if state.id == sid:
                    gameState_list.remove(state)


class ServerWriteThread(threading.Thread):  # 向客户端发送消息
    def __init__(self, client):
        super(ServerWriteThread, self).__init__()
        self.client = client
        self.forever = True

    def run(self):
        while self.forever:
            time.sleep(0.5)
            for state in gameState_list:
                msg = state.get_state()
                msg = {'type': 'server_to_client', 'data': msg}
                encode_json = json.dumps(msg) + '#'
                self.client.sendall(encode_json.encode())

if __name__ == '__main__':
    gameServer = GameServer()
    gameServer.server_forever()
