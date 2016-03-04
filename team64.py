import random

class Player64:

	def __init__(self):
		self.player_mark = 'Z'
		self.opponent_mark = 'Y'
		self.level = -1
		self.depth_limit = 2
		#self.states_map = {}
		#self.opponent_moves = []

	def move(self,temp_board,temp_block,old_move,flag):
		#print 'Entered move, prev move'+str(old_move)
		self.level += 1
		current_board_state = temp_board
		current_block_state = temp_block
		#List of permitted blocks, based on old move.
		#print 'Calling blocks allowed - '
		blocks_allowed = self.get_allowed_blocks(old_move, current_block_state)
		#print 'Blocks allowed + ' + str(blocks_allowed)
		self.player_mark = flag
		self.opponent_mark = self.compliment_mark(flag)
		#Get list of empty valid cells
		#print 'Allowed cars - '
		cells = self.get_actions(current_board_state, current_block_state, blocks_allowed)
		#print 'Allowed cells +' + str(cells)
		#print 'Status after move'
		if self.level <= 1:
			if old_move == (-1,-1):
				return (4,4)
			return cells[random.randrange(len(cells))]
		if self.level >= 4:
			self.depth_limit = 4
		#if self.level >= 11:
		#	self.depth_limit = 4
			#return self.early_decision(current_board_state, current_block_state, old_move, cells, flag)
		tpl = self.minimax_decision(current_board_state, current_block_state, cells, flag)
		#print_lists(current_board_state, current_block_state)
		return tpl

	def early_decision(self, current_board_state, current_block_state, old_move, actions, flag, ):
		mod1 = 0
		mod2 = 0
		if self.level == 0 or self.level == 4:
			mod1 = 0
			mod2 = 0
		elif self.level == 1:
			mod1 = 0
			mod2 = 2
		elif self.level == 2:
			mod1 = 2
			mod2 = 2
		else:
			mod1 = 2
			mod2 = 0
		for action in actions:
			if action[0]%3 == mod1 and action[1]%3 == mod2:
				#print 'Returned less than 4'
				return action
		return actions[random.randrange(len(actions))]

			


	def minimax_decision(self, current_board_state, current_block_state, actions, flag):
		#print 'Entered minimax_decision'
		#print 'Max-value alpha: ' + str(alpha) + ' beta: ' + str(beta)

		best_value = float("-infinity")
		alpha = float("-infinity")
		beta = float("infinity")
		if len(actions) == 0:
			print '*******List of actions empty ERROR*******'
		else:
			best_action = actions[0]
		for current_action in actions:
			block_wd, block_num = self.update_state(current_board_state, current_block_state, current_action, flag)
			current_min_value = self.min_value(current_board_state, current_block_state, alpha, beta, current_action, self.compliment_mark(flag), 0)
			if current_min_value > best_value:
				best_action = current_action
				best_value = current_min_value
			self.revert_state(current_board_state, current_block_state, current_action, block_wd, block_num)
			if best_value >= alpha:
				alpha = best_value
				#print 'Best value ' + str(best_value)
			#print 'Minimax Decision alpha: ' + str(alpha) + ' beta: ' + str(beta)

		return best_action


	def min_value(self, current_board_state, current_block_state, alpha, beta,  prev_action, flag, depth):
		#print 'Entered min value'
		#print 'Min-value alpha: ' + str(alpha) + ' beta: ' + str(beta)

		#print 'Depth = ' + str(depth)
		if self.terminal_test(current_board_state, current_block_state, depth) == True:
			#print 'return from terminal'
			return self.utility(current_board_state, current_block_state)

		blocks_allowed  = self.get_allowed_blocks(prev_action, current_block_state)
		actions = self.get_actions(current_board_state, current_block_state, blocks_allowed)
		best_min_value = float("infinity")
		for current_action in actions:
			block_wd, block_num = self.update_state(current_board_state, current_block_state, current_action, flag)
			current_max_value = self.max_value(current_board_state, current_block_state, alpha, beta, current_action, self.compliment_mark(flag), depth + 1)
			#print 'Current min value' + str(current_max_value)
			if current_max_value < best_min_value:
				best_min_value = current_max_value
			self.revert_state(current_board_state, current_block_state, current_action, block_wd, block_num)
			#print 'min compare 1'
			if best_min_value <= alpha:
				return best_min_value
			#print 'min compare 2'
			if best_min_value < beta:
				beta = best_min_value
			#print 'Min-value alpha: ' + str(alpha) + ' beta: ' + str(beta)

		return best_min_value

	def max_value(self, current_board_state, current_block_state, alpha, beta, prev_action, flag, depth):
		#print 'Entered max value'
		if self.terminal_test(current_board_state, current_block_state, depth) == True:
			return self.utility(current_board_state, current_block_state)

		blocks_allowed  = self.get_allowed_blocks(prev_action, current_block_state)
		actions = self.get_actions(current_board_state, current_block_state, blocks_allowed)
		best_max_value = float("-infinity")
		for current_action in actions:
			block_wd, block_num = self.update_state(current_board_state, current_block_state, current_action, flag)
			current_min_value = self.min_value(current_board_state,current_block_state, alpha, beta,  current_action, self.compliment_mark(flag), depth + 1)
			#print 'Current min value' + str(current_min_value)
			if current_min_value > best_max_value:
				best_max_value = current_min_value
			self.revert_state(current_board_state, current_block_state, current_action, block_wd, block_num)
			if best_max_value >= beta:
				return best_max_value
			if best_max_value >= alpha:
				alpha = best_max_value
			#print 'Max-value alpha: ' + str(alpha) + ' beta: ' + str(beta)

		return best_max_value

	def terminal_test(self, current_board_state, current_block_state, depth):
		flag = True
		for i in range(9):
			if current_block_state[i] == '-':
				flag = False
		if flag:
			return True
		if depth >= self.depth_limit:
			#print 'Returning true'
			return True
		else:
			return False

	def calculate_score(self, board_state, block_num, factor, mark):
		#print 'Entered calculate_score'
		#print 'Board state' + str(board_state)
		score = 0
		idx1 = (block_num/3)*3
		idx2 = (block_num%3)*3

		#First Diagonal
		if (board_state[idx1][idx2] == mark and board_state[idx1+1][idx2+1] == '-' and board_state[idx1+2][idx2+2] == '-') or (board_state[idx1+1][idx2+1] == mark and board_state[idx1][idx2] == '-' and board_state[idx1+2][idx2+2] == '-') or (board_state[idx1+2][idx2+2] == mark and board_state[idx1][idx2] == '-' and board_state[idx1+1][idx2+1] == '-'):
			score += (factor * 1)
		elif (board_state[idx1][idx2] == board_state[idx1 + 1][idx2 + 1] and board_state[idx1 + 2][idx2 + 2] == '-' and board_state[idx1][idx2] == mark) or (board_state[idx1 + 1][idx2 + 1] == board_state[idx1 + 2][idx2 + 2] and board_state[idx1 + 1][idx2 + 1] == mark and board_state[idx1][idx2] == '-') or (board_state[idx1][idx2] == board_state[idx1 + 2][idx2 + 2] and board_state[idx1 + 1][idx2 + 1] == '-' and board_state[idx1][idx2] == mark):
			score += (factor * 10)
		elif board_state[idx1][idx2] == board_state[idx1 + 1][idx2 + 1] and board_state[idx1 + 1][idx2 + 1] == board_state[idx1 + 2][idx2 + 2] and board_state[idx1][idx2] == mark:
			score += (factor * 100)
		
		#print 'Score D = ' + str(score)	
		#Second Diagonal
		if (board_state[idx1+2][idx2] == mark and board_state[idx1 + 1][idx2 + 1] == '-' and board_state[idx1][idx2 + 2] == '-') or (board_state[idx1+2][idx2] == '-' and board_state[idx1 + 1][idx2 + 1] == mark and board_state[idx1][idx2 + 2] == '-') or (board_state[idx1+2][idx2] == '-' and board_state[idx1 + 1][idx2 + 1] == '-' and board_state[idx1][idx2 + 2] == mark):
			score += (factor * 1)
		elif (board_state[idx1+2][idx2] == board_state[idx1 + 1][idx2 + 1] and board_state[idx1+2][idx2] == mark and board_state[idx1][idx2+2] == '-') or (board_state[idx1 + 1][idx2 + 1] == board_state[idx1][idx2 + 2] and board_state[idx1 + 1][idx2 + 1] == mark and board_state[idx1+2][idx2] == '-') or (board_state[idx1 + 2][idx2] == board_state[idx1][idx2 + 2] and board_state[idx1 + 2][idx2] == mark and board_state[idx1+1][idx2+1] == '-'): 
			score += (factor * 10)
		elif board_state[idx1+2][idx2] == board_state[idx1 + 1][idx2 + 1] and board_state[idx1 + 1][idx2 + 1] == board_state[idx1][idx2 + 2] and board_state[idx1 + 2][idx2] == mark:
			score += (factor * 100)
			
		#Rows
		for i in range(idx1,idx1+3):
			if (board_state[i][idx2] == mark and board_state[i][idx2+1] == '-' and board_state[i][idx2+2] =='-') or (board_state[i][idx2] == '-' and board_state[i][idx2+1] == mark and board_state[i][idx2+2] =='-') or (board_state[i][idx2] == '-' and board_state[i][idx2+1] == '-' and board_state[i][idx2+2] ==mark):
				score += (factor * 1)
			elif (board_state[i][idx2] == board_state[i][idx2 + 1] and board_state[i][idx2] ==mark and board_state[i][idx2 + 2] == '-') or (board_state[i][idx2 + 1] == board_state[i][idx2 + 2] and board_state[i][idx2 + 1] == mark and board_state[i][idx2] == '-') or (board_state[i][idx2] == board_state[i][idx2 + 2] and board_state[i][idx2] == mark and board_state[i][idx2+1] == '-'):
				score += (factor * 10)
			elif board_state[i][idx2] == board_state[i][idx2 + 1] and board_state[i][idx2 + 1] == board_state[i][idx2 + 2] and board_state[i][idx2] == mark:
				score += (factor * 100)

		#Columns
		for i in range(idx2,idx2+3):
			if (board_state[idx1][i] == mark and board_state[idx1+1][i] == '-' and board_state[idx1+2][i] == '-') or (board_state[idx1][i] == '-' and board_state[idx1+1][i] == mark and board_state[idx1+2][i] == '-') or (board_state[idx1][i] == '-' and board_state[idx1+1][i] == '-' and board_state[idx1+2][i] == mark):
				score += (factor * 1)
			elif (board_state[idx1][i] == board_state[idx1+1][i] and board_state[idx1][i] == mark and board_state[idx1+2][i] =='-') or (board_state[idx1+1][i] == board_state[idx1+2][i] and board_state[idx1+1][i] == mark and board_state[idx1][i] == '-') or (board_state[idx1][i] == board_state[idx1+2][i] and board_state[idx1][i] == mark and board_state[idx1+1][i] == '-'):
				score += (factor * 10)
			elif board_state[idx1][i] == board_state[idx1+1][i] and board_state[idx1+1][i] == board_state[idx1+2][i] and board_state[idx1][i] == mark:
				score += (factor * 100)

		#print 'Score = ' + str(score)
		return score


	def calc_prob_score(self, vec_sum):
		sum_score = 0

		if vec_sum > 1 and vec_sum < 2:
			sum_score += (vec_sum - 1)*9 + 1
		elif vec_sum > 2:
			sum_score += 10 + (vec_sum - 2)*90
		elif vec_sum > 0:
			sum_score += vec_sum
		elif vec_sum < 0 and vec_sum > -1:
			sum_score += vec_sum
		elif vec_sum <= -1 and vec_sum > -2:
			sum_score += (-1 + (vec_sum - 1)*9)
		elif vec_sum <= -2:
			sum_score += (-10 + (vec_sum - 2)*90)

		return sum_score

	def get_signature(self, current_board_state, block_num):
		idx1 = (block_num/3)*3
		idx2 = (block_num%3)*3
		signature = 0
		power = 0
		num = 0
		for i in range(idx1,idx1 + 3):
			for j in range(idx2,idx2 + 3):
				if current_board_state[i][j] == '-':
					num = 0
				elif current_board_state[i][j] == 'x':
					num = 1
				else:
					num = 2
				signature += (3 ** power) * num
				power += 1

		return signature





	def utility(self, current_board_state, current_block_state):
		#print 'Entered utiluty'
		sum_score = 0
		max_score = 1
		signature = 0
		board_utility = [[0.0 for j in range(3)] for i in range(3)]
		for block_num in range(8):
			#signature = 1 #self.get_signature(current_board_state, block_num)
			#print 'signature: ' + str(signature)
			#if False and signature in self.states_map:
			#	board_utility[row][col] = self.states_map[signature]
			
			#print 'Entered'
			row = block_num/3
			col = block_num%3
			board_utility[row][col] += self.calculate_score(current_board_state, block_num, 1, self.player_mark)
			board_utility[row][col] += self.calculate_score(current_board_state, block_num, -1, self.opponent_mark)
			#print 'Board utility: ' + str(board_utility[row][col])
			#self.states_map[signature] = board_utility[row][col]
			#print 'Came here after adding hash'
			#print 'New state added, signature: ' + str(signature) 
 			if max_score < board_utility[row][col]:
				max_score = board_utility[row][col]
			#sum_score += board_utility[row][col]
			#print 'Score for block = '+str(block_num)+" is = "+ str(sum_score)
		
		for block_num in range(8):
			row = block_num/3
			col = block_num%3
			board_utility[row][col] = board_utility[row][col]/float(max_score)
			#print 'Board utility is = ' + str(board_utility[row][col])


		#diagonals
		diag_sum = board_utility[0][0] + board_utility[1][1] + board_utility[2][2]
		#print 'Diag sum = ' + str(diag_sum)
		sum_score += self.calc_prob_score(diag_sum)

		#print 'Sum score = ' + str(sum_score)

		diag_sum = board_utility[2][0] + board_utility[1][1] + board_utility[0][2]
		sum_score += self.calc_prob_score(diag_sum)

		#rows
		for i in range(0,3):
			row_sum = board_utility[i][0] + board_utility[i][1] + board_utility[i][2]
			sum_score += self.calc_prob_score(row_sum)
			

		for i in range(0,3):
			col_sum = board_utility[0][i] + board_utility[1][i] + board_utility[2][i]
			sum_score += self.calc_prob_score(col_sum)
			

		#print 'Final score to be returned' + str(sum_score)
		return sum_score
		
	def compliment_mark(self, flag):
		if flag == 'x':
			return 'o'
		elif flag == 'o':
			return 'x'
		else:
			return 'Z'
		
	def get_allowed_blocks(self, prev_move, block_status):
		#print 'Entered get allowed block**'
		#print 'Prev move: ' + str(prev_move)
		blocks = []
		if prev_move[0]%3 == 0 and prev_move[1]%3 == 0:
			blocks = [1, 3]
		elif prev_move[0]%3 == 0 and prev_move[1]%3 == 1:
			blocks = [0, 2]
		elif prev_move[0]%3 == 0 and prev_move[1]%3 == 2:
			blocks = [1, 5]
		elif prev_move[0]%3 == 1 and prev_move[1]%3 == 0:
			blocks = [0, 6]
		elif prev_move[0]%3 == 1 and prev_move[1]%3 == 1:
			blocks = [4]
		elif prev_move[0]%3 == 1 and prev_move[1]%3 == 2:
			blocks = [2, 8]
		elif prev_move[0]%3 == 2 and prev_move[1]%3 == 0:
			blocks = [3, 7]
		elif prev_move[0]%3 == 2 and prev_move[1]%3 == 1:
			blocks = [6, 8]
		elif prev_move[0]%3 == 2 and prev_move[1]%3 == 2:
			blocks = [5, 7]

		#print 'Permitted blocks till now: ' + str(blocks)

		allowed_blocks = []
		for block_num in blocks:
			if block_status[block_num] == '-':
				allowed_blocks.append(block_num)
		#print 'Returning allowed_blocks' + str(allowed_blocks)

		return allowed_blocks

	def update_state(self, board_state, block_state, action, flag):

		board_state[action[0]][action[1]] = flag

		block_num = (action[0]/3)*3 + action[1]%3
		#Coordinates of top left cell of the modified block
		idx1 = (block_num/3)*3
		idx2 = (block_num%3)*3
		dflag = False

		if block_state[block_num] == 'D':
			dflag = True
		else:
			for i in range(3):
				for j in range(3):
					if board_state[idx1 + i][idx2 + j] == '-':
						dflag = True

		if dflag == False:
			#print 'Made block num: ' + str(block_num) + 'Draw' 
			block_state[block_num] = 'D'

		flag = False

		if block_state[block_num] == '-':
			#Checking diagonals
			if board_state[idx1][idx2] == board_state[idx1 + 1][idx2 + 1] and board_state[idx1 + 1][idx2 + 1] == board_state[idx1 + 2][idx2 + 2] and board_state[idx1][idx2] != '-':
				flag = True
			elif board_state[idx1+2][idx2] == board_state[idx1 + 1][idx2 + 1] and board_state[idx1 + 1][idx2 + 1] == board_state[idx1][idx2 + 2] and board_state[idx1 + 2][idx2] != '-':
				flag = True

			#Checking rows
			if flag != True:
				for i in range(idx1,idx1+3):
					if board_state[i][idx2] == board_state[i][idx2 + 1] and board_state[i][idx2 + 1] == board_state[i][idx2 + 2] and board_state[i][idx2] != '-':
						flag = True
						break
			#Checking columns
			if flag != True:
				for i in range(idx2,idx2+3):
					if board_state[idx1][i] == board_state[idx1+1][i] and board_state[idx1+1][i] == board_state[idx1+2][i] and board_state[idx1][i] != '-':
						flag = True
						break

		if dflag == False:
			return True,block_num

		if flag == True:
			block_state[block_num] = flag
			return True,block_num
		else:
			return False,-1


	def revert_state(self, board_state, block_state, action, block_wd, block_num):
		board_state[action[0]][action[1]] = '-'
		if block_wd:
			block_state[block_num] = '-'

	def get_actions(self, board_state, block_state, blocks_allowed):
		actions = []
		#print 'Blocks allowed: ' + str(blocks_allowed)
		#print 'Block state' + str(block_state)
		for block_num in blocks_allowed:
			#Coordinates of top left cell of the modified block
			idx1 = (block_num/3)*3
			idx2 = (block_num%3)*3
			for i in range(idx1, idx1 + 3):
				for j in range(idx2, idx2 + 3):
					if board_state[i][j] == '-':
						actions.append((i,j))

		if actions == []:
			#print 'Provided blocks already filled'
			for block_num in range(0,9):
				if block_state[block_num] != '-':
					continue
				idx1 = (block_num/3)*3
				idx2 = (block_num%3)*3
				for i in range(idx1, idx1 + 3):
					for j in range(idx2, idx2 + 3):
						if board_state[i][j] == '-':
							actions.append((i,j))

		return actions

