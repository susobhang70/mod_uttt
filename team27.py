import random
import copy					# For copy.deepcopy() 
import time     			# For timer functions

class Player27():
	'''This class and associated methods calculate the best move when move function is called by the game engine with the class object'''

	def __init__(self):
		'''Initializes the variables'''
		self.ALPHA_BETA_DEPTH = 6	# The depth of the search tree
		self.toggle = False			# toggle is used in generate_successor(). It is used to decide whether to place x or o in the current turn
		self.start_time = 0.0
		self.ALLOWED_TIME = 11.5	# Allowed time for each move
		self.freemoveflag = 0       # Flag to check if current move results in free move
		self.center_cells = [(1,1), (4,4), (7,7), (1,4), (1,7), (4,1), (4,7), (7,1), (7,4)]		# List of all center cells
		self.timedout = False		# To check whether a possible cell at the root level is fully evaluated

	def move(self, temp_board, temp_block, old_move, flag):
		'''Called by game engine. Calculates the best move for the player and returns. Big function due to avoid method call overhead (12 seconds time limit)'''
		# board: is the list of lists that represents the 9x9 grid
		# board[i] can be 'x', 'o' or '-'
		# block: is a list that represents if a block is won or available to play in
		# block[i] can be 'x', 'o' or '-' or 'D'
		# old_move: is a tuple of integers representing co-ordintates of the last move made. For the first move of game it is (-1,-1)
		# flag: is your marker. it can be 'x' or 'o'.
		# List of permitted blocks, based on old move.

		# If moving first, place in the centre of centre
		if(old_move[0] == -1 and old_move[1] == -1):
			return (4,4)

		# deepcopy the temp block to avoid changes to temp block
		new_temp_block = copy.deepcopy(temp_block)

		# Get list of empty valid cells
		blocks_allowed  = self.__get_valid_blocks(old_move, temp_block)
		cells = self.__get_valid_cells(temp_board, blocks_allowed, temp_block)

		# If only one move available, don't waste time further
		if(len(cells) == 1):
			return (cells[0][0], cells[0][1])

		next_moves = []
		old_next_moves = []

		if len(cells) in (1,2):
			self.ALPHA_BETA_DEPTH = 5	# If less number of choices, look deeper
		elif len(cells) in (3,4,5):
			self.ALPHA_BETA_DEPTH = 4
		elif len(cells) in (6,7):
			self.ALPHA_BETA_DEPTH = 3	# If more number of choices, look shallower
		else:
			self.ALPHA_BETA_DEPTH = 2	
		
		self.start_time = time.time()

		while True:
			if time.time() - self.start_time >= self.ALLOWED_TIME:
				break
			old_next_moves = copy.deepcopy(next_moves)
			next_moves = []
			minvalue = 0
			for cell in cells:
				self.toggle = False
				successor_board = self.generate_successor(temp_board, cell, flag)
				successor_block = self.__update_block(successor_board, new_temp_block, cell)

				# Calculates valid moves for opponent
				successor_blocks_allowed = self.__get_valid_blocks(cell, successor_block)
				successor_cells = self.__get_valid_cells(successor_board, successor_blocks_allowed, successor_block)

				# Stores the flag if the the played move results in freemove
				successor_freemoveflag = self.freemoveflag

				end_result = self.__check_end(successor_block)

				self.timedout = False

				if end_result == 2:
					return cell

				elif end_result == 0:
					minvalue = self.__eval_state(successor_board, successor_block, flag)

				else:	
					minvalue = self.__min_val_ab(successor_board, self.ALPHA_BETA_DEPTH, successor_block, cell, flag, successor_cells)

				if self.timedout == True:
					break

				# Score increase on winning center block
				if (temp_block[4] == '-' and successor_block[4] == flag):
					minvalue *= 1.3

				# If cell not in center block
				if ((int(cell[0]/3) * 3) + int(cell[1]/3)) != 4:
					top_x = cell[0] - (cell[0] % 3)
					top_y = cell[1] - (cell[1] % 3)
					# Don't play through center
					if successor_board[top_x][top_y] == successor_board[top_x + 2][top_y + 2] and successor_board[top_x + 1][top_y + 1] == '-' and successor_board[top_x][top_y] == flag:
						minvalue -= 1
					if successor_board[top_x + 2][top_y] == successor_board[top_x][top_y + 2] and successor_board[top_x + 1][top_y + 1] == '-' and successor_board[top_x][top_y + 2] == flag:
						minvalue -= 1

					# Don't play in center unless its very important
					if cell in self.center_cells and successor_block[4] == '-':
					 	minvalue -= 1

				next_moves.append((cell, minvalue))	# From each successor position, call "min"
			sorted(next_moves, key=lambda x: x[1], reverse = True)

			if next_moves != [] and next_moves[0][1] == 0:
				return next_moves[0][0]

			cells = []
			for z in next_moves:
				if z[1] != 0:
					cells.append(z[0])
			self.ALPHA_BETA_DEPTH += 1

		if old_next_moves == []:
			old_next_moves = copy.deepcopy(next_moves)
		else:
			for i in next_moves:
				for j in old_next_moves:
					if i[0] == j[0]:
						j = i

		_, best_value = max(old_next_moves, key=lambda x: x[1])		#Stores coordinates, value in _, best_value respectively.. lamba function - sorting key... Choose "max" from amongst "mins" as we are "max"
		
		choices = [cell for cell, val in old_next_moves if val == best_value]
		not_center = [cell for cell in choices if cell not in self.center_cells]
		if not_center != []:
			return random.choice(not_center)
		else:
			return random.choice(choices)

	# Determines the valid blocks from block stat
	def __get_valid_blocks(self, previous_move, block):
		allowed_blocks = []
		if previous_move[0] % 3 == 0 and previous_move[1] % 3 == 0:
			allowed_blocks = [1, 3]
		elif previous_move[0] % 3 == 0 and previous_move[1] % 3 == 2:
			allowed_blocks = [1, 5]
		elif previous_move[0] % 3 == 2 and previous_move[1] % 3 == 0:
			allowed_blocks = [3, 7]
		elif previous_move[0] % 3 == 2 and previous_move[1] % 3 == 2:
			allowed_blocks = [5, 7]
		elif previous_move[0] % 3 == 0 and previous_move[1] % 3 == 1:
			allowed_blocks = [0, 2]
		elif previous_move[0] % 3 == 1 and previous_move[1] % 3 == 0:
			allowed_blocks = [0, 6]
		elif previous_move[0] % 3 == 2 and previous_move[1] % 3 == 1:
			allowed_blocks = [6, 8]
		elif previous_move[0] % 3 == 1 and previous_move[1] % 3 == 2:
			allowed_blocks = [2, 8]
		elif previous_move[0] % 3 == 1 and previous_move[1] % 3 == 1:
			allowed_blocks = [4]

		valid_blocks = []
		for i in allowed_blocks:
			if block[i] == '-':
				valid_blocks.append(i)
		return valid_blocks

	# Gets empty cells from the list of possible blocks. Hence gets valid moves. 
	def __get_valid_cells(self, board, allowed_blocks, block):

		cells = []  # it will be list of tuples
		# Iterate over possible blocks and get empty cells
		for a_block in allowed_blocks:
			block_x = a_block / 3
			block_y = a_block % 3
			for i in range(block_x * 3, block_x * 3 + 3):
				for j in range(block_y * 3, block_y * 3 + 3):
					if board[i][j] == '-':
						cells.append((i, j))

		# If all the possible blocks are full, you can move anywhere
		if cells == []:
			self.freemoveflag = 1
			new_allowed_blocks = []
			for i in xrange(9):
				if block[i]=='-':
					new_allowed_blocks.append(i)

			for a_block in new_allowed_blocks:
				block_x = a_block / 3
				block_y = a_block % 3
				for i in range(block_x * 3, block_x * 3 + 3):
					for j in range(block_y * 3, block_y * 3 + 3):
						if board[i][j] == '-':
							cells.append((i, j))

		else:
			self.freemoveflag = 0
		return cells

	# Primarily lifted from evaluator_code.py but toggle used to ensure correct o or x is placed
	def generate_successor(self, temp_board, cell, flag):
		if self.toggle == True:
			flag = self.get_opp(flag)
		board = copy.deepcopy(temp_board)
		board[cell[0]][cell[1]] = flag
		return board

	# min from Russell and Norvig
	def __min_val_ab(self, temp_board, depth, temp_block, old_move, flag, cells, alpha=-(9223372036854775807), beta=(9223372036854775807)):	
		#Evaluate state if terminal test results in a true
		if self.terminal_test(temp_board, depth, temp_block) or ((time.time() - self.start_time) >= self.ALLOWED_TIME):
			if (time.time() - self.start_time) >= self.ALLOWED_TIME:
				self.timedout = True
			return self.__eval_state(temp_board, temp_block, flag)

		val = (9223372036854775807)

		maxvalue = 0

		for cell in cells:
			self.toggle = True
			successor_board = self.generate_successor(temp_board, cell, flag)
			successor_block = self.__update_block(successor_board, temp_block, cell)

			# Calculates valid moves for opponent
			successor_blocks_allowed = self.__get_valid_blocks(cell, successor_block)
			successor_cells = self.__get_valid_cells(successor_board, successor_blocks_allowed, successor_block)

			# Stores the flag if the the played move results in freemove
			successor_freemoveflag = self.freemoveflag

			end_result = self.__check_end(successor_block)

			if end_result == 2:
				return 0

			elif end_result == 0:
				maxvalue = self.__eval_state(successor_board, successor_block, flag)

			else:
				maxvalue = self.__max_val_ab(successor_board, depth - 1, successor_block, cell, flag, successor_cells, alpha, beta)

			#Penalty if opponent wins center block
			if (temp_block[4] == '-' and successor_block[4] == self.get_opp(flag)):
				maxvalue *= 0.9

			# Penalizes the move resulting in freemove for opponent
			if (successor_freemoveflag == 1 and (depth - 1) == 0):
				maxvalue += 10

			val = min(val, maxvalue)
			if val <= alpha:
				return val
			beta = min(beta, val)

		return val

	#max from Russell and Norvig
	def __max_val_ab(self, temp_board, depth, temp_block, old_move, flag, cells, alpha=-(9223372036854775807), beta=(9223372036854775807)):
		#Evaluate state if terminal test results in a true
		if self.terminal_test(temp_board, depth, temp_block) or ((time.time() - self.start_time) >= self.ALLOWED_TIME):
			if (time.time() - self.start_time) >= self.ALLOWED_TIME:
				self.timedout = True
			return self.__eval_state(temp_board, temp_block, flag)

		val = -(9223372036854775807)

		minvalue = 0

		for cell in cells:
			self.toggle = False
			successor_board = self.generate_successor(temp_board, cell, flag)
			successor_block = self.__update_block(successor_board, temp_block, cell)

			# Calculates valid moves for opponent
			successor_blocks_allowed = self.__get_valid_blocks(cell, successor_block)
			successor_cells = self.__get_valid_cells(successor_board, successor_blocks_allowed, successor_block)

			# Stores the flag if the the played move results in freemove
			successor_freemoveflag = self.freemoveflag

			end_result = self.__check_end(successor_block)

			if end_result == 2:
				return 1000

			elif end_result == 0:
				minvalue = self.__eval_state(successor_board, successor_block, flag)

			else:
				minvalue = self.__min_val_ab(successor_board, depth - 1, successor_block, cell, flag, successor_cells, alpha, beta)

			#Score boost if player wins center
			if (temp_block[4] == '-' and successor_block[4] == flag):
				minvalue *= 1.1

			# Penalizes the move resulting in freemove for opponent
			if (successor_freemoveflag == 1 and (depth - 1) == 0):
				minvalue -= 10

			val = max(val, minvalue)
			if val >= beta:
				return val
			alpha = max(alpha, val)

		return val

	#Used with toggle
	def get_opp(self, flag):
		if flag == 'x':
			return 'o'
		else:
			return 'x'

	def terminal_test(self, temp_board, depth, temp_block):
		if depth == 0:
			return True
		else:
			return False

	def __eval_state(self, temp_board, temp_block, flag):
		uttt_board = copy.deepcopy(temp_board)
		mini_board = copy.deepcopy(temp_block)

		mini_board_scores = []
		#Store probabilities of winning a mini board
		for val in xrange(9):
			if mini_board[val] == '-':
				temp_val = self.__evaluate_Mini_Board(uttt_board, temp_block, val, flag)
				mini_board_scores.append((float(temp_val)+800.0)/1600.0)	#Max value possibly returned by __evaluate_Mini_Board is +800 and min is -800 (A board full of "flags" gives +800 while a board full of "antiflags" gives -800). So scale it between 0 and 1 as probability is needed
			elif mini_board[val] == flag:
				mini_board_scores.append(1.0)
			else:
				mini_board_scores.append(0.0)

		#Get the bigger picture !!
		val = self.score_big_board(mini_board_scores)
	
		return val

	# Returns the lines involved in winning
	def __get_possible_blocks(self, index):
		if index == 0:
			return [(1,2), (3,6), (4,8)]
		elif index == 1:
			return [(0,2), (4,7)]
		elif index == 2:
			return [(0,1), (5,8), (4,6)]
		elif index == 3:
			return [(0,6), (4,5)]
		elif index == 4:
			return [(0,8), (2,6), (1,7), (3,5)]
		elif index == 5:
			return [(3,4), (2,8)]
		elif index == 6:
			return [(0,3), (7,8), (2,4)]
		elif index == 7:
			return [(1,4), (6,8)]
		elif index == 8:
			return [(0,4), (2,5), (6,7)]

	def __evaluate_Mini_Board(self, temp_board, temp_block, index, flag):
		score = 0
		row_num = 0
		col_num = 0
		
		#Initialize row_num and col_num to point to correct cell in 3x3 mini board using index
		if index == 0 or index == 1 or index == 2:
			row_num = 0
		elif index == 3 or index == 4 or index == 5:
			row_num = 3
		else:
			row_num = 6

		if index == 0 or index == 3 or index == 6:
			col_num = 0
		elif index == 1 or index == 4 or index == 7:
			col_num = 3
		else:
			col_num = 6

		#For rows get score
		for i in xrange(3):
			flags, anti_flags, blanks = self.count_symbols_row(temp_board, row_num+i, col_num, flag)
			if flags == 3:
				score += 100
			elif flags == 2 and blanks == 1:
				score += 10
			elif flags == 1 and blanks == 2:
				score += 1
			elif anti_flags == 3:
				score -= 100
			elif anti_flags == 2 and blanks == 1:
				score -= 10
			elif anti_flags == 1 and blanks == 2:
				score -= 1
			elif flags == 2 and anti_flags == 1:
				temp_combos = self.__get_possible_blocks(index)
				for k in temp_combos:
					selfs = 0
					for l in (0,1):
						if temp_block[k[l]] == flag:
							selfs += 1
					if selfs == 2:
						score -= 10
					else:
						score -= 1
			elif anti_flags == 2 and flags == 1:
				temp_combos = self.__get_possible_blocks(index)
				for k in temp_combos:
					opps = 0
					for l in (0,1):
						if temp_block[k[l]] == self.get_opp(flag):
							opps += 1
					if opps == 2:
						score += 10
					else:
						score += 1

		#For cols get score
		for i in xrange(3):
			flags, anti_flags, blanks = self.count_symbols_col(temp_board, row_num, col_num+i, flag)
			if flags == 3:
				score += 100
			elif flags == 2 and blanks == 1:
				score += 10
			elif flags == 1 and blanks == 2:
				score += 1
			elif anti_flags == 3:
				score -= 100
			elif anti_flags == 2 and blanks == 1:
				score -= 10
			elif anti_flags == 1 and blanks == 2:
				score -= 1
			elif flags == 2 and anti_flags == 1:
				temp_combos = self.__get_possible_blocks(index)
				for k in temp_combos:
					selfs = 0
					for l in (0,1):
						if temp_block[k[l]] == flag:
							selfs += 1
					if selfs == 2:
						score -= 10
					else:
						score -= 1
			elif anti_flags == 2 and flags == 1:
				temp_combos = self.__get_possible_blocks(index)
				for k in temp_combos:
					opps = 0
					for l in (0,1):
						if temp_block[k[l]] == self.get_opp(flag):
							opps += 1
					if opps == 2:
						score += 10
					else:
						score += 1

		#For diag left top to bottom right get score
		flags = 0 
		anti_flags = 0
		blanks = 0
		for i in xrange(3):
			if temp_board[row_num+i][col_num+i] == flag:
				flags += 1
			elif temp_board[row_num+i][col_num+i] == '-':
				blanks += 1
			else:
				anti_flags += 1

		if flags == 3:
			score += 100
		elif flags == 2 and blanks == 1:
			score += 10
		elif flags == 1 and blanks == 2:
			score += 1
		elif anti_flags == 3:
			score -= 100
		elif anti_flags == 2 and blanks == 1:
			score -= 10
		elif anti_flags == 1 and blanks == 2:
			score -= 1
		elif flags == 2 and anti_flags == 1:
			temp_combos = self.__get_possible_blocks(index)
			for k in temp_combos:
				selfs = 0
				for l in (0,1):
					if temp_block[k[l]] == flag:
						selfs += 1
				if selfs == 2:
					score -= 10
				else:
					score -= 1
		elif anti_flags == 2 and flags == 1:
			temp_combos = self.__get_possible_blocks(index)
			for k in temp_combos:
				opps = 0
				for l in (0,1):
					if temp_block[k[l]] == self.get_opp(flag):
						opps += 1
				if opps == 2:
					score += 10
				else:
					score += 1

		#For diag right top to bottom left get score
		flags = 0 
		anti_flags = 0
		blanks = 0
		for i in xrange(3):
			if temp_board[row_num+2-i][col_num+2-i] == flag:
				flags += 1
			elif temp_board[row_num+2-i][col_num+2-i] == '-':
				blanks += 1
			else:
				anti_flags += 1

		if flags == 3:
			score += 100
		elif flags == 2 and blanks == 1:
			score += 10
		elif flags == 1 and blanks == 2:
			score += 1
		elif anti_flags == 3:
			score -= 100
		elif anti_flags == 2 and blanks == 1:
			score -= 10
		elif anti_flags == 1 and blanks == 2:
			score -= 1
		elif flags == 2 and anti_flags == 1:
			temp_combos = self.__get_possible_blocks(index)
			for k in temp_combos:
				selfs = 0
				for l in (0,1):
					if temp_block[k[l]] == flag:
						selfs += 1
				if selfs == 2:
					score -= 10
				else:
					score -= 1
		elif anti_flags == 2 and flags == 1:
			temp_combos = self.__get_possible_blocks(index)
			for k in temp_combos:
				opps = 0
				for l in (0,1):
					if temp_block[k[l]] == self.get_opp(flag):
						opps += 1
				if opps == 2:
					score += 10
				else:
					score += 1
			
		return score

	#To count number of "flag", "antiflag" and "-" in a given row
	def count_symbols_row(self, temp_board, row_num, col_num, flag):
		flags = 0 
		anti_flags = 0
		blanks = 0
		for i in xrange(3):
			if temp_board[row_num][col_num+i] == flag:
				flags += 1
			elif temp_board[row_num][col_num+i] == '-':
				blanks += 1
			else:
				anti_flags += 1

		return flags, anti_flags, blanks

	#To count number of "flag", "antiflag" and "-" in a given column
	def count_symbols_col(self, temp_board, row_num, col_num, flag):
		flags = 0 
		anti_flags = 0
		blanks = 0
		for i in xrange(3):
			if temp_board[row_num+i][col_num] == flag:
				flags += 1
			elif temp_board[row_num+i][col_num] == '-':
				blanks += 1
			else:
				anti_flags += 1

		return flags, anti_flags, blanks

	#Scores the bigger 3x3 board where each block is considered a cell
	#mini_board_scores holds the probability of winning that particular block
	def score_big_board(self, mini_board_scores):
		score = 0

		#Score the rows
		for i in [0,3,6]:
			temp_val = 0
			if self.__check_xo_together(mini_board_scores, (i+0, i+1, i+2)) == True:
				continue
			for j in [0,1,2]:
				temp_val += mini_board_scores[i+j]
			if temp_val >= 0 and temp_val < 1:
				score += temp_val
			elif temp_val >= 1 and temp_val < 2:
				temp = temp_val - 1
				score += (1 + (temp * (10-1)))
			else:
				temp = temp_val - 2
				score += (10 + (temp * (100-10-1)))
		
		#Score the columns
		for i in [0,1,2]:
			temp_val = 0
			if self.__check_xo_together(mini_board_scores, (i+0, i+3, i+6)) == True:
				continue
			for j in [0,3,6]:
				temp_val += mini_board_scores[i+j]
			if temp_val >= 0 and temp_val < 1:
				score += temp_val
			elif temp_val >= 1 and temp_val < 2:
				temp = temp_val - 1
				score += (1 + (temp * (10-1)))
			else:
				temp = temp_val - 2
				score += (10 + (temp * (100-10-1)))

		#Score diag top left to bottom right
		temp_val = 0
		if self.__check_xo_together(mini_board_scores, (0, 4, 8)) == False:
			for i in [0,4,8]:
				temp_val += mini_board_scores[i]
			if temp_val >= 0 and temp_val < 1:
				score += temp_val
			elif temp_val >= 1 and temp_val < 2:
				temp = temp_val - 1
				score += (1 + (temp * (10-1)))
			else:
				temp = temp_val - 2
				score += (10 + (temp * (100-10-1)))

		#Score diag top right to bottom left
		temp_val = 0
		if self.__check_xo_together(mini_board_scores, (2, 4, 6)) == False:
			for i in [2,4,6]:
				temp_val += mini_board_scores[i]
			if temp_val >= 0 and temp_val < 1:
				score += temp_val
			elif temp_val >= 1 and temp_val < 2:
				temp = temp_val - 1
				score += (1 + (temp * (10-1)))
			else:
				temp = temp_val - 2
				score += (10 + (temp * (100-10-1)))

		return score

	def __update_block(self, board, original_block, cell):

		block = copy.deepcopy(original_block)

		# Finds the block number where the move has been made
		index_of_block = (cell[0] / 3) * 3 + (cell[1] / 3)

		top_x = cell[0] - (cell[0] % 3)
		top_y = cell[1] - (cell[1] % 3)

		for i in xrange(3):
			#Rows
			if board[top_x + i][top_y] == board[top_x + i][top_y + 1] and board[top_x + i][top_y + 1] == board[top_x + i][top_y + 2]:
				if board[top_x + i][top_y] == 'x':
					block[index_of_block] = 'x'
					return block

				elif board[top_x + i][top_y] == 'o':
					block[index_of_block] = 'o'
					return block
			
			#Columns
			elif board[top_x][top_y + i] == board[top_x + 1][top_y + i] and board[top_x + 1][top_y + i] == board[top_x + 2][top_y + i]:
				if board[top_x][top_y + i] == 'x':
					block[index_of_block] = 'x'
					return block

				elif board[top_x][top_y + i] == 'o':
					block[index_of_block] = 'o'
					return block

		#Top left to bottom right
		if board[top_x][top_y] == board[top_x + 1][top_y + 1] and board[top_x + 1][top_y + 1] == board[top_x + 2][top_y + 2]:
			if board[top_x][top_y] == 'x':
				block[index_of_block] = 'x'
				return block

			elif board[top_x][top_y] == 'o':
				block[index_of_block] = 'o'
				return block

		#Bottom left to top right
		if board[top_x + 2][top_y] == board[top_x + 1][top_y + 1] and board[top_x + 1][top_y + 1] == board[top_x][top_y + 2]:
			if board[top_x + 2][top_y] == 'x':
				block[index_of_block] = 'x'
				return block

			elif board[top_x + 2][top_y] == 'o':
				block[index_of_block] = 'o'
				return block

		for i in xrange(3):
			for j in xrange(3):
				if board[top_x + i][top_y + i] == '-':
					return block

		block[index_of_block] = 'D'
		return block

	#Checks if the game has ended
	#Return 2 for win, 1 for not ended, 0 for draw
	def __check_end(self, block):
		for i in [0, 3, 6]:
			if block[i + 0] == block[i + 1] and block[i + 1] == block[i + 2] and (block[i] == 'x' or block[i] == 'o'):
				return 2
		for i in [0, 1, 2]:
			if block[i + 0] == block[i + 3] and block[i + 3] == block[i + 6] and (block[i] == 'x' or block[i] == 'o'):
				return 2

		if block[0] == block[4] and block[4] == block[8] and (block[0] == 'x' or block[0] == 'o'):
			return 2

		if block[2] == block[4] and block[4] == block[6] and (block[2] == 'x' or block[2] == 'o'):
			return 2

		for i in xrange(9):
			if block[i] == '-':
				return 1

		return 0

	#Used in score_big_board while evaluating probabilites
	def __check_xo_together(self, block, arrs):
		xs = 0
		os = 0
		for i in arrs:
			if block[i] == 1:
				xs += 1
			elif block[i] == 0:
				os += 1

		if xs > 0 and os > 0:
			return True
		else:
			return False

