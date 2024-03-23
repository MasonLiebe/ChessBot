# CustomChess

CustomChess is a comprehensive chess application that offers both 2-player and 1-player chess options, featuring a highly capable chess bot. Although written in Python, which is not typically optimal for chess engines, this bot employs a combination of personal and publicly available ideas, along with various search optimizations, to greatly reduce the number of nodes searched when suggesting moves. The primary objective here is to showcase the power of creative algorithms in enhancing search performance with a prototype, rather than building a hyper efficient architecture-optimized engine like Stockfish.  Additionally, it does not employ any opening book or endgame tablebase, so it is not optimized at all for standard chess.  That being said, it is capable of playing standard chess at a 2000+ ELO level.  In the future, I think a port of this into a more suitable low-level language would be very interesting!

Features of CustomChess include:

- **Graphical User Interface (GUI):** A straightforward and functional interface allowing seamless interaction with the game. (IN PROGRESS)
- **Board Representation & Game State Management:** Robust under-the-hood mechanics ensuring accurate game play and state tracking.
- **Original Bitboard Architecture:** Supports custom game structures, rules, and uniquely crafted chess pieces, enhancing the traditional chess experience. Due to a lack of strong options for handeling 256-bit unsigned integers, this involves a custom class to represent and handle all of the operations.  This is a major efficiency painpoint and a future optimization possibility.
  - **User-Created Custom Pieces:** Players can design and introduce their own pieces into the game, adding a personalized touch.
  - **Custom Starting Positions and Board Sizes:** Tailor the board to fit your strategy or preference, breaking the confines of the 8x8 grid.

The heart of CustomChess is its Chess Bot, which boasts efficient position evaluation and move suggestion capabilities st through the implementation of advanced techniques such as:

- **Zobrist Hashing and Transposition Tables:** For efficient position recognition and redundant evaluation avoidance.
- **Principal Variation Search with Iterative Deepening:** Balancing depth and breadth search to identify the best moves.
- **Quiescence Search:** To ensure that only positions at 'quiet' states are evaluated, avoiding the horizon effect.
- **History and Killer Heuristics:** For move ordering optimization, reducing the search space by an average of 75%.
- **Null-move Pruning:** To reduce search depth under certain conditions without missing critical moves.

For position evaluation, the bot employs a nuanced scoring system. It begins with static material scoring and then applies multipliers to adjust the value contributions of pieces based on their board positions. This evaluation strategy recognizes the tactical significance of piece placement, such as knights being more valuable in the center than at the edges, and pawns increasing in value as they approach promotion.

Moreover, CustomChess introduces an innovative approach to evaluating custom pieces by estimating their centipawn value and positional multipliers. This estimation leverages published research on the relative value of specific piece capabilities determined by AlphaZero, accessible [here](https://arxiv.org/pdf/2009.04374.pdf).

![v2200](https://github.com/MasonLiebe/ChessBot/assets/149519733/1884a189-2226-43b3-8655-bcd85e2f0372)

CustomChess vs. 2200-Rated Noam on Chess.com

# What is Zobrist Hashing?

Zobrist Hashing is a technique employed in CustomChess to efficiently map unique board positions to specific hash values, facilitating rapid lookups and comparisons. This method is fundamental for enabling the chess engine to quickly recognize and evaluate repeated positions, thereby optimizing its decision-making process.

### Initialization

At the start of the program, we generate an extensive array of pseudorandom numbers, each assigned to distinct game features:

- A unique number for every possible placement of each chess piece on the board.
- A specific number to denote if the side to move is black.
- Four numbers to represent combinations of castling rights.
- Eight numbers to specify the file of a potential en passant square, acknowledging that pawns never appear on the first and last ranks, which allows for some array size reductions.

### Runtime Application

The Zobrist hash for any given board position is computed by performing an XOR operation between the random numbers corresponding to the features present in that position. This includes pieces on their respective squares, the side to move, castling rights, and potential en passant squares.

For example, the initial position's hash is derived by XORing the random values associated with each piece's starting square, the castling rights, and so forth. The beauty of the XOR operation lies in its reversibility—undoing an operation simply requires applying XOR with the same operand again. This property is particularly useful for chess engines, allowing them to quickly update hash keys during moves without needing to recompute the entire hash from scratch.

For instance, when a White Knight moves from b1 to c3 and captures a Black Bishop, the hash update involves:
- XORing out the Knight's original square and the captured Bishop's square.
- XORing in the Knight's new position and adjusting the side to move.

This incremental approach to updating the Zobrist hash allows CustomChess to efficiently track and evaluate board states, significantly enhancing its performance and strategic depth.

# Principle Variation Search (NegaScout)

Principal Variation Search (PVS), also known as "NegaScout," is an enhancement of the alpha-beta pruning algorithm. It is designed to reduce the number of nodes evaluated in the search tree, thereby speeding up the decision-making process of the chess engine. PVS exploits the fact that good moves are found more often by examining moves in their best-known order. By guessing the best move first, PVS attempts to narrow the search window with a minimal margin, performing a full-width search only when necessary.

### PVS Algorithm

The essence of the PVS algorithm is captured in the following pseudo-code, illustrating its recursive nature and how it differentiates between the search's first child node and subsequent nodes:

```
function pvs(node, depth, α, β, color) is
    if depth = 0 or node is a terminal node then
        return color × the heuristic value of node
    for each child of node do
        if child is the first child then
            score := −pvs(child, depth − 1, −β, −α, −color)
        else
            score := −pvs(child, depth − 1, −α − 1, −α, −color) (* search with a null window *)
            if α < score < β then
                score := −pvs(child, depth − 1, −β, −α, −color) (* if it failed high, do a full re-search *)
        α := max(α, score)
        if α ≥ β then
            break (* beta cut-off *)
    return α
```

# Quiescence Search (QS)

Quiescence Search is employed to avoid the "horizon effect" by extending the search depth for positions with potential tactical operations like captures or checks, ensuring that the evaluation of a position doesn't overlook imminent threats or opportunities. This algorithm helps in providing more accurate evaluations by continuing the search until a "quiet" position is reached, where a static evaluation becomes reliable. The following pseudocode outlines the basic structure of Quiescence Search integrated within a typical search routine:

```plaintext
function quiescence_search(node, depth) is
    if node appears quiet or node is a terminal node or depth = 0 then
        return estimated value of node
    else
        (recursively search node children with quiescence_search)
        return estimated value of children

function normal_search(node, depth) is
    if node is a terminal node then
        return estimated value of node
    else if depth = 0 then
        if node appears quiet then
            return estimated value of node
        else
            return estimated value from quiescence_search(node, reasonable_depth_value)
    else
        (recursively search node children with normal_search)
        return estimated value of children
```

Quiescence Search emulates human intuition in chess, allowing the engine to distinguish between moves requiring deeper investigation and those that can be evaluated as they stand. This differentiation ensures that the engine's move decisions are both efficient and tactically sound, enhancing its competitiveness and strategic depth.




