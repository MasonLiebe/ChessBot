from piece import PieceType, Piece
import random
from collections import defaultdict

class ZobristTable:
    def __init__(self):
        self.rng = random.Random(5435651169991665628)
        self.ep_zobrist = [self.rng.getrandbits(64) for _ in range(17)]
        self.zobrist = [[self._generate_randoms(256) for _ in range(6)] for _ in range(2)]
        self.custom_zobrist = defaultdict(list)
        self.white_to_move = self.rng.getrandbits(64)
        self.w_q_castle = self.rng.getrandbits(64)
        self.b_q_castle = self.rng.getrandbits(64)
        self.w_k_castle = self.rng.getrandbits(64)
        self.b_k_castle = self.rng.getrandbits(64)

    def _generate_randoms(self, count):
        return [self.rng.getrandbits(64) for _ in range(count)]

    def get_to_move_zobrist(self, player_num):
        return self.white_to_move

    def get_castling_zobrist(self, player_num, kingside):
        if player_num == 0:
            return self.w_k_castle if kingside else self.w_q_castle
        elif player_num == 1:
            return self.b_k_castle if kingside else self.b_q_castle
        else:
            return 0

    def get_zobrist_sq_from_pt(self, pt, owner, index):
        piece_type_mapping = {
            'King': 0,
            'Queen': 1,
            'Rook': 2,
            'Bishop': 3,
            'Knight': 4,
            'Pawn': 5,
            'Custom1': 6,
            'Custom2': 7,
            'Custom3': 8,
            'Custom4': 9,
            'Custom5': 10,
            'Custom6': 11,
        }
        if pt in piece_type_mapping:
            return self.zobrist[owner][piece_type_mapping[pt]][index]
        else:  # Custom piece type
            key = (owner, pt)
            if key not in self.custom_zobrist:
                return 0
            return self.custom_zobrist[key][index]

    def get_zobrist_sq(self, piece, index):
        return self.get_zobrist_sq_from_pt(piece.piece_type, piece.player_num, index)

    def get_ep_zobrist_file(self, rank):
        return self.ep_zobrist[rank]

    def register_piecetype(self, player_num, pt):
        self.custom_zobrist[(player_num, pt)] = self._generate_randoms(256)