# =========== Game Board ===========
# - - -  - - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - -

# - - -  - - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - -

# - - -  - - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Player 1 made the move: (3, 8) with x
# =========== Game Board ===========
# - - -  - - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - -

# - - -  - - -  - - x
# - - -  - - -  - - -
# - - -  - - -  - - -

# - - -  - - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (0, 3) with o
# =========== Game Board ===========
# - - -  o - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - -

# - - -  - - -  - - x
# - - -  - - -  - - -
# - - -  - - -  - - -

# - - -  - - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Player 1 made the move: (3, 1) with x
# =========== Game Board ===========
# - - -  o - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - -

# - x -  - - -  - - x
# - - -  - - -  - - -
# - - -  - - -  - - -

# - - -  - - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (2, 8) with o
# =========== Game Board ===========
# - - -  o - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - o

# - x -  - - -  - - x
# - - -  - - -  - - -
# - - -  - - -  - - -

# - - -  - - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Player 1 made the move: (7, 3) with x
# =========== Game Board ===========
# - - -  o - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - o

# - x -  - - -  - - x
# - - -  - - -  - - -
# - - -  - - -  - - -

# - - -  - - -  - - -
# - - -  x - -  - - -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (0, 2) with o
# =========== Game Board ===========
# - - o  o - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - o

