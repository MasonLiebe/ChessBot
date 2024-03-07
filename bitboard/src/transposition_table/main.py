from enum import Enum
from typing import List, Optional

from bitboard.src.types.chess_move import Move

class EntryFlag(Enum):
    ALPHA = 1
    EXACT = 2
    BETA = 3
    NULL = 4

class Entry:
    def __init__(self, key: int, flag: EntryFlag, value: int, move_: Move, depth: int, ancient: bool):
        self.key = key
        self.flag = flag
        self.value = value
        self.move_ = move_
        self.depth = depth
        self.ancient = ancient

    @staticmethod
    def null():
        return Entry(0, EntryFlag.NULL, 0, Move.null(), 0, True)

class Cluster:
    def __init__(self):
        self.entries = [Entry.null() for _ in range(4)]

class TranspositionTable:
    TABLE_SIZE = 1_500_000

    def __init__(self):
        self.data = [Cluster() for _ in range(TranspositionTable.TABLE_SIZE)]

    def set_ancient(self):
        for cluster in self.data:
            for entry in cluster.entries:
                entry.ancient = True

    def insert(self, zobrist_key: int, entry: Entry):
        cluster = self.data[zobrist_key % TranspositionTable.TABLE_SIZE]
        for i, tentry in enumerate(cluster.entries):
            if tentry.depth <= entry.depth and tentry.key == zobrist_key and tentry.flag != EntryFlag.NULL:
                cluster.entries[i] = entry
                return

        lowest_depth_and_ancient = 255
        lowest_depth_and_ancient_indx = -1
        lowest_depth = 255
        lowest_depth_index = 0
        for i in range(4):
            if cluster.entries[i].ancient and cluster.entries[i].depth <= lowest_depth_and_ancient:
                lowest_depth_and_ancient = cluster.entries[i].depth
                lowest_depth_and_ancient_indx = i
            if cluster.entries[i].depth <= lowest_depth:
                lowest_depth = cluster.entries[i].depth
                lowest_depth_index = i

        if lowest_depth_and_ancient_indx != -1:
            cluster.entries[lowest_depth_and_ancient_indx] = entry
        else:
            cluster.entries[lowest_depth_index] = entry

    def retrieve(self, zobrist_key: int) -> Optional[Entry]:
        cluster = self.data[zobrist_key % TranspositionTable.TABLE_SIZE]
        for entry in cluster.entries:
            if entry.key == zobrist_key and entry.flag != EntryFlag.NULL:
                return entry
        return None


