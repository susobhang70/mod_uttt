# AI for a variant of Ultimate TicTacToe

#### The Game
- Ultimate TicTacToe is an extension of the 3x3 TicTacToe, where there are `9 blocks` each having `3x3 cells`.
- Each game is between two teams.
- At the beginning, a coin is flipped to decide the team which will move first (First player).
- The marker for the `first player is ‘x’` and for the `second player is ‘o’`.
- The objective of the game is to win the board by making a legitimate pattern of the blocks.
- A `cell` would refer to any of the `81 smaller squares`.
- A `block` would refer to a `3x3 miniboard` composed of `9 cells`.

#### The rules
1. **[FIRST MOVE]** The very first move of the game is an open move, i.e. `Any cell` on the entire board is valid.
2. **[CORRESPONDENCE RULE]** If the opponent places his/her marker in any of the cells, except for the center cell of a block, then you need to place your marker anywhere in the `two blocks adjacent to the block corresponding to the cell`. For example, for the top left cell, the next player needs to move in center left and top center. Similarly for the right center cell, top right and bottom right blocks are open. Please refer to the code for more clarity.
3. **[CENTER RULE]** If the opponent places his/her marker in the `center cell` of any block, then you need to place your marker in the `center block` only.
4. **[FREE MOVE RULE]** In case the `all of the cells` in the destined blocks obtained from Rule 2 or Rule 3 are `occupied`, then the player may move in `any free cell in the entire board`.
5. **[ABANDON RULE]** Once a block is `won` by a player, it has to be abandoned. That is, you may consider the entire block to be full and `no other player may play` in that block.
6. **[WIN RULE]** The player who wins any three blocks which are either a `row`, `column` or `diagonal` of the board, `wins the game` and the game is over. If all the cells are filled, and `no pattern` has been formed then the `game is
over`.

#### Time Limit
A valid move needs to be returned from the `move` function within `12 seconds`. If the time exceeds 12 seconds for a particular move, then the match will be forfeited and the `opponent wins` by default.

#### To Play
- `python evaluator_code.py <option>`  
where `<option>` is one of the following integers:
  - **1** Random player vs AI - Random starts first
  - **2** Human vs. AI
  - **3** Human vs. Human
  - **4** AI vs. Random player - AI starts first
  - **5** AI vs NaiveAI - AI moves first
  - **6** NaiveAI vs AI - NaiveAI moves first
  - **7** AI1 vs AI2 - AI1 moves first
  - **8** AI vs OldAI - OldAI moves first
  - **9** AI vs OldAI - AI moves first
  - **10** 27 vs 64 - 64 moves first
  - **11** 27 vs 64 - 27 moves first

#### Code Highlights
- The code has been written in `Python` and is well documented.
- The `move` function is responsible for returning a valid move within `12 sec` and `time.time()` has been used for this.
- A valid move is returned after `Alpha-Beta` pruning is done on the `Minimax tree` and various board positions have been `scored`.
- There is no specific `Alpha-Beta Search Depth`. The full 12 seconds is utilized. This is possible becuase of an `Iterative Deepening Search` implementation.
- As a first step, all valid moves are generated and then `MIN` is called from the `move` function. `MIN` and `MAX` call each other interchangeabley until a `Terminal State` is reached. On reaching a terminal state, the board position is evaluated and scored according to various `heuristics` in `__eval_state`, `__evaluate_Mini_Board` and `score_big_board` functions.
- For various `heuristics` and `optimization` snippets, please read the well-documented code. It really is very interesting and we've worked really hard on implementing those rather smart heuristics.
- Our AI is contained in the file `team27.py`. Various other AI's used during testing have also been provided.



