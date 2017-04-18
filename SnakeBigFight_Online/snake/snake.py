import cocos
from cocos import sprite, director
from snake import define
import random
import math
from snake.gameState import GameState
from cocos.actions import *


class Snake(cocos.cocosnode.CocosNode):
    def __init__(self, parent, id, is_enemy, **kwargs):
        super(Snake, self).__init__()
        self.parent = parent
        self.scale = 1.5
        self.is_enemy = is_enemy
        self.is_dead = False
        window_size = director.director.get_window_size()
        self.center = (window_size[0] / 2, window_size[1] / 2)  # center即主角蛇头相对于窗口的位置
        if not self.is_enemy:
            self.id = id
            self.position = random.randrange(200, define.WIDTH-200), random.randrange(200, define.HEIGHT-200)
            self.rotation = random.randrange(0, 360)
            self.color = random.choice(define.ALL_COLOR)
        else:
            self.id = id
            self.position = kwargs['position']
            self.rotation = kwargs['rotation']
            self.color = kwargs['color']
        #  增加头部
        self.rotation_rate = 90
        self.head = sprite.Sprite('circle.png', color=self.color)
        self.add(self.head)
        self.length = 5
        self.score = 5000
        self.score_to_body = 1000
        self.move_time = 1
        self.body = []
        self.gameState = GameState(id=self.id, score=self.score, rotation=self.rotation, length=self.length,
                                   color=self.color, position=self.position)
        # 增加一个眼球
        eyeball = sprite.Sprite('circle.png', color=define.WHITE)
        eyeball.scale = 0.5  # 缩放是相对于父节点
        eyeball.position = self.head.position
        eyeball.x = -5  # 偏移是相对于父节点
        eyeball.y = 2
        eye = sprite.Sprite('circle.png', color=define.BLACK)
        eye.scale = 0.5
        eyeball.add(eye)
        self.head.add(eyeball)
        # 增加一个眼球
        eyeball = sprite.Sprite('circle.png', color=define.WHITE)
        eyeball.scale = 0.5  # 缩放是相对于父节点
        eyeball.position = self.head.position
        eyeball.x = 5  # 偏移是相对于父节点
        eyeball.y = 2
        eye = sprite.Sprite('circle.png', color=define.BLACK)
        eye.scale = 0.5
        eyeball.add(eye)
        self.head.add(eyeball)
        # 开始初始化
        self.init_body()
        self.schedule(self.update)

    def add_body(self):  # 增加身体长度的函数
        body_part = sprite.Sprite('circle.png', color=self.color)
        if len(self.body) == 0:  # 如果当前只有头部，根据当前头部的方向，确定新生成的身体的位置
            x = -math.sin(self.rotation / 360 * 2 * math.pi) * body_part.width
            y = -math.cos(self.rotation / 360 * 2 * math.pi) * body_part.height
            last_x, last_y = self.position
            body_part.rotation = self.rotation
        else:  # 如果已有一部分的身体，根据最后一个身体部分的位置，确定新生成的身体的位置
            x = -math.sin(self.body[-1].rotation / 360 * 2 * math.pi) * body_part.width
            y = -math.cos(self.body[-1].rotation / 360 * 2 * math.pi) * body_part.height
            last_x, last_y = self.body[-1].position
            body_part.rotation = self.body[-1].rotation
        body_part.position = last_x + x, last_y + y
        body_part.scale = 1.5
        self.body.append(body_part)  # 将新生成的部分部分加入到身体中
        self.parent.batch.add(body_part, define.SNAKE_FLOOR)

    def init_body(self):  # 初始化身体
        for i in range(self.length):
            self.add_body()

    def update(self, dt):
        self.gameState.rotation = self.rotation
        self.gameState.score = self.score
        self.gameState.position = self.position
        self.gameState.length = self.length
        snake_id_list = self.parent.all_snake_list.keys()
        for sid in snake_id_list:  # 检测是否与其他蛇发生碰撞，是否撞到边界
            self.chech_crash(another=self.parent.all_snake_list[sid])
        if self.score / self.score_to_body > len(self.body):  # 分数增加，身体变长
            self.add_body()
        tar_x = math.sin(self.rotation / 360 * 2 * math.pi) * self.head.width  # 往头部指向的方向移动，因为移动的速率是固定的
        tar_y = math.cos(self.rotation / 360 * 2 * math.pi) * self.head.height  # 所以定义了move_time以代替移动速度
        self.do(MoveBy((tar_x, tar_y), self.move_time))
        for i in range(len(self.body)):  # 身体中的每个部分，跟着前一个身体部分的方向位置移动
            if i == 0:
                self.body[i].do(MoveTo(self.position, self.move_time))
                self.body[i].do(RotateTo(self.rotation, self.move_time))
            else:
                self.body[i].do(MoveTo(self.body[i - 1].position, self.move_time))
                self.body[i].do(RotateTo(self.body[i - 1].rotation, self.move_time))

    def update_angle(self, x, y):  # 当用户鼠标拖拽时，主角要更新自己的头部的角度
        angle = self.get_angle((x, y))  # 计算出当前鼠标位置与头部的夹角
        angle = (angle + 360) % 360
        angle_dist = (angle - self.rotation + 360) % 360
        angle_change = 45  # 每次要变换的角度
        if 60 < angle_dist < 180:
            self.do(RotateBy(angle_change, angle_change / self.rotation_rate))
        elif 240 < angle_dist < 360:
            self.do(RotateBy(-angle_change, angle_change / self.rotation_rate))

    def get_angle(self, position_tar):  # 计算出当前鼠标位置与头部的夹角
        x_tar, y_tar = position_tar
        x_from, y_from = self.center
        len_y = y_tar - y_from
        len_x = x_tar - x_from
        if len_x == 0:
            return self.rotation
        tan_yx = math.fabs(len_y / len_x)
        angle = 0
        if len_y > 0 and len_x < 0:  # 分成四个象限来考虑
            angle = math.atan(tan_yx) * 180 / math.pi - 90
        elif len_y > 0 and len_x > 0:
            angle = 90 - math.atan(tan_yx) * 180 / math.pi
        elif len_y < 0 and len_x < 0:
            angle = -math.atan(tan_yx) * 180 / math.pi - 90
        elif len_y < 0 and len_x > 0:
            angle = math.atan(tan_yx) * 180 / math.pi + 90
        return angle

    def chech_crash(self, another):  # 检测碰撞的函数
        if self is None or another is None:
            return
        if self.is_dead or another.is_dead:
            return
        if (self.x < 0 or self.x > define.WIDTH) or (self.y < 0 or self.y > define.HEIGHT):  # 检测是否碰到边界
            self.send_dead_msg()
            return
        if self == another:
            return
        for body_part in another.body:  # 是否撞到其他的蛇
            if math.sqrt(math.pow(self.x - body_part.x, 2) + math.pow(self.y - body_part.y, 2)) < 24:
                self.send_dead_msg()

    def send_dead_msg(self):
        if not self.is_dead and not self.is_enemy:  # 如果撞到了，则启动死亡
            self.is_dead = True
            game = self.parent.parent
            game.send_msg(self.id, 'dead')

    def go_to_dead(self):
        self.unschedule(self.update)  # 取消计划任务
        for body_part in self.body:  # 移除身体
            self.parent.batch.remove(body_part)
        self.parent.remove(self)
