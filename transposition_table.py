from typing import List, Optional
from move import Move
from enum import Enum

TABLE_SIZE = 1_500_000
ENTRIES_PER_CLUSTER = 4

class EntryFlag(Enum):
    ALPHA = 0
    EXACT = 1
    BETA = 2
    NULL = 3

class Entry:
    def __init__(self, key: int, flag: EntryFlag, value: int, move_: Move, depth: int, ancient: bool):
        self.key = key
        self.flag = flag
        self.value = value
        self.move_ = move_
        self.depth = depth
        self.ancient = ancient

    @classmethod
    def null(cls) -> 'Entry':
        return cls(0, EntryFlag.NULL, 0, Move.null(), 0, True)

class Cluster:
    def __init__(self):
        self.entries: List[Entry] = [Entry.null() for _ in range(ENTRIES_PER_CLUSTER)]

class TranspositionTable:
    def __init__(self):
        self.data: List[Cluster] = [Cluster() for _ in range(TABLE_SIZE)]

    def set_ancient(self):
        for cluster in self.data:
            for entry in cluster.entries:
                entry.ancient = True

    def insert(self, zobrist_key: int, entry: Entry):
        cluster = self.data[zobrist_key % TABLE_SIZE]
        for i in range(len(cluster.entries)):
            tentry = cluster.entries[i]
            if tentry.depth <= entry.depth and tentry.key == zobrist_key and tentry.flag != EntryFlag.NULL:
                cluster.entries[i] = entry
                return

        lowest_depth_and_ancient = float('inf')
        lowest_depth_and_ancient_indx = -1
        lowest_depth = float('inf')
        lowest_depth_index = 0
        for i in range(ENTRIES_PER_CLUSTER):
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
        cluster = self.data[zobrist_key % TABLE_SIZE]
        for entry in cluster.entries:
            if entry.key == zobrist_key and entry.flag != EntryFlag.NULL:
                return entry
        return None