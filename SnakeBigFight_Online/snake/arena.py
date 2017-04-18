import cocos
from snake import define
from cocos import batch, director
from snake.snake import Snake


class Arena(cocos.layer.ColorLayer):
    is_event_handler = True

    def __init__(self, parent, snake_id):
        super(Arena, self).__init__(250, 255, 255, 255, define.WIDTH, define.HEIGHT)
        window_size = director.director.get_window_size()  # 获取当前的窗口大小
        self.center = (window_size[0] / 2, window_size[1] / 2)
        self.batch = batch.CocosNode()
        self.add(self.batch)
        self.all_snake_list = {}
        self.id = snake_id
        self.parent = parent
        self.gameState_list = self.parent.gameState_list
        # 增加主角
        self.snake = Snake(self, self.id, False)
        self.all_snake_list[self.id] = self.snake
        self.add(self.snake, define.SNAKE_FLOOR)
        self.schedule(self.update)

    def update(self, dt):  # 背景移动，看起来主角就像都定在中心了一样
        self.x = self.center[0] - self.snake.x
        self.y = self.center[1] - self.snake.y
        if self.snake.is_dead:
            self.parent.end_game()
        for state in self.gameState_list.values():
            if state is None:
                continue
            if state.id == self.id:  # 这条蛇是自己
                continue
            else:
                if state.id in self.all_snake_list:  # 改变这条蛇的状态
                    snake = self.all_snake_list[state.id]
                    if snake is None:
                        continue
                    snake.score = state.score
                    snake.position = state.position
                    snake.rotation = state.rotation
                else:  # 新增一条蛇
                    snake = Snake(self, state.id, True, position=state.position, rotation=state.rotation,
                                  color=state.color)
                    self.add(snake, define.SNAKE_FLOOR)
                    self.all_snake_list[state.id] = snake

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):  # 监听鼠标拖拽，改变主角的蛇头方向
        self.snake.update_angle(x, y)

