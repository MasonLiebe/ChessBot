class CastleRights:
    def __init__(self):
        self.kingside_rights = 255
        self.queenside_rights = 255
        self.castled = 0

    def can_player_castle_kingside(self, playernum):
        return (self.kingside_rights >> playernum) & 1 != 0

    def can_player_castle_queenside(self, playernum):
        return (self.queenside_rights >> playernum) & 1 != 0

    def can_player_castle(self, playernum):
        return self.can_player_castle_kingside(playernum) or self.can_player_castle_queenside(playernum)

    def did_player_castle(self, playernum):
        return (self.castled >> playernum) & 1 != 0

    def set_player_castled(self, playernum):
        self.castled |= 1 << playernum

    def disable_kingside_castle(self, playernum):
        self.kingside_rights &= ~(1 << playernum)

    def disable_queenside_castle(self, playernum):
        self.queenside_rights &= ~(1 << playernum)

# # Test cases
# if __name__ == "__main__":
#     test_rights = CastleRights()
#     print(test_rights.can_player_castle_queenside(0))
#     test_rights.disable_queenside_castle(0)
#     print(test_rights.can_player_castle_queenside(0))
#     print(test_rights.can_player_castle_kingside(0))
#     print(test_rights.can_player_castle(0))
#     test_rights.disable_kingside_castle(0)
#     print(test_rights.can_player_castle_kingside(0))
#     print(test_rights.can_player_castle(0))

