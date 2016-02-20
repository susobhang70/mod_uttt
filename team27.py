import random
import copy

class Player27():

	def __init__(self):
		pass

	def move(self, temp_board, temp_block, old_move, flag):
		# board: is the list of lists that represents the 9x9 grid
		# board[i] can be 'x', 'o' or '-'
		# block: is a list that represents if a block is won or available to play in
		# block[i] can be 'x', 'o' or '-'
		# old_move: is a tuple of integers representing co-ordintates of the last move made. For the first move of game it is (-1,-1)
		# flag: is your marker. it can be 'x' or 'o'.
		#List of permitted blocks, based on old move.
		blocks_allowed  = self.determine_blocks_allowed(old_move, temp_block)
		#Get list of empty valid cells
		cells = self.get_empty_out_of(temp_board, blocks_allowed,temp_block)
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
