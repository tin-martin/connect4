import numpy as np
class gameBoard:
	def __init__(self,columns,rows):
		self.columns = columns
		self.rows  =  rows
		self.board = [[" " for i in range(columns)] for i in range(rows)]
	def getBoard(self):
		return self.board
	def printBoard(self):
		for i in range(self.rows+2):
			print("-",end="")
		print()
		for i in range(len(self.board[0])):
			print("|",end="")
			for j in range(len(self.board)):
				print(self.board[j][i], end="")
			print("|")
		for i in range(self.rows+2):
			print("-",end="")
		print()
	def setBoard(self, new_board):
		self.board = new_board
	def check_straight(self,board,x,y):
		symbol = board[x][y]
		if(board[x][y] == symbol and board[x][y+1] == symbol and board[x][y+2] == symbol and board[x][y+3] == symbol):
			return True
		return False
	def check_diagonal(self,board,x,y):
		symbol = board[x][y]
		if(board[x][y] == symbol and board[x+1][y+1] == symbol and board[x+2][y+2] == symbol and board[x+3][y+3] == symbol):
			return True
		return False
	def check(self,symbol):
		board_tbc = np.array(self.board)
		for z in range(4):
			for x in range(len(board_tbc.tolist())):
				for y in range(len(board_tbc.tolist()[0])):
					if board_tbc[x][y] != ' ':	
						try:
							if(self.check_diagonal(board_tbc.tolist(),x,y) or self.check_straight(board_tbc.tolist(),x,y)):
								if(board_tbc[x][y] == symbol):
									return "win"
								else:
									return "loss"
						except:
							pass
			board_tbc = np.rot90(board_tbc,axes=(1,0))	
		return "incomplete"


