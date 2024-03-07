
class BitboardMoves:
    def __init__(self, enemies, moves, source_index, promotion_squares=None, promo_vals=None):
        self.enemies = enemies
        self.moves = moves
        self.source_index = source_index
        self.promotion_squares = promotion_squares
        self.promo_vals = promo_vals
        self.current_promo_vals = None

    def __iter__(self):
        return self

    def __next__(self):
        to = self.moves.lowest_one()
        if to is None:
            raise StopIteration
        promo_here = self.promotion_squares.bit(to) if self.promotion_squares else False
        capture_here = self.enemies.bit(to)
        if capture_here and promo_here:
            move_type = "PromotionCapture"
        elif capture_here:
            move_type = "Capture"
        elif promo_here:
            move_type = "Promotion"
        else:
            move_type = "Quiet"
        target = to if capture_here else 0
        promo_char = None
        if promo_here:
            if self.current_promo_vals is None:
                self.current_promo_vals = self.promo_vals.copy()
            promo_char = self.current_promo_vals.pop()
            if len(self.current_promo_vals) == 0:
                self.current_promo_vals = None
                self.moves.set_bit(to, False)
        else:
            self.moves.set_bit(to, False)
        return {'source_index': self.source_index, 'to': to, 'target': target, 'move_type': move_type, 'promo_char': promo_char}
