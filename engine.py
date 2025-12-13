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
            print(f"checking move {move.uci()}")
            val = self.negamax(float("-inf"), float("inf"), 4) * (-1 if self.board.turn else 1)
            self.board.pop()
            if val > best_move_val:
                best_move_val = val
                best_move = move
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
            self.board.pop() # unmake move

            # we found a move better than the best one found so far
            alpha = max(val, alpha)

            # prune if our opponent could force us into a worse move
            if alpha >= beta:
                break

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
                score = 0 
                piece_values = {
                    chess.PAWN: 100,
                    chess.KNIGHT: 300,
                    chess.BISHOP: 300,
                    chess.ROOK: 500,
                    chess.QUEEN: 900,
                    chess.KING: 1000,
                }
                PIECE_SQUARE_TABLES = {
                    chess.PAWN: [
                        0,  0,  0,  0,  0,  0,  0,  0,
                        50, 50, 50, 50, 50, 50, 50, 50,
                        10, 10, 20, 30, 30, 20, 10, 10,
                        5,  5, 10, 25, 25, 10,  5,  5,
                        0,  0,  0, 20, 20,  0,  0,  0,
                        5, -5,-10,  0,  0,-10, -5,  5,
                        5, 10, 10,-20,-20, 10, 10,  5,
                        0,  0,  0,  0,  0,  0,  0,  0
                    ],
                    chess.KNIGHT: [
                        -50,-40,-30,-30,-30,-30,-40,-50,
                        -40,-20,  0,  0,  0,  0,-20,-40,
                        -30,  0, 10, 15, 15, 10,  0,-30,
                        -30,  5, 15, 20, 20, 15,  5,-30,
                        -30,  0, 15, 20, 20, 15,  0,-30,
                        -30,  5, 10, 15, 15, 10,  5,-30,
                        -40,-20,  0,  5,  5,  0,-20,-40,
                        -50,-40,-30,-30,-30,-30,-40,-50
                    ],
                    chess.BISHOP: [
                        -20,-10,-10,-10,-10,-10,-10,-20,
                        -10,  0,  0,  0,  0,  0,  0,-10,
                        -10,  0,  5, 10, 10,  5,  0,-10,
                        -10,  5,  5, 10, 10,  5,  5,-10,
                        -10,  0, 10, 10, 10, 10,  0,-10,
                        -10, 10, 10, 10, 10, 10, 10,-10,
                        -10,  5,  0,  0,  0,  0,  5,-10,
                        -20,-10,-10,-10,-10,-10,-10,-20
                    ],
                    chess.ROOK: [
                        0,  0,  0,  0,  0,  0,  0,  0,
                        5, 10, 10, 10, 10, 10, 10,  5,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        -5,  0,  0,  0,  0,  0,  0, -5,
                        0,  0,  0,  5,  5,  0,  0,  0
                    ],
                    chess.QUEEN: [
                        -20,-10,-10, -5, -5,-10,-10,-20,
                        -10,  0,  0,  0,  0,  0,  0,-10,
                        -10,  0,  5,  5,  5,  5,  0,-10,
                        -5,  0,  5,  5,  5,  5,  0, -5,
                        0,  0,  5,  5,  5,  5,  0, -5,
                        -10,  5,  5,  5,  5,  5,  0,-10,
                        -10,  0,  5,  0,  0,  0,  0,-10,
                        -20,-10,-10, -5, -5,-10,-10,-20
                    ],
                    chess.KING: [
                        -30,-40,-40,-50,-50,-40,-40,-30,
                        -30,-40,-40,-50,-50,-40,-40,-30,
                        -30,-40,-40,-50,-50,-40,-40,-30,
                        -30,-40,-40,-50,-50,-40,-40,-30,
                        -20,-30,-30,-40,-40,-30,-30,-20,
                        -10,-20,-20,-20,-20,-20,-20,-10,
                        20, 20,  0,  0,  0,  0, 20, 20,
                        20, 30, 10,  0,  0, 10, 30, 20
                    ]
                }
                
                score = 0
                for piece_type in chess.PIECE_TYPES:
                    white_squares = self.board.pieces(piece_type, chess.WHITE)
                    black_squares = self.board.pieces(piece_type, chess.BLACK)

                    material_value = piece_values[piece_type]

                    for square in white_squares:
                        # we mirror the square because python-chess puts A1 at 0, and would make our piece
                        # square tables upside down if we didn't mirror it.
                        mirrored_square = chess.square_mirror(square)
                        score += material_value + PIECE_SQUARE_TABLES[piece_type][mirrored_square]

                    for square in black_squares:
                        score -= material_value + PIECE_SQUARE_TABLES[piece_type][square]

                    
                return score
