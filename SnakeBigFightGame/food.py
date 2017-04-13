import cocos
import random
import define
import math


class Food(cocos.sprite.Sprite):  # 食物
    def __init__(self, position, parent):
        super(Food, self).__init__('circle.png')
        self.color = random.choice(define.ALL_COLOR)
        self.position = position
        self.scale = 0.8
        self.x += random.randrange(-10, 10)
        self.y += random.randrange(-10, 10)
        self.schedule(self.update)
        self.parent = parent

    def update(self, dt):  # 如果食物的数量少于一定的数量，则要增加食物
        arena = self.parent.parent
        snake = arena.snake
        dis = math.sqrt(math.pow(self.x-snake.x, 2)+math.pow(self.y-snake.y, 2))
        if dis < 10:
            snake.score += 100
            self.parent.remove(self)
            arena.food_list.remove(self)