# - x -  - - -  - - x
# - - -  - - -  - - -
# - - -  - - -  - - -

# - - -  - - -  - - -
# - - -  x - -  - - -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Player 1 made the move: (4, 6) with x
# =========== Game Board ===========
# - - o  o - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - o

# - x -  - - -  - - x
# - - -  - - -  x - -
# - - -  - - -  - - -

# - - -  - - -  - - -
# - - -  x - -  - - -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (0, 0) with o
# =========== Game Board ===========
# o - o  o - -  - - -
# - - -  - - -  - - -
# - - -  - - -  - - o

# - x -  - - -  - - x
# - - -  - - -  x - -
# - - -  - - -  - - -

# - - -  - - -  - - -
# - - -  x - -  - - -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Player 1 made the move: (2, 5) with x
# =========== Game Board ===========
# o - o  o - -  - - -
# - - -  - - -  - - -
# - - -  - - x  - - o

# - x -  - - -  - - x
# - - -  - - -  x - -
# - - -  - - -  - - -

# - - -  - - -  - - -
# - - -  x - -  - - -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (5, 7) with o
# =========== Game Board ===========
# o - o  o - -  - - -
# - - -  - - -  - - -
# - - -  - - x  - - o

# - x -  - - -  - - x
# - - -  - - -  x - -
# - - -  - - -  - o -

