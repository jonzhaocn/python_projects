import cocos
from cocos import director
import define


class GameOver(cocos.layer.ColorLayer):  # 游戏结束时的画面
    def __init__(self):
        super(GameOver, self).__init__(200, 235, 235, 200, 400, 300)
        self.position = (director.director.get_window_size()[0] / 2 - 200,
                         director.director.get_window_size()[1] / 2 - 150)
        self.visible = False
        self.score = cocos.text.Label('',  # 显示分数
                                      font_name='SimHei',
                                      font_size=36,
                                      color=define.MAROON)
        self.score.position = 250, 200
        self.add(self.score)

        text = cocos.text.Label('SCORE: ',
                                font_name='SimHei',
                                font_size=24,
                                color=define.MAROON)
        text.position = 50, 200
        self.add(text)
        text = cocos.text.Label('CLICK TO REPLAY...',
                                font_name='SimHei',
                                font_size=24,
                                color=define.MAROON)
        text.position = 50, 100
        self.add(text)