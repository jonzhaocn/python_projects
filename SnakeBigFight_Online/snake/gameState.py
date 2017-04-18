
class GameState(object):
    def __init__(self, id, score, rotation, length, color, position):
        self.id = id
        self.score = score
        self.rotation = rotation
        self.length = length
        self.color = color
        self.position = position

    def get_state(self):
        state = {'id': self.id, 'score': self.score, 'rotation': self.rotation, 'length': self.length,
                 'color': self.color, 'position': self.position}
        return state

    def update(self, score, rotation, length, position):
        self.score = score
        self.rotation = rotation
        self.length = length
        self.position = position