# - - -  - - -  - - -
# - - -  x - -  - - -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Player 1 made the move: (7, 6) with x
# =========== Game Board ===========
# o - o  o - -  - - -
# - - -  - - -  - - -
# - - -  - - x  - - o

# - x -  - - -  - - x
# - - -  - - -  x - -
# - - -  - - -  - o -

# - - -  - - -  - - -
# - - -  x - -  x - -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# - - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (0, 1) with o
# =========== Game Board ===========
# o o o  o - -  - - -
# - - -  - - -  - - -
# - - -  - - x  - - o

# - x -  - - -  - - x
# - - -  - - -  x - -
# - - -  - - -  - o -

# - - -  - - -  - - -
# - - -  x - -  x - -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# o - -
# - - -
# - - -
# ==================================

# Player 1 made the move: (1, 6) with x
# =========== Game Board ===========
# o o o  o - -  - - -
# - - -  - - -  x - -
# - - -  - - x  - - o

# - x -  - - -  - - x
# - - -  - - -  x - -
# - - -  - - -  - o -

# - - -  - - -  - - -
# - - -  x - -  x - -
# - - -  - - -  - - -
# ==================================
# =========== Block Status =========
# o - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (8, 2) with o
# =========== Game Board ===========
# o o o  o - -  - - -
# - - -  - - -  x - -
# - - -  - - x  - - o

