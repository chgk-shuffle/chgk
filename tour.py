class Tour:

    def __init__(self, countT, countQ, id, type):
        self.id = id
        self.countQ = countQ
        self.teamScore = [0] * countT
        self.type = type
