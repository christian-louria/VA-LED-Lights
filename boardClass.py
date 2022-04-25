class BoardInfo:
    rotate = 0
    cascaded = 8
    block_orientation = -90
    blocks_arranged_in_reverse_order = False
    viewportHeight = 50
    viewportWidth = 200

class Board:
    def __init__(self, device, virtual):
        self.device = device
        self.virtual = virtual
