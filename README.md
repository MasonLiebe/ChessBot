# chessBot
This is a complete chess app that allows for 2-player and 1-player chess options with the best chess bot I could come up with using a mix of personal and publicly available ideas

Aside from the mundane GUI, board representation, and game state handling features, here are the cool things about this project.

Allows for custom game structures and custom pieces
 - Duck Chess
 - Self Capture Chess
 - No-Castle Chess
 - User-Created Custom Pieces
 - Custom starting positions
 - Chess 960

Even with all of these variations, it has some sort of bot implementation for any game.  No promises that the bot will be very strong though.
It is strongest with standard chess, as it has a tailored bot just for that, which implements an opening book of grandmaster games, then once it's out of book uses minimax search with alpha beta pruning to efficiently search for a move suggestion.

For static evaluation, the bot uses standard material scoring  (pawns worth a point, knights and bishops worth 3 points, rooks are 5 points, and queens 9 points), then multipliers that adjust different piece's score contributions based on their placement on the board (for example, knights are worth more in the center of the board than in the corner, pawns are worth more when they are nearing promotion, etc.).