# - x -  - - -  - - x
# - - -  - - -  x - -
# - - -  - - -  - o -

# - - -  - - -  - - -
# - - -  x - -  x - -
# - - o  - - -  - - -
# ==================================
# =========== Block Status =========
# o - -
# - - -
# - - -
# ==================================

# Player 1 made the move: (6, 5) with x
# =========== Game Board ===========
# o o o  o - -  - - -
# - - -  - - -  x - -
# - - -  - - x  - - o

# - x -  - - -  - - x
# - - -  - - -  x - -
# - - -  - - -  - o -

# - - -  - - x  - - -
# - - -  x - -  x - -
# - - o  - - -  - - -
# ==================================
# =========== Block Status =========
# o - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (1, 3) with o
# =========== Game Board ===========
# o o o  o - -  - - -
# - - -  o - -  x - -
# - - -  - - x  - - o

# - x -  - - -  - - x
# - - -  - - -  x - -
# - - -  - - -  - o -

# - - -  - - x  - - -
# - - -  x - -  x - -
# - - o  - - -  - - -
# ==================================
# =========== Block Status =========
# o - -
# - - -
# - - -
# ==================================

# Player 1 made the move: (8, 1) with x
# =========== Game Board ===========
# o o o  o - -  - - -
# - - -  o - -  x - -
# - - -  - - x  - - o

