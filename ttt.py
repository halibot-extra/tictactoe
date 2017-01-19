from halibot import HalModule

class Game():

	def __init__(self, n=3):
		self.board = [ ' ' * n ] * n
		self.n = n
		self.mover = 0

	# Return values:
	#   'X' - X won
	#   'O' - O won
	#   ' ' - Game ongoing
	#   None - Tie
	def is_victor(self):
		# Check rows and columns
		for i in range(0, self.n):
			row = self.board[i][0]
			col = self.board[0][i]
			win_row = win_col = True

			for j in range(1, self.n):
				if row != self.board[i][j]: win_row = False
				if col != self.board[j][i]: win_col = False

			if win_row: return row
			if win_col: return col

		# Check diagonals
		pos = self.board[0][0]
		neg = self.board[0][-1]
		win_pos = win_neg = True

		for i in range(1, self.n):
			if pos != self.board[i][i]:    win_pos = False
			if neg != self.board[i][-1-i]: win_neg = False

		if win_pos: return pos
		if win_neg: return neg

		# Check for tie
		tie = True
		for i in range(0, self.n):
			if ' ' in self.board[i]:
				# Game ongoing
				return ' '

		# It was a tie
		return None

	def move(self, row, col):
		# TODO extrapolate to N players?
		pieces = 'XO'

		if self.board[row][col] != ' ':
			return False

		self.board[row] = self.board[row][:col] + pieces[self.mover] + self.board[row][col+1:]
		self.mover = (self.mover + 1) % 2
		return True

	def draw_board(self):
		s = ''
		for i in range(0, self.n):

			# Make vertical divier
			if i != 0:
				for j in range(0, self.n):
					if j != 0:
						s += '+'
					s += '-'
				s += '\n'

			# Make row
			for j in range(0, self.n):
				if j != 0:
					s += '|'
				s += self.board[i][j]
			s += '\n'
		return s

class TicTacToe(HalModule):

	def init(self):
		self.game = None

	def new_game(self, msg):
		if self.game != None:
			self.reply(msg, body='A game is already begun!')
		else:
			self.game = Game()
			self.reply(msg, body='Game start.')

	def move(self, msg, row, col):
		if self.game == None:
			self.reply(msg, body='There is no ongoing game!')
		else:
			self.game.move(row+1, col+1)
			result = self.game.is_victor()

			if result != ' ':
				# The game is done
				if result == 'X':
					txt = 'X wins!'
				elif result == 'O':
					txt = 'O wins!'
				else:
					txt = 'The game tied.'
					if math.randint(0,20) == 0:
						txt = 'The only winning move is not to play.'
				self.game = None
			else:
				txt = self.game.draw_board()

			self.reply(msg, body=txt)

	def usage(self, msg):
		self.reply(msg, body='usage: "!tictactoe new" or "!tictactoe [row] [column]"')

	def receive(self, msg):
		args = msg.body.split(' ')

		if len(args) > 0 and args[0] == '!tictactoe':
			
			if len(args) == 2 and args[1] == 'new':
				self.new_game(msg)
			elif len(args) == 3 and args[1].isdigit() and args[2].isdigit():
				self.move(msg, int(args[1]), int(args[2]))
			else:
				self.usage(msg)

