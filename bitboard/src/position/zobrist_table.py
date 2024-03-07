import random
from enum import Enum
from collections import defaultdict
from bitboard.src.types.mod import PieceType
from bitboard.src.position.piece import Piece


class ZobristTable:
    def __init__(self):
        self.rng = random.Random(5435651169991665628)
        self.ep_zobrist = [self.rng.getrandbits(64) for _ in range(17)]
        self.zobrist = [[[self.rng.getrandbits(64) for _ in range(256)] for _ in range(6)] for _ in range(2)]
        self.custom_zobrist = defaultdict(list)
        self.white_to_move = self.rng.getrandbits(64)
        self.w_q_castle = self.rng.getrandbits(64)
        self.b_q_castle = self.rng.getrandbits(64)
        self.w_k_castle = self.rng.getrandbits(64)
        self.b_k_castle = self.rng.getrandbits(64)

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
        if pt == PieceType.Custom:
            return self.custom_zobrist[(owner, pt)][index]
        else:
            return self.zobrist[owner][pt.value][index]

    def get_zobrist_sq(self, piece, index):
        return self.get_zobrist_sq_from_pt(piece.piece_type, piece.player_num, index)

    def get_ep_zobrist_file(self, rank):
        return self.ep_zobrist[rank]

    def register_piecetype(self, player_num, pt):
        randoms = [self.rng.getrandbits(64) for _ in range(256)]
        self.custom_zobrist[(player_num, pt)] = randoms