# - x -  - - -  - - x
# - - -  - - -  x - -
# - - -  - - -  - o -

# - - -  - - x  - - -
# - - -  x - -  x - -
# - x o  - - -  - - -
# ==================================
# =========== Block Status =========
# o - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (7, 1) with o
# =========== Game Board ===========
# o o o  o - -  - - -
# - - -  o - -  x - -
# - - -  - - x  - - o

# - x -  - - -  - - x
# - - -  - - -  x - -
# - - -  - - -  - o -

# - - -  - - x  - - -
# - o -  x - -  x - -
# - x o  - - -  - - -
# ==================================
# =========== Block Status =========
# o - -
# - - -
# - - -
# ==================================

# Player 1 made the move: (3, 4) with x
# =========== Game Board ===========
# o o o  o - -  - - -
# - - -  o - -  x - -
# - - -  - - x  - - o

# - x -  - x -  - - x
# - - -  - - -  x - -
# - - -  - - -  - o -

# - - -  - - x  - - -
# - o -  x - -  x - -
# - x o  - - -  - - -
# ==================================
# =========== Block Status =========
# o - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (1, 8) with o
# =========== Game Board ===========
# o o o  o - -  - - -
# - - -  o - -  x - o
# - - -  - - x  - - o

# - x -  - x -  - - x
# - - -  - - -  x - -
# - - -  - - -  - o -

# - - -  - - x  - - -
# - o -  x - -  x - -
# - x o  - - -  - - -
# ==================================
# =========== Block Status =========
# o - -
# - - -
# - - -
# ==================================

# Player 1 made the move: (0, 8) with x
# =========== Game Board ===========
# o o o  o - -  - - x
# - - -  o - -  x - o
# - - -  - - x  - - o

# - x -  - x -  - - x
# - - -  - - -  x - -
# - - -  - - -  - o -

