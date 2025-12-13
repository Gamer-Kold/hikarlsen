import chess
class Engine:
    def __init__(self):
        self.board = None # will be set by the "position" command
        self.transposition_table = {} # to speed up alpha-beta

    def position(self, position, moves):
        self.board = chess.Board(position)
        for move in moves:
            board.push_uci(move)

    def negamax(self, depth):
        if depth == 0 or self.board.is_game_over():
            # negate evaluation if it's black's turn
            # this allow's the evaluation function to be absolute
            val = self.evaluate() * (1 if self.board.turn else -1)
            return val
        # negative infinity is always lower than 
        # all integers so it's useful as an initial value
        val = float("-inf") 

        for candidate_move in self.board.legal_moves:
            self.board.push(move) # make the move on the board
            val = max(val, -self.negamax(depth - 1)) # evaluate new position
            self.board.pop() # unmake move
            return val # return

    def evaluate(self):
        pass
