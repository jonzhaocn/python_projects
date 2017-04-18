from cocos import director, scene
from snake.snakeBigFightGame import SnakeBigFightGame


if __name__ == '__main__':
    director.director.init()
    main_scene = scene.Scene(SnakeBigFightGame())
    director.director.run(main_scene)