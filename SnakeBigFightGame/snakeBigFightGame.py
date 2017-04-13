import cocos
from cocos import director
from arena import Arena
import define
from gameOverLayer import GameOver


class SnakeBigFightGame(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self):
        super(SnakeBigFightGame, self).__init__()
        self.score = cocos.text.Label('30',  # 显示当前分数用的label
                                      font_name='Times New Roman',
                                      font_size=24,
                                      color=define.GOLD)
        self.score.position = 20, 540
        self.add(self.score, define.SCORE_LAYER_FLOOR)
        self.arena = Arena()  # 添加一个竞技场
        self.add(self.arena)
        self.gameover = GameOver()
        self.add(self.gameover, define.GAME_OVER_LAYER_FLOOR)
        self.schedule(self.update)  # 执行更新

    def update(self, dt):  # 更新当前分数
        self.score.element.text = str(self.arena.snake.score)

    def end_game(self):  # 游戏结束时的场景
        self.gameover.visible = True
        self.gameover.score.element.text = str(self.arena.snake.score)

    def on_mouse_press(self, x, y, buttons, modifiers):  # 当游戏结束时，鼠标点击启动一个新的游戏
        if self.gameover.visible:
            self.gameover.visible = False
            self.arena.unschedule(self.arena.update)
            self.remove(self.arena)
            self.arena = Arena()
            self.add(self.arena)

if __name__ == '__main__':  # 启动游戏
    director.director.init(800, 600, caption="Snake Big Fight")
    main_scene = cocos.scene.Scene(SnakeBigFightGame())
    cocos.director.director.run(main_scene)
