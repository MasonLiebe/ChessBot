# chessBot
This is a complete chess app that allows for 2-player and 1-player chess options with the best chess bot I could come up with using a mix of personal and publicly available ideas

Aside from the mundane GUI, board representation, and game state handling features, here are the goals.

Original Bitboard Architecture that will allow for custom game structures, rules, and custom pieces.
 - Self Capture Chess
 - No-Castle Chess
 - User-Created Custom Pieces
 - Custom starting positions and Board Sizes

Chess Bot that will efficiently evaluate positions and suggest moves based on the following techinques:

- Zobrist Hashing
- Transposition Tables
- Principal Variation Search using Iterative Deepening
- Quiescence search
- History Heuristic
- Killer Heuristic
- Null-move pruning

For static evaluation, the bot will use static material scoring for board, then multipliers that adjust different piece's score contributions based on their placement on the board (for example, knights are worth more in the center of the board than in the corner, pawns are worth more when they are nearing promotion, etc.).

