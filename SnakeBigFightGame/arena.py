import cocos
from snake import Snake
from cocos import batch, director
import random
import define
from food import Food


class Arena(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self):
        super(Arena, self).__init__(250, 255, 255, 255, define.WIDTH, define.HEIGHT)  # 定义背景、长宽
        window_size = director.director.get_window_size()  # 获取当前的窗口大小
        self.center = (window_size[0]/2, window_size[1]/2)
        self.batch = batch.BatchNode()
        self.add(self.batch)
        self.all_snake_list = []
        self.food_list = []
        # 增加主角
        self.snake = Snake(self)
        self.add(self.snake, define.SNAKE_FLOOR)
        self.all_snake_list.append(self.snake)
        # 增加敌人
        for i in range(random.randrange(5, 10)):
            enemy = Snake(self, True)
            self.add(enemy, define.SNAKE_FLOOR)
            self.all_snake_list.append(enemy)
        self.schedule(self.update)

    def update(self, dt):  # 背景移动，看起来主角就像都定在中心了一样
        self.x = self.center[0] - self.snake.x
        self.y = self.center[1] - self.snake.y
        if self.snake.is_dead:
            self.parent.end_game()
        if len(self.food_list) < define.FOOD_COUNT:  # 如果食物减少了，就增加食物
            x = random.randrange(0, define.WIDTH)
            y = random.randrange(0, define.HEIGHT)
            food = Food((x, y), self.batch)
            self.batch.add(food, define.FOOD_FLOOR)
            self.food_list.append(food)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):  # 监听鼠标拖拽，改变主角的蛇头方向
        self.snake.update_angle(x, y)

    def on_key_press(self, key, modifiers):  # 按住空格键蛇加速
        # 按下按键自动触发本方法
        if key == 32:
            self.snake.speed_up()

    def on_key_release(self, key, modifiers):  # 松开空格键，恢复原速
        # 松开按键自动触发本方法
        if key == 32:
            self.snake.move_time = self.snake.max_move_time







