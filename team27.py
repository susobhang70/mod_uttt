import random
import copy
import sys

class Player27():

	def __init__(self):
		self.WINNING_COMBOS = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
		self.FIRST = False
		self.ALPHA_BETA_DEPTH = 3
		self.max = 9223372036854775807

	MAX = 9223372036854775807

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

		if (len(cells) >= 2):
			self.ALPHA_BETA_DEPTH = 2
		else:
			self.ALPHA_BETA_DEPTH = 3

		for cell in cells:
			successor_board = self.generate_successor(temp_board, cell, flag)
			next_moves.append((cell, self.__min_val_ab(successor_board, self.ALPHA_BETA_DEPTH, temp_block, old_move, flag)))
		_, best_value = max(next_moves, key=lambda x: x[1])
		return random.choice([best_action for best_action, val in next_moves if val == best_value])

		#sys.exit(1)

		#Choose a move based on some algorithm, here it is a random move.
		return cells[random.randrange(len(cells))]
		#return (4,4)

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

	def generate_successor(self, temp_board, cell, flag):
		board = copy.deepcopy(temp_board)
		board[cell[0]][cell[1]] = flag
		return board

	def __min_val_ab(self, temp_board, depth, temp_block, old_move, flag, alpha=-(MAX), beta=(MAX)):	
		if self.terminal_test(temp_board, depth, temp_block):
			return self.__eval_state(temp_board, temp_block, flag)
		val = (self.max)

		blocks_allowed  = self.determine_blocks_allowed(old_move, temp_block)
		cells = self.get_empty_out_of(temp_board, blocks_allowed, temp_block)

		for cell in cells:
			successor_board = self.generate_successor(temp_board, cell, flag)
			val = min(val, self.__max_val_ab(successor_board,  depth - 1, temp_block, old_move, flag, alpha, beta))
			if val <= alpha:
				return val
			beta = min(beta, val)
		return val

	def __max_val_ab(self, temp_board, depth, temp_block, old_move, flag, alpha=-(MAX), beta=(MAX)):
		if self.terminal_test(temp_board, depth, temp_block):
			return self.__eval_state(temp_board, temp_block, flag)
		val = -(self.max)

		blocks_allowed  = self.determine_blocks_allowed(old_move, temp_block)
		cells = self.get_empty_out_of(temp_board, blocks_allowed, temp_block)

		for cell in cells:
			successor_board = self.generate_successor(temp_board, cell, flag)
			val = max(val, self.__min_val_ab(successor_board, depth, temp_block, old_move, flag, alpha, beta))
			if val >= beta:
				return val
			alpha = max(alpha, val)
		return val

	def terminal_test(self, temp_board, depth, temp_block):
		if depth==0:
			return True
		#a,b =  self.terminal_state_reached(temp_board, temp_block)
		#return a

	def __eval_state(self, temp_board, temp_block, flag):
		uttt_board = copy.deepcopy(temp_board)
		mini_board = copy.deepcopy(temp_block)

		'''
		if self.get_winner(temp_block) != False:
			free_cells = 0
			for i in xrange(9):
				for j in xrange(9):
					if uttt_board[i][j] == '-':
						free_cells += 1
			return self.WIN_SCORE + free_cells if self.get_winner(temp_block) == flag else -self.WIN_SCORE - free_cells
		
		if self.is_board_full(uttt_board):
			return 0

		board_as_mini = []
		for i in xrange(9):
			board_as_mini.append(temp_block[i])

		ret = self.__assess_miniB(board_as_mini, flag) * self.BIG_BOARD_WEIGHT
		for i in xrange(9):
			if temp_block[i] == '-':
				miniB = self.get_miniBoard(uttt_board,i)
				if '-' in miniB:
					ret += self.__assess_miniB(miniB, flag)
		return ret
		'''
		return random.randrange(100)