# - - -  - - x  - - -
# - o -  x - -  x - -
# - x o  - - -  - - -
# ==================================
# =========== Block Status =========
# o - -
# - - -
# - - -
# ==================================

# Player 2 made the move: (2, 3) with o
# =========== Game Board ===========
# o o o  o - -  - - x
# - - -  o - -  x - o
# - - -  o - x  - - o

# - x -  - x -  - - x
# - - -  - - -  x - -
# - - -  - - -  - o -

# - - -  - - x  - - -
# - o -  x - -  x - -
# - x o  - - -  - - -
# ==================================
# =========== Block Status =========
# o o -
# - - -
# - - -
# ==================================

# Player 1 made the move: (4, 1) with x
# =========== Game Board ===========
# o o o  o - -  - - x
# - - -  o - -  x - o
# - - -  o - x  - - o

# - x -  - x -  - - x
# - x -  - - -  x - -
# - - -  - - -  - o -

# - - -  - - x  - - -
# - o -  x - -  x - -
# - x o  - - -  - - -
# ==================================
# =========== Block Status =========
# o o -
# - - -
# - - -
# ==================================

# Player 2 made the move: (4, 4) with o
# =========== Game Board ===========
# o o o  o - -  - - x
# - - -  o - -  x - o
# - - -  o - x  - - o

# - x -  - x -  - - x
# - x -  - o -  x - -
# - - -  - - -  - o -

# - - -  - - x  - - -
# - o -  x - -  x - -
# - x o  - - -  - - -
# ==================================
# =========== Block Status =========
# o o -
# - - -
# - - -
# ==================================

# Player 1 made the move: (5, 5) with x
# =========== Game Board ===========
# o o o  o - -  - - x
# - - -  o - -  x - o
# - - -  o - x  - - o

# - x -  - x -  - - x
# - x -  - o -  x - -
# - - -  - - x  - o -

# - - -  - - x  - - -
# - o -  x - -  x - -
# - x o  - - -  - - -
# ==================================
# =========== Block Status =========
# o o -
# - - -
# - - -
# ==================================

# Player 2 made the move: (5, 8) with o
# =========== Game Board ===========
# o o o  o - -  - - x
# - - -  o - -  x - o
# - - -  o - x  - - o

# - x -  - x -  - - x
# - x -  - o -  x - -
# - - -  - - x  - o o

# - - -  - - x  - - -
# - o -  x - -  x - -
# - x o  - - -  - - -
# ==================================
# =========== Block Status =========
# o o -
# - - -
# - - -
# ==================================

# Player 1 made the move: (4, 7) with x
# =========== Game Board ===========
# o o o  o - -  - - x
# - - -  o - -  x - o
# - - -  o - x  - - o

# - x -  - x -  - - x
# - x -  - o -  x x -
# - - -  - - x  - o o

# - - -  - - x  - - -
# - o -  x - -  x - -
# - x o  - - -  - - -
# ==================================
# =========== Block Status =========
# o o -
# - - -
# - - -
# ==================================

# Player 2 made the move: (3, 5) with o
# =========== Game Board ===========
# o o o  o - -  - - x
# - - -  o - -  x - o
# - - -  o - x  - - o

# - x -  - x o  - - x
# - x -  - o -  x x -
# - - -  - - x  - o o

# - - -  - - x  - - -
# - o -  x - -  x - -
# - x o  - - -  - - -
# ==================================
# =========== Block Status =========
# o o -
# - - -
# - - -
# ==================================

# Player 1 made the move: (5, 6) with x
# =========== Game Board ===========
# o o o  o - -  - - x
# - - -  o - -  x - o
# - - -  o - x  - - o

# - x -  - x o  - - x
# - x -  - o -  x x -
# - - -  - - x  x o o

# - - -  - - x  - - -
# - o -  x - -  x - -
# - x o  - - -  - - -
# ==================================
# =========== Block Status =========
# o o -
# - - x
# - - -
# ==================================

# Player 2 made the move: (5, 2) with o
# =========== Game Board ===========
# o o o  o - -  - - x
# - - -  o - -  x - o
# - - -  o - x  - - o

# - x -  - x o  - - x
# - x -  - o -  x x -
# - - o  - - x  x o o

# - - -  - - x  - - -
# - o -  x - -  x - -
# - x o  - - -  - - -
# ==================================
# =========== Block Status =========
# o o -
# - - x
# - - -
# ==================================

# Player 1 made the move: (8, 4) with x
# =========== Game Board ===========
# o o o  o - -  - - x
# - - -  o - -  x - o
# - - -  o - x  - - o

# - x -  - x o  - - x
# - x -  - o -  x x -
# - - o  - - x  x o o

# - - -  - - x  - - -
# - o -  x - -  x - -
# - x o  - x -  - - -
# ==================================
# =========== Block Status =========
# o o -
# - - x
# - - -
# ==================================

# Player 2 made the move: (8, 8) with o
# =========== Game Board ===========
# o o o  o - -  - - x
# - - -  o - -  x - o
# - - -  o - x  - - o

# - x -  - x o  - - x
# - x -  - o -  x x -
# - - o  - - x  x o o

# - - -  - - x  - - -
# - o -  x - -  x - -
# - x o  - x -  - - o
# ==================================
# =========== Block Status =========
# o o -
# - - x
# - - -
# ==================================

# Player 1 made the move: (7, 4) with x
# =========== Game Board ===========
# o o o  o - -  - - x
# - - -  o - -  x - o
# - - -  o - x  - - o

