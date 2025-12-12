import chess
class Engine:
    def __init__(self):
        self.board = None # will be set by the "position" command
        self.transposition_table = {} # to speed up alpha-beta

    def position(self, position, moves):
        self.board = chess.Board(position)
        for move in moves:
            board.push_uci(move)
