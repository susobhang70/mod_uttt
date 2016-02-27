import random
import copy		#For copy.deepcopy() 
import sys 		#For sys.exit()
import time     #For timer functions

MAX = 9223372036854775807	#For MAX used 

class Player27():

	#TODO : Can have a timer with the help of which best move seen so far can be returned just before the timer runs out
	def __init__(self):
		self.ALPHA_BETA_DEPTH = 6	#The depth of the search tree
		self.toggle = False			#toggle is used in generate_successor(). It is used to decide whether to place x or o in the current turn
		#TODO : toggle may be slowing the code. May optimize for speed using another mechanism
		self.start_time = 0.0
		self.ALLOWED_TIME = 11.5

	def move(self, temp_board, temp_block, old_move, flag):
		# board: is the list of lists that represents the 9x9 grid
		# board[i] can be 'x', 'o' or '-'
		# block: is a list that represents if a block is won or available to play in
		# block[i] can be 'x', 'o' or '-'
		# old_move: is a tuple of integers representing co-ordintates of the last move made. For the first move of game it is (-1,-1)
		# flag: is your marker. it can be 'x' or 'o'.
		#List of permitted blocks, based on old move.

		#If moving first, place in the centre of centre
		if(old_move[0] == -1 and old_move[1] == -1):
			return (4,4)

		#Get list of empty valid cells
		blocks_allowed  = self.determine_blocks_allowed(old_move, temp_block)
		cells = self.get_empty_out_of(temp_board, blocks_allowed,temp_block)

		#If only one move available, don't waste time further
		if(len(cells) == 1):
			return (cells[0][0], cells[0][1])

		next_moves = []

		#Search depth optimization. TODO : Modify and find optimum, may try IDS too
		if (len(cells) >= 3):
			self.ALPHA_BETA_DEPTH = 2	#If more number of choices, look shallower
		else:
			self.ALPHA_BETA_DEPTH = 3	#If less number of choices, look deeper
		
		self.start_time = time.time()

		while True:
			if time.time() - self.start_time >= self.ALLOWED_TIME:
				break
			self.ALPHA_BETA_DEPTH += 1
			for cell in cells:
				self.toggle = False
				successor_board = self.generate_successor(temp_board, cell, flag)
				#TODO : May need to work on move ordering to make alpha beta pruning more effective
				next_moves.append((cell, self.__min_val_ab(successor_board, self.ALPHA_BETA_DEPTH, temp_block, old_move, flag)))	#From each successor position, call "min"

		print self.ALPHA_BETA_DEPTH,"ALPHA_BETA_DEPTH"
		_, best_value = max(next_moves, key=lambda x: x[1])		#Stores coordinates, value in _, best_value respectively.. lamba function - sorting key... Choose "max" from amongst "mins" as we are "max"
		
		return random.choice([best_action for best_action, val in next_moves if val == best_value])	#If many choices with equal reward, choose randomly..Python syntactic sugar!!

	# #Time out handler
	# def handler(signum, frame):
	#     #print 'Signal handler called with signal', signum
	#     raise TimedOutExc()

	#This is lifted from evaluator_code.py.. TODO : Will have to change as per rules
	def determine_blocks_allowed(self, old_move, block_stat):
		blocks_allowed = []
		if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
			blocks_allowed = [1,3]
		elif old_move[0] % 3 == 0 and old_move[1] % 3 == 2:
			blocks_allowed = [1,5]
		elif old_move[0] % 3 == 2 and old_move[1] % 3 == 0:
			blocks_allowed = [3,7]
		elif old_move[0] % 3 == 2 and old_move[1] % 3 == 2:
			blocks_allowed = [5,7]
		elif old_move[0] % 3 == 0 and old_move[1] % 3 == 1:
			blocks_allowed = [0,2]
		elif old_move[0] % 3 == 1 and old_move[1] % 3 == 0:
			blocks_allowed = [0,6]
		elif old_move[0] % 3 == 2 and old_move[1] % 3 == 1:
			blocks_allowed = [6,8]
		elif old_move[0] % 3 == 1 and old_move[1] % 3 == 2:
			blocks_allowed = [2,8]
		elif old_move[0] % 3 == 1 and old_move[1] % 3 == 1:
			blocks_allowed = [4]
		else:
			sys.exit(1)
		final_blocks_allowed = []
		for i in blocks_allowed:
			if block_stat[i] == '-':
				final_blocks_allowed.append(i)
		return final_blocks_allowed

	#This is lifted from evaluator_code.py.. TODO : Will have to change as per rules
	#Gets empty cells from the list of possible blocks. Hence gets valid moves. 
	def get_empty_out_of(self, gameb, blal,block_stat):
		cells = []  # it will be list of tuples
		#Iterate over possible blocks and get empty cells
		for idb in blal:
			id1 = idb/3
			id2 = idb%3
			for i in range(id1*3,id1*3+3):
				for j in range(id2*3,id2*3+3):
					if gameb[i][j] == '-':
						cells.append((i,j))

		# If all the possible blocks are full, you can move anywhere
		if cells == []:
			new_blal = []
			all_blal = [0,1,2,3,4,5,6,7,8]
			for i in all_blal:
				if block_stat[i]=='-':
					new_blal.append(i)

			for idb in new_blal:
				id1 = idb/3
				id2 = idb%3
				for i in range(id1*3,id1*3+3):
					for j in range(id2*3,id2*3+3):
						if gameb[i][j] == '-':
							cells.append((i,j))
		return cells

	#Primarily lifted from evaluator_code.py but toggle used to ensure correct o or x is placed
	def generate_successor(self, temp_board, cell, flag):
		if self.toggle == True:
			flag = self.get_opp(flag)
		board = copy.deepcopy(temp_board)
		board[cell[0]][cell[1]] = flag
		return board

	#min from Russell and Norvig
	def __min_val_ab(self, temp_board, depth, temp_block, old_move, flag, alpha=-(MAX), beta=(MAX)):	
		#Evaluate state if terminal test results in a true
		if self.terminal_test(temp_board, depth, temp_block) or ((time.time() - self.start_time) >= self.ALLOWED_TIME):
			return self.__eval_state(temp_board, temp_block, flag)

		val = (MAX)

		#Get list of empty valid cells, TODO : again may need to work on move ordering
		blocks_allowed  = self.determine_blocks_allowed(old_move, temp_block)
		cells = self.get_empty_out_of(temp_board, blocks_allowed, temp_block)

		for cell in cells:
			self.toggle = True
			successor_board = self.generate_successor(temp_board, cell, flag)
			val = min(val, self.__max_val_ab(successor_board,  depth-1, temp_block, old_move, flag, alpha, beta))
			if val <= alpha:
				return val
			beta = min(beta, val)

		return val

	#max from Russell and Norvig
	def __max_val_ab(self, temp_board, depth, temp_block, old_move, flag, alpha=-(MAX), beta=(MAX)):
		#Evaluate state if terminal test results in a true
		if self.terminal_test(temp_board, depth, temp_block) or ((time.time() - self.start_time) >= self.ALLOWED_TIME):
			return self.__eval_state(temp_board, temp_block, flag)

		val = -(MAX)

		#Get list of empty valid cells, TODO : again may need to work on move ordering
		blocks_allowed  = self.determine_blocks_allowed(old_move, temp_block)
		cells = self.get_empty_out_of(temp_board, blocks_allowed, temp_block)

		for cell in cells:
			self.toggle = False
			successor_board = self.generate_successor(temp_board, cell, flag)
			val = max(val, self.__min_val_ab(successor_board, depth-1, temp_block, old_move, flag, alpha, beta))
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

	#Simple terminal test.. TODO : Possibilities to improve the terminal test
	def terminal_test(self, temp_board, depth, temp_block):
		if depth==0:
			return True
		else:
			return False

	#Evaluation Function TODO : Add a lot of heuristics
	def __eval_state(self, temp_board, temp_block, flag):
		uttt_board = copy.deepcopy(temp_board)
		mini_board = copy.deepcopy(temp_block)

		mini_board_scores = []
		#Store probabilities of winning a mini board
		for val in xrange(9):
			if mini_board[val] == '-':
				temp_val = self.__evaluate_Mini_Board(uttt_board, val, flag)
				mini_board_scores.append((float(temp_val)+800.0)/1600.0)	#Max value possibly returned by __evaluate_Mini_Board is +800 and min is -800 (A board full of "flags" gives +800 while a board full of "antiflags" gives -800). So scale it between 0 and 1 as probability is needed
			elif mini_board[val] == flag:
				mini_board_scores.append(1.0)
			else:
				mini_board_scores.append(0.0)

		#Get the bigger picture !!
		val = self.score_big_board(mini_board_scores)
	
		return val

	def __evaluate_Mini_Board(self, temp_board, index, flag):
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







		

