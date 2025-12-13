import chess
class Engine:
    def __init__(self):
        self.board = None # will be set by the "position" command
        self.transposition_table = {} # to speed up alpha-beta

    def position(self, position, moves):
        if position == None:
            self.board = chess.Board()
        else:
            self.board = chess.Board(" ".join(position))
        for move in moves:
            self.board.push_uci(move)


    def search(self, stop_searching_event):
        best_move = None
        best_move_val = float("-inf")
        for move in self.board.legal_moves:
            if stop_searching_event.is_set():
                break
            self.board.push(move)
            val = self.negamax(float("-inf"), float("inf"), 7)
            if val > best_move_val:
                best_move_val = val
                best_move = move
            self.board.pop()
        return best_move

    def negamax(self, alpha, beta, depth):
        if depth == 0 or self.board.is_game_over():
            # negate evaluation if it's black's turn
            # this allow's the evaluation function to be absolute
            val = self.evaluate() * (1 if self.board.turn else -1)
            return val
        # negative infinity is always lower than 
        # all integers so it's useful as an initial value
        val = float("-inf") 

        for candidate_move in self.board.legal_moves:
            self.board.push(candidate_move) # make the move on the board

            val = max(val, -self.negamax(-beta, -alpha, depth - 1)) # evaluate new position

            # we found a move better than the best one found so far
            alpha = max(val, alpha)

            # prune if our opponent could force us into a worse move
            if alpha >= beta:
                break

            self.board.pop() # unmake move
            return val # return

    def evaluate(self):
        outcome = self.board.outcome()
        if outcome != None:
            if outcome.winner == None:
                return 0
            elif outcome.winner:
                return float("inf")
            else:
                return float("-inf")
        else:
            opponent_moves = self.board.legal_moves.count()
            self.board.turn = not self.board.turn
            your_moves = self.board.legal_moves.count()
            self.board.turn = not self.board.turn
            return (your_moves - opponent_moves) * (1 if self.board.turn else -1) 
