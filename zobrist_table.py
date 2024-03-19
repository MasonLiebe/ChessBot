import random
from typing import Dict, List, Tuple
from piece import Piece, PieceType

class ZobristTable:
    def __init__(self):
        self.rng = random.Random(5435651169991665628)
        self.ep_zobrist = [self.rng.getrandbits(64) for _ in range(17)]
        self.zobrist = [[] for _ in range(2)]
        for i in range(2):
            for j in range(6):
                randoms = [self.rng.getrandbits(64) for _ in range(256)]
                self.zobrist[i].append(randoms)
        self.custom_zobrist: Dict[Tuple[int, PieceType], List[int]] = {}
        self.white_to_move = self.rng.getrandbits(64)
        self.w_q_castle = self.rng.getrandbits(64)
        self.b_q_castle = self.rng.getrandbits(64)
        self.w_k_castle = self.rng.getrandbits(64)
        self.b_k_castle = self.rng.getrandbits(64)

    def get_to_move_zobrist(self, player_num: int) -> int:
        return self.white_to_move

    def get_castling_zobrist(self, player_num: int, kingside: bool) -> int:
        if player_num == 0 and kingside:
            return self.w_k_castle
        elif player_num == 0 and not kingside:
            return self.w_q_castle
        elif player_num == 1 and kingside:
            return self.b_k_castle
        elif player_num == 1 and not kingside:
            return self.b_q_castle
        else:
            return 0

    def get_zobrist_sq_from_pt(self, pt: PieceType, owner: int, index: int) -> int:
        if pt == PieceType.King:
            return self.zobrist[owner][0][index]
        elif pt == PieceType.Queen:
            return self.zobrist[owner][1][index]
        elif pt == PieceType.Rook:
            return self.zobrist[owner][2][index]
        elif pt == PieceType.Bishop:
            return self.zobrist[owner][3][index]
        elif pt == PieceType.Knight:
            return self.zobrist[owner][4][index]
        elif pt == PieceType.Pawn:
            return self.zobrist[owner][5][index]
        else:
            if (owner, pt) not in self.custom_zobrist:
                return 0
            return self.custom_zobrist[(owner, pt)][index]

    def get_zobrist_sq(self, piece: Piece, index: int) -> int:
        return self.get_zobrist_sq_from_pt(piece.piece_type, piece.player_num, index)

    def get_ep_zobrist_file(self, rank: int) -> int:
        return self.ep_zobrist[rank]

    def register_piecetype(self, player_num: int, pt: PieceType):
        randoms = self._make_randoms()
        self.custom_zobrist[(player_num, pt)] = randoms

    def _make_randoms(self) -> List[int]:
        return [self.rng.getrandbits(64) for _ in range(256)]