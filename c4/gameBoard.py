import numpy as np
from copy import deepcopy
class gameBoard:
	def __init__(self, board):
		self.rows = 6
		self.columns  =  7
		self.board = board
	def getBoard(self):
		return self.board
	def printBoard(self):
		for i in range(self.rows+2):
			print("-",end="")
		print("")
		for i in range(len(self.board[0])):
			print("|",end="")
			for j in range(len(self.board)):
				print(self.board[j][i], end="")
			print("|")
		for i in range(self.rows+2):
			print("-",end="")
		print("")
		
	def setBoard(self, new_board):
		self.board = new_board
#_________________
	def move(self, symbol,row):
		
		board = deepcopy(self.getBoard())

		if(board[row][0] != " "):
			raise ValueError('A very specific bad thing happened.')

		for i in range(len(board[row])):
			if (board[row][i] != " "):
				board[row][i-1] = symbol
				break
			if(i == len(board[row])-1):
				board[row][i] = symbol			
		return board
#__________________
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
	def isTerminal(self):
		board_tbc = deepcopy(np.array(self.board))
		isTie = True
		for z in range(4):
			for x in range(len(board_tbc.tolist())):
				for y in range(len(board_tbc.tolist()[0])):

					if board_tbc[x][y] != ' ':	
						
						try:
							if(self.check_diagonal(board_tbc.tolist(),x,y) or self.check_straight(board_tbc.tolist(),x,y)):
								return True, board_tbc[x][y]
						except:
							pass
					else:
						isTie = False
							
			if(isTie):
				return True, "TIE"
				
			board_tbc = np.rot90(board_tbc,axes=(1,0))	
		return False, " "

	def get_legal_actions(self):
		legal_actions = []
		for i in range(self.rows):
			if(self.board[i][0] == " "):
				legal_actions.append(i)
		return legal_actions



