import unittest
from unittest import *
from .bitboard import Bitboard
from .piece import Piece, PieceType
from .move import *
from .position_properties import CastleRights, PositionProperties
from .position import Position
from engine.engine import Engine

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

class TestPositionProperties(unittest.TestCase):
    def setUp(self):
        self.position_properties = PositionProperties()
    
    def test_initial_state(self):
        self.assertEqual(self.position_properties.en_passant_target, 0)
        self.assertEqual(self.position_properties.castle_rights.kingside_rights, 255)
        self.assertEqual(self.position_properties.castle_rights.queenside_rights, 255)
        self.assertEqual(self.position_properties.castle_rights.castled, 0)
        self.assertIsNone(self.position_properties.move_played)
        self.assertIsNone(self.position_properties.promote_from)
        self.assertIsNone(self.position_properties.captured_piece)
        self.assertIsNone(self.position_properties.prev_properties)

class TestFENPositions(unittest.TestCase):
    def setUp(self):
        self.engine = Engine.default()
    def test_starting_pos(self):
        self.assertEqual(self.engine.perft(1), 20)
        self.assertEqual(self.engine.perft(2), 400)
        self.assertEqual(self.engine.perft(3), 8902)
        self.assertEqual(self.engine.perft(4), 197281)
        self.assertEqual(self.engine.perft(5), 4865609)

    def test_kiwipete(self):
        self.engine.current_position = Position.from_fen("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - ")
        self.assertEqual(self.engine.perft(1), 48)
        self.assertEqual(self.engine.perft(2), 2039)
        self.assertEqual(self.engine.perft(3), 97862)
        self.assertEqual(self.engine.perft(4), 4085603)
        self.assertEqual(self.engine.perft(5), 193690690)

    def test_pos3(self):
        self.engine.current_position = Position.from_fen("8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - ")
        self.assertEqual(self.engine.perft(1), 14)
        self.assertEqual(self.engine.perft(2), 191)
        self.assertEqual(self.engine.perft(3), 2812)
        self.assertEqual(self.engine.perft(4), 43238)
        self.assertEqual(self.engine.perft(5), 674624)

    def test_pos4(self):
        self.engine.current_position = Position.from_fen("r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1")
        self.assertEqual(self.engine.perft(1), 6)
        self.assertEqual(self.engine.perft(2), 264)
        self.assertEqual(self.engine.perft(3), 9467)
        self.assertEqual(self.engine.perft(4), 422333)
        self.assertEqual(self.engine.perft(5), 15833292)

    def test_pos5(self):
        self.engine.current_position = Position.from_fen("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8")
        self.assertEqual(self.engine.perft(1), 44)
        self.assertEqual(self.engine.perft(2), 1486)
        self.assertEqual(self.engine.perft(3), 62379)
        self.assertEqual(self.engine.perft(4), 2103487)
        self.assertEqual(self.engine.perft(5), 89941194)

    def test_pos6(self):
        self.engine.current_position = Position.from_fen("r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10")
        self.assertEqual(self.engine.perft(1), 46)
        self.assertEqual(self.engine.perft(2), 2079)
        self.assertEqual(self.engine.perft(3), 89890)
        self.assertEqual(self.engine.perft(4), 3894594)
        self.assertEqual(self.engine.perft(5), 164075551)

if __name__ == '__main__':
    unittest.main()


if __name__ == '__main__':
    unittest.main()