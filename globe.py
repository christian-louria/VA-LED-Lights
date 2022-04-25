kill = False

class DotMatrix:
    custom = []
    boards = ["weather", "time"]

    def changeMode(self, boardNumber, mode):
        self.boards[boardNumber] = mode
        # setattr(self, boardNumber, mode)


dotMatrix = DotMatrix()

