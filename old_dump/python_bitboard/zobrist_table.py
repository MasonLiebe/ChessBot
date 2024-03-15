from piece import PieceType, Piece
import random
from collections import defaultdict
from constants import *

class ZobristTable:
    def __init__(self):
        self.rng = random.Random(5435651169991665628)
        self.ep_zobrist = [self.rng.getrandbits(64) for _ in range(17)]
        self.zobrist = [[self._generate_randoms(256) for _ in range(13)] for _ in range(2)] # 2 players, 13 piece types, 256 squares
        self.to_move = self.rng.getrandbits(64)
        self.w_q_castle = self.rng.getrandbits(64)
        self.b_q_castle = self.rng.getrandbits(64)
        self.w_k_castle = self.rng.getrandbits(64)
        self.b_k_castle = self.rng.getrandbits(64)

    def _generate_randoms(self, count):
        # Generates the random numbers for the piece/square combinations
        return [self.rng.getrandbits(64) for _ in range(count)]

    def get_to_move_zobrist(self, player_num):
        # returns the zobrist signature for the player to move
        if player_num == 0:
            return self.to_move
        else:
            return 0

    def get_castling_zobrist(self, player_num, kingside):
        # returns the zobrist signature for the castling rights
        if player_num == 0:
            return self.w_k_castle if kingside else self.w_q_castle
        elif player_num == 1:
            return self.b_k_castle if kingside else self.b_q_castle
        else:
            return 0

    def get_zobrist_sq_from_pt(self, pt, owner, index):
        # returns the zobrist signature for the piece at the given square
        # pt is a string 'King', 'Queen', etc.
        # regardless if the piece is there or not=
        if pt in PIECE_TO_INT:
            return self.zobrist[owner][PIECE_TO_INT[pt] - 1][index] # piece ints are 1-indexed
        else:
            return 0

    def get_zobrist_sq(self, piece, index):
        # returns the zobrist signature for the piece at the given square
        # piece is a Piece object
        return self.get_zobrist_sq_from_pt(piece.piece_type, piece.player_num, index)

    def get_zobrist_piece(self, piece, owner):
        # returns the zobrist signature for the entire piece 
        # for each entry in the piece's bitboard, it xors the zobrist signature for that square
        # if the piece is in that square
        output_zobrist = 0
        # iterate through all indices and test if the piece is there

        for index in range(256):
            if piece.bitboard.get_index(index):
                output_zobrist ^= self.zobrist[owner][INT_TO_PIECE[piece.piece_type - 1]][index]  # piece ints are 1-indexed
        return output_zobrist

    def get_ep_zobrist_file(self, rank):
        return self.ep_zobrist[rank]
    