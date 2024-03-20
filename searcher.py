from move import Move, MoveType
from position import Position
from move_generator import MoveGenerator
from evaluator import Evaluator
from transposition_table import TranspositionTable, Entry, EntryFlag
from datetime import datetime as instant
from typing import Optional


class Searcher:
    def __init__(self):
        self.transposition_table = TranspositionTable()
        self.killer_moves = [[Move.null(), Move.null()] for _ in range(64)]
        self.history_moves = [[0] * 256 for _ in range(256)]
        self.nodes_searched = 0
        self.nodes_fail_high_first = 0
        self.nodes_fail_high = 0

    def get_best_move(self, position: Position, eval: Evaluator, movegen: MoveGenerator, depth: int) -> Move:
        self.clear_heuristics()
        self.transposition_table.set_ancient()
        for d in range(1, depth + 1):
            alpha = -float('inf')
            beta = float('inf')
            best_score = self.alphabeta(position, eval, movegen, d, alpha, beta, True)

            ordering_percentage = (self.nodes_fail_high_first / self.nodes_fail_high) if self.nodes_fail_high != 0 else 0.0
            print(f"score:{best_score} depth: {d}, nodes: {self.nodes_searched}, ordering: {ordering_percentage}")

            self.clear_search_stats()

        entry = self.transposition_table.retrieve(position.get_zobrist())
        return entry.move_ if entry else None

    def get_best_move_timeout(self, position: Position, eval: Evaluator, movegen: MoveGenerator, time_sec: int) -> (Move, int):
        self.clear_heuristics()
        self.transposition_table.set_ancient()
        d = 1
        start = instant.now()
        max_time = instant.duration(seconds=time_sec)
        while True:
            if start.elapsed() >= max_time:
                break

            alpha = -float('inf')
            beta = float('inf')
            best_score = self.alphabeta(position, eval, movegen, d, alpha, beta, True)

            ordering_percentage = (self.nodes_fail_high_first / self.nodes_fail_high) if self.nodes_fail_high != 0 else 0.0
            print(f"score:{best_score} depth: {d}, nodes: {self.nodes_searched}, ordering: {ordering_percentage}")

            self.clear_search_stats()
            d += 1

        entry = self.transposition_table.retrieve(position.get_zobrist())
        return (entry.move_, d) if entry else None

    def alphabeta(self, position: Position, eval: Evaluator, movegen: MoveGenerator,
                  depth: int, alpha: int, beta: int, do_null: bool) -> int:
        self.nodes_searched += 1

        if depth <= 0:
            return self.quiesce(position, eval, movegen, 0, alpha, beta)

        is_pv = alpha != beta - 1
        entry = self.transposition_table.retrieve(position.get_zobrist())
        if entry and entry.depth >= depth:
            if entry.flag == EntryFlag.EXACT:
                if entry.value < alpha:
                    return alpha
                if entry.value >= beta:
                    return beta
                return entry.value
            elif entry.flag == EntryFlag.BETA:
                if not is_pv and beta <= entry.value:
                    return beta
            elif entry.flag == EntryFlag.ALPHA:
                if not is_pv and alpha >= entry.value:
                    return alpha

        if not is_pv:
            beta_result = self.try_null_move(position, eval, movegen, depth, alpha, beta, do_null)
            if beta_result is not None:
                return beta_result

        moves_and_score = self.get_scored_pseudo_moves(eval, movegen, position, depth)
        best_move = Move.null()
        num_legal_moves = 0
        old_alpha = alpha
        best_score = -float('inf')
        in_check = movegen.in_check(position)
        for i in range(len(moves_and_score)):
            Searcher.sort_moves(i, moves_and_score)
            move_ = moves_and_score[i][1]

            if not movegen.is_move_legal(move_, position):
                continue

            num_legal_moves += 1
            position.make_move(move_)
            if num_legal_moves == 1:
                score = -self.alphabeta(position, eval, movegen, depth - 1, -beta, -alpha, True)
            else:
                if num_legal_moves > 4 and move_.get_move_type() == MoveType.Quiet and not is_pv and depth >= 5 and not in_check:
                    reduced_depth = depth - 2
                    if num_legal_moves > 10:
                        reduced_depth = depth - 3
                    score = -self.alphabeta(position, eval, movegen, reduced_depth, -alpha - 1, -alpha, True)
                else:
                    score = alpha + 1

                if score > alpha:
                    score = -self.alphabeta(position, eval, movegen, depth - 1, -alpha - 1, -alpha, True)
                    if score > alpha and score < beta:
                        score = -self.alphabeta(position, eval, movegen, depth - 1, -beta, -alpha, True)

            position.unmake_move()

            if score > best_score:
                best_score = score
                best_move = move_

                if score > alpha:
                    if score >= beta:
                        if num_legal_moves == 1:
                            self.nodes_fail_high_first += 1
                        self.nodes_fail_high += 1
                        self.update_killers(depth, move_)
                        self.transposition_table.insert(position.get_zobrist(), Entry(
                            key=position.get_zobrist(),
                            flag=EntryFlag.BETA,
                            value=beta,
                            move_=move_,
                            depth=depth,
                            ancient=False
                        ))
                        return beta
                    alpha = score

                    self.update_history_heuristic(depth, move_)

        if num_legal_moves == 0:
            return -99999 if movegen.in_check(position) else 0

        if alpha != old_alpha:
            self.transposition_table.insert(position.get_zobrist(), Entry(
                key=position.get_zobrist(),
                flag=EntryFlag.EXACT,
                value=best_score,
                move_=best_move,
                depth=depth,
                ancient=False
            ))
        else:
            self.transposition_table.insert(position.get_zobrist(), Entry(
                key=position.get_zobrist(),
                flag=EntryFlag.ALPHA,
                value=alpha,
                move_=best_move,
                depth=depth,
                ancient=False
            ))
        return alpha

    def quiesce(self, position: Position, eval: Evaluator, movegen: MoveGenerator,
                depth: int, alpha: int, beta: int) -> int:
        self.nodes_searched += 1
        score = eval.evaluate(position, movegen)
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score

        best_move = Move.null()
        num_legal_moves = 0
        moves_and_score = self.get_scored_capture_moves(eval, movegen, position, depth)
        for i in range(len(moves_and_score)):
            Searcher.sort_moves(i, moves_and_score)
            move_ = moves_and_score[i][1]

            if not movegen.is_move_legal(move_, position):
                continue

            num_legal_moves += 1
            position.make_move(move_)
            score = -self.quiesce(position, eval, movegen, depth, -beta, -alpha)
            position.unmake_move()

            if score >= beta:
                if num_legal_moves == 1:
                    self.nodes_fail_high_first += 1
                self.nodes_fail_high += 1
                return beta
            if score > alpha:
                alpha = score
                best_move = move_

        return alpha

    @staticmethod
    def sort_moves(current_index: int, moves: list):
        best_score = 0
        best_score_index = current_index
        for i in range(current_index, len(moves)):
            score = moves[i][0]
            if score >= best_score:
                best_score = score
                best_score_index = i
        if current_index != best_score_index:
            moves[current_index], moves[best_score_index] = moves[best_score_index], moves[current_index]

    def clear_heuristics(self):
        for i in range(len(self.killer_moves)):
            for j in range(len(self.killer_moves[i])):
                self.killer_moves[i][j] = Move.null()
        for i in range(len(self.history_moves)):
            for j in range(len(self.history_moves[i])):
                self.history_moves[i][j] = 0

    def clear_search_stats(self):
        self.nodes_searched = 0
        self.nodes_fail_high_first = 0
        self.nodes_fail_high = 0

    def update_killers(self, depth: int, move_: Move):
        if not move_.get_is_capture():
            if move_ != self.killer_moves[depth][0] and move_ != self.killer_moves[depth][1]:
                self.killer_moves[depth][1] = self.killer_moves[depth][0]
                self.killer_moves[depth][0] = move_

    def update_history_heuristic(self, depth: int, move_: Move):
        if not move_.get_is_capture():
            self.history_moves[move_.get_from()][move_.get_to()] += depth

    def get_scored_pseudo_moves(self, eval: Evaluator, movegen: MoveGenerator, position: Position, depth: int) -> list:
        moves_and_score = [(eval.score_move(depth, self.history_moves, self.killer_moves, position, mv), mv) for mv in movegen.get_pseudo_moves(position)]

        entry = self.transposition_table.retrieve(position.get_zobrist())
        if entry:
            best_move = entry.move_
            for i in range(len(moves_and_score)):
                if moves_and_score[i][1] == best_move:
                    moves_and_score[i] = (float('inf'), moves_and_score[i][1])
                    break

        return moves_and_score

    def get_scored_capture_moves(self, eval: Evaluator, movegen: MoveGenerator, position: Position, depth: int) -> list:
        moves_and_score = [(eval.score_move(depth, self.history_moves, self.killer_moves, position, mv), mv) for mv in movegen.get_capture_moves(position)]

        entry = self.transposition_table.retrieve(position.get_zobrist())
        if entry:
            best_move = entry.move_
            for i in range(len(moves_and_score)):
                if moves_and_score[i][1] == best_move:
                    moves_and_score[i] = (float('inf'), moves_and_score[i][1])
                    break

        return moves_and_score

    def try_null_move(self, position: Position, eval: Evaluator, movegen: MoveGenerator,
                      depth: int, alpha: int, beta: int, do_null: bool) -> Optional[int]:
        if do_null:
            if depth > 3 and eval.can_do_null_move(position) and not movegen.in_check(position):
                position.make_move(Move.null())
                nscore = -self.alphabeta(position, eval, movegen, depth - 3, -beta, -beta + 1, False)
                position.unmake_move()
                if nscore >= beta:
                    return beta
        return None