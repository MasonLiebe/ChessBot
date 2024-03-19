import unittest
from bitboard import Bitboard
from piece import Piece, PieceType
from move import *
from position_properties import CastleRights, PositionProperties

class TestPiece(unittest.TestCase):
    def test_blank_custom(self):
        piece = Piece.blank_custom(1, 'x')
        self.assertEqual(piece.player_num, 1)
        self.assertEqual(piece.char_rep, 'x')
        self.assertEqual(piece.piece_type, 'x')
        self.assertEqual(piece.bitboard, Bitboard.zero())

    def test_blank_pawn(self):
        piece = Piece.blank_pawn(2)
        self.assertEqual(piece.player_num, 2)
        self.assertEqual(piece.char_rep, 'p')
        self.assertEqual(piece.piece_type, PieceType.Pawn)
        self.assertEqual(piece.bitboard, Bitboard.zero())

    def test_blank_knight(self):
        piece = Piece.blank_knight(1)
        self.assertEqual(piece.player_num, 1)
        self.assertEqual(piece.char_rep, 'n')
        self.assertEqual(piece.piece_type, PieceType.Knight)
        self.assertEqual(piece.bitboard, Bitboard.zero())

    def test_blank_king(self):
        piece = Piece.blank_king(2)
        self.assertEqual(piece.player_num, 2)
        self.assertEqual(piece.char_rep, 'k')
        self.assertEqual(piece.piece_type, PieceType.King)
        self.assertEqual(piece.bitboard, Bitboard.zero())

    def test_blank_rook(self):
        piece = Piece.blank_rook(1)
        self.assertEqual(piece.player_num, 1)
        self.assertEqual(piece.char_rep, 'r')
        self.assertEqual(piece.piece_type, PieceType.Rook)
        self.assertEqual(piece.bitboard, Bitboard.zero())

    def test_blank_bishop(self):
        piece = Piece.blank_bishop(2)
        self.assertEqual(piece.player_num, 2)
        self.assertEqual(piece.char_rep, 'b')
        self.assertEqual(piece.piece_type, PieceType.Bishop)
        self.assertEqual(piece.bitboard, Bitboard.zero())

    def test_blank_queen(self):
        piece = Piece.blank_queen(1)
        self.assertEqual(piece.player_num, 1)
        self.assertEqual(piece.char_rep, 'q')
        self.assertEqual(piece.piece_type, PieceType.Queen)
        self.assertEqual(piece.bitboard, Bitboard.zero())

class TestMove(unittest.TestCase):
    def test_new(self):
        move = Move.new(0, 1, 2, 'Capture', 'q')
        self.assertEqual(move.get_from(), 0)
        self.assertEqual(move.get_to(), 1)
        self.assertEqual(move.get_target(), 2)
        self.assertEqual(move.get_move_type(), 'Capture')
        self.assertEqual(move.get_promotion_char(), 'q')

    def test_null(self):
        move = Move.null()
        self.assertEqual(move.get_from(), 0)
        self.assertEqual(move.get_to(), 0)
        self.assertEqual(move.get_target(), 0)
        self.assertEqual(move.get_move_type(), 'Null')
        self.assertIsNone(move.get_promotion_char())

    def test_get_is_capture(self):
        move = Move.new(0, 1, 2, 'Capture', None)
        self.assertTrue(move.get_is_capture())

        move = Move.new(0, 1, 2, 'Quiet', None)
        self.assertFalse(move.get_is_capture())

    def test_equality(self):
        move1 = Move.new(0, 1, 2, 'Capture', 'q')
        move2 = Move.new(0, 1, 2, 'Capture', 'q')
        move3 = Move.new(0, 1, 2, 'Quiet', 'q')

        self.assertEqual(move1, move2)
        self.assertNotEqual(move1, move3)

    def test_str(self):
        move = Move.new(0, 1, 2, 'Capture', 'q')
        expected_str = "(from: A1, to:B1)"
        self.assertEqual(str(move), expected_str)

class TestCastleRights(unittest.TestCase):
    def setUp(self):
        self.castle_rights = CastleRights()

    def test_initial_state(self):
        self.assertEqual(self.castle_rights.kingside_rights, 255)
        self.assertEqual(self.castle_rights.queenside_rights, 255)
        self.assertEqual(self.castle_rights.castled, 0)

    def test_can_player_castle_kingside(self):
        self.assertTrue(self.castle_rights.can_player_castle_kingside(0))
        self.assertTrue(self.castle_rights.can_player_castle_kingside(7))
        self.castle_rights.disable_kingside_castle(0)
        self.assertFalse(self.castle_rights.can_player_castle_kingside(0))
        self.assertTrue(self.castle_rights.can_player_castle_kingside(7))

    def test_can_player_castle_queenside(self):
        self.assertTrue(self.castle_rights.can_player_castle_queenside(0))
        self.assertTrue(self.castle_rights.can_player_castle_queenside(7))
        self.castle_rights.disable_queenside_castle(0)
        self.assertFalse(self.castle_rights.can_player_castle_queenside(0))
        self.assertTrue(self.castle_rights.can_player_castle_queenside(7))

    def test_can_player_castle(self):
        self.assertTrue(self.castle_rights.can_player_castle(0))
        self.assertTrue(self.castle_rights.can_player_castle(7))
        self.castle_rights.disable_kingside_castle(0)
        self.assertTrue(self.castle_rights.can_player_castle(0))
        self.castle_rights.disable_queenside_castle(0)
        self.assertFalse(self.castle_rights.can_player_castle(0))
        self.assertTrue(self.castle_rights.can_player_castle(7))

    def test_did_player_castle(self):
        self.assertFalse(self.castle_rights.did_player_castle(0))
        self.assertFalse(self.castle_rights.did_player_castle(7))
        self.castle_rights.set_player_castled(0)
        self.assertTrue(self.castle_rights.did_player_castle(0))
        self.assertFalse(self.castle_rights.did_player_castle(7))

    def test_set_player_castled(self):
        self.castle_rights.set_player_castled(0)
        self.assertTrue(self.castle_rights.did_player_castle(0))
        self.assertFalse(self.castle_rights.did_player_castle(1))
        self.castle_rights.set_player_castled(7)
        self.assertTrue(self.castle_rights.did_player_castle(0))
        self.assertTrue(self.castle_rights.did_player_castle(7))

    def test_disable_kingside_castle(self):
        self.castle_rights.disable_kingside_castle(0)
        self.assertFalse(self.castle_rights.can_player_castle_kingside(0))
        self.assertTrue(self.castle_rights.can_player_castle_kingside(1))

    def test_disable_queenside_castle(self):
        self.castle_rights.disable_queenside_castle(0)
        self.assertFalse(self.castle_rights.can_player_castle_queenside(0))
        self.assertTrue(self.castle_rights.can_player_castle_queenside(1))

if __name__ == '__main__':
    unittest.main()