import cocos
from snake import define
import threading
import socket
from snake.gameState import GameState
from snake.arena import Arena
import json
import random
import time
from cocos import director
from snake.gameOverLayer import GameOver


class SnakeBigFightGame(cocos.layer.Layer):
    def __init__(self):
        super(SnakeBigFightGame, self).__init__()
        window_size = director.director.get_window_size()
        # 显示分数
        self.score = cocos.text.Label('30',  # 显示当前分数用的label
                                      font_name='Times New Roman',
                                      font_size=24,
                                      color=define.GOLD)
        self.score.position = 20,  window_size[1]-40
        self.add(self.score, define.SCORE_LAYER_FLOOR)
        # 显示当前人数
        self.people_count = cocos.text.Label('', font_name='Times New Roman', font_size=10, color=define.GOLD)
        self.people_count.position = 20, window_size[1]-60
        self.add(self.people_count, define.SCORE_LAYER_FLOOR)
        # 显示游戏结束画面
        self.game_over = GameOver()
        self.add(self.game_over, define.GAME_OVER_LAYER_FLOOR)
        # 信息存放位置
        self.gameState_list = {}
        # 添加一个竞技场
        self.id = random.randrange(1, 10000)
        self.arena = Arena(self, self.id)
        self.add(self.arena)
        # 保存所有用户的游戏状态
        self.gameState = self.arena.snake.gameState
        self.snake = self.arena.snake
        self.gameState_list[self.id] = self.gameState
        #  连接到服务器
        try:
            self.HOST, self.PORT = 'localhost', 8888
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.HOST, self.PORT))
        except ConnectionRefusedError:
            print('无法连接到服务器')
            return
        self.send_msg(self.id, 'new_client')
        self.writeThread = threading.Thread(target=self.write_thread)
        self.readThread = threading.Thread(target=self.read_thread)
        self.writeThread.start()
        self.readThread.start()
        self.schedule(self.update)

    def update(self, dt):
        self.score.element.text = str(self.gameState.score)
        people_count = len(self.arena.all_snake_list)
        self.people_count.element.text = '当前人数：' + str(people_count)

    def end_game(self):  # 游戏结束时的场景
        self.game_over.visible = True
        self.game_over.score.element.text = str(self.arena.snake.score)

    def send_msg(self, sid, msg_type):
        if msg_type == 'dead':
            print('发送死亡信息')
            dead_dict = {'id': sid, 'is_dead': True}
            msg_dict = {'type': 'client_dead', 'data': dead_dict}
            encode_json = json.dumps(msg_dict) + '#'
            self.client.send(encode_json.encode())
        elif msg_type == 'new_client':
            data_dict = self.snake.gameState.get_state()
            msg_dict = {'type': 'new_client', 'data': data_dict}
            encode_json = json.dumps(msg_dict) + '#'
            self.client.send(encode_json.encode())

    def write_thread(self):  # 向服务器发送消息，发送心跳包
        while True:
            time.sleep(0.1)
            state_dict = self.gameState.get_state()
            msg = {'type': 'client_state', 'data': state_dict}
            encode_json = json.dumps(msg) + '#'
            self.client.send(encode_json.encode())

    def read_thread(self):  # 读取服务器发送过来的消息
        while True:
            buffer = self.client.recv(1024).decode()
            buffer = buffer.split('#')  # 传送过来的信息用‘#’分割
            for item in buffer:
                if item is None or len(item) <= 0:
                    continue
                try:
                    decode_json = json.loads(item)
                    if decode_json['type'] == 'server_to_client':
                        data = decode_json['data']
                        if data['id'] in self.gameState_list:
                            state = self.gameState_list[data['id']]
                            state.update(score=data['score'], rotation=data['rotation'], length=data['length'],
                                                 position=data['position'])
                            break
                        else:
                            gameState = GameState(id=data['id'], score=data['score'], rotation=data['rotation'],
                                                  length=data['length'], color=data['color'], position=data['position'])
                            self.gameState_list[data['id']] = gameState
                    elif decode_json['type'] == 'client_dead':
                        print('客户端接受到死亡信息')
                        dead_id = decode_json['data']['id']
                        if dead_id in self.gameState_list:
                            self.gameState_list.pop(dead_id)
                        self.arena.all_snake_list[dead_id].go_to_dead()
                        self.arena.all_snake_list.pop(dead_id)
                except json.decoder.JSONDecodeError:
                    continue