# - x -  - x o  - - x
# - x -  - o -  x x -
# - - o  - - x  x o o

# - - -  - - x  - - -
# - o -  x x -  x - -
# - x o  - x -  - - o
# ==================================
# =========== Block Status =========
# o o -
# - - x
# - - -
# ==================================

# Player 2 made the move: (5, 3) with o
# =========== Game Board ===========
# o o o  o - -  - - x
# - - -  o - -  x - o
# - - -  o - x  - - o

# - x -  - x o  - - x
# - x -  - o -  x x -
# - - o  o - x  x o o

# - - -  - - x  - - -
# - o -  x x -  x - -
# - x o  - x -  - - o
# ==================================
# =========== Block Status =========
# o o -
# - o x
# - - -
# ==================================

# Player 1 made the move: (8, 5) with x
# =========== Game Board ===========
# o o o  o - -  - - x
# - - -  o - -  x - o
# - - -  o - x  - - o

# - x -  - x o  - - x
# - x -  - o -  x x -
# - - o  o - x  x o o

# - - -  - - x  - - -
# - o -  x x -  x - -
# - x o  - x x  - - o
# ==================================
# =========== Block Status =========
# o o -
# - o x
# - - -
# ==================================

# Player 2 made the move: (6, 4) with o
# =========== Game Board ===========
# o o o  o - -  - - x
# - - -  o - -  x - o
# - - -  o - x  - - o

# - x -  - x o  - - x
# - x -  - o -  x x -
# - - o  o - x  x o o

# - - -  - o x  - - -
# - o -  x x -  x - -
# - x o  - x x  - - o
# ==================================
# =========== Block Status =========
# o o -
# - o x
# - - -
# ==================================

# Player 1 made the move: (0, 6) with x
# =========== Game Board ===========
# o o o  o - -  x - x
# - - -  o - -  x - o
# - - -  o - x  - - o

# - x -  - x o  - - x
# - x -  - o -  x x -
# - - o  o - x  x o o

# - - -  - o x  - - -
# - o -  x x -  x - -
# - x o  - x x  - - o
# ==================================
# =========== Block Status =========
# o o -
# - o x
# - - -
# ==================================

# Player 2 made the move: (5, 0) with o
# =========== Game Board ===========
# o o o  o - -  x - x
# - - -  o - -  x - o
# - - -  o - x  - - o

# - x -  - x o  - - x
# - x -  - o -  x x -
# o - o  o - x  x o o

# - - -  - o x  - - -
# - o -  x x -  x - -
# - x o  - x x  - - o
# ==================================
# =========== Block Status =========
# o o -
# - o x
# - - -
# ==================================

# Player 1 made the move: (3, 0) with x
# =========== Game Board ===========
# o o o  o - -  x - x
# - - -  o - -  x - o
# - - -  o - x  - - o

# x x -  - x o  - - x
# - x -  - o -  x x -
# o - o  o - x  x o o

# - - -  - o x  - - -
# - o -  x x -  x - -
# - x o  - x x  - - o
# ==================================
# =========== Block Status =========
# o o -
# - o x
# - - -
# ==================================

# Player 2 made the move: (5, 1) with o
# =========== Game Board ===========
# o o o  o - -  x - x
# - - -  o - -  x - o
# - - -  o - x  - - o

# x x -  - x o  - - x
# - x -  - o -  x x -
# o o o  o - x  x o o

# - - -  - o x  - - -
# - o -  x x -  x - -
# - x o  - x x  - - o
# ==================================
# =========== Block Status =========
# o o -
# o o x
# - - -
# ==================================

# Player 1 made the move: (8, 6) with x
# =========== Game Board ===========
# o o o  o - -  x - x
# - - -  o - -  x - o
# - - -  o - x  - - o

# x x -  - x o  - - x
# - x -  - o -  x x -
# o o o  o - x  x o o

# - - -  - o x  - - -
# - o -  x x -  x - -
# - x o  - x x  x - o
# ==================================
# =========== Block Status =========
# o o -
# o o x
# - - -
# ==================================

# Player 2 made the move: (6, 3) with o
# =========== Game Board ===========
# o o o  o - -  x - x
# - - -  o - -  x - o
# - - -  o - x  - - o

# x x -  - x o  - - x
# - x -  - o -  x x -
# o o o  o - x  x o o

# - - -  o o x  - - -
# - o -  x x -  x - -
# - x o  - x x  x - o
# ==================================
# =========== Block Status =========
# o o -
# o o x
# - - -
# ==================================

# Player 1 made the move: (1, 7) with x
# =========== Game Board ===========
# o o o  o - -  x - x
# - - -  o - -  x x o
# - - -  o - x  - - o

# x x -  - x o  - - x
# - x -  - o -  x x -
# o o o  o - x  x o o

# - - -  o o x  - - -
# - o -  x x -  x - -
# - x o  - x x  x - o
# ==================================
# =========== Block Status =========
# o o -
# o o x
# - - -
# ==================================

# Player 2 made the move: (6, 0) with o
# =========== Game Board ===========
# o o o  o - -  x - x
# - - -  o - -  x x o
# - - -  o - x  - - o

# x x -  - x o  - - x
# - x -  - o -  x x -
# o o o  o - x  x o o

# o - -  o o x  - - -
# - o -  x x -  x - -
# - x o  - x x  x - o
# ==================================
# =========== Block Status =========
# o o -
# o o x
# o - -
# ==================================

# P2
# COMPLETE