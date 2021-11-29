import numpy as np
import random
from c4 import gameBoard, Player
from copy import deepcopy
import math

class Node:
	def __init__(self,state: tuple = None,parent: object = None, symbol: str = None):
		self.state = state
		self.parent = parent
		self.childs = []
		self.legal_actions = self.get_legal_actions()

		self.untried_actions = deepcopy(self.legal_actions)
		#self.untried_actions = self.legal_actions()


		self.win = 0
		self.simulations = 0
		self.c = math.sqrt(2)

		self.ucb1 = self.calculate_ucb1()

		self.rows = 6
		self.columns = 7

		self.symbol = symbol
		if(symbol == None):
			self.symbol = "X"

	def calculate_ucb1(self):
		if(self.parent == None):
			self.parent_simulations = 0
		else:
			self.parent_simulations = self.parent.simulations
		try:
			ucb1 = (self.win/self.simulations) + self.c*(math.log(self.parent_simulations)/self.simulations)
			self.ucb1 = ucb1
			return ucb1
		except:
			return 0

	def get_legal_actions(self):  
		legal_actions = []
		for i in range(6):
			if(self.state[i][0] == " "):
				legal_actions.append(i)
		self.legal_actions = legal_actions
		return legal_actions

    
	def printBoard(self):
		for i in range(self.rows+2):
			print("-",end="")
		print("")
		for i in range(len(self.state[0])):
			print("|",end="")
			for j in range(len(self.state)):
				print(self.state[j][i], end="")
			print("|")
		for i in range(self.rows+2):
			print("-",end="")
		print("")
	
	def move(self, row):
		board = deepcopy(self.state)
		symbol = self.symbol 

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
		board_tbc = np.array(deepcopy(self.state))
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
				return True, "T"
			board_tbc = np.rot90(board_tbc,axes=(1,0))	
		return False, ""

class mctsAgent:
	def __init__(self,state):

		self.root_state = deepcopy(state)
		#does a move
		self.root_node = Node(self.root_state)

	def print_childs(self,node): 
		for child in node.childs:
			print(child.simulations,end="\t")
		print("")
		for child in node.childs:
			self.print_childs(child)

	def print_tree(self):
		self.print_childs(self.root_node)

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
	def isTerminal(self,board):
			board_tbc = np.array(board)
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
			return False, ""



	def select(self,node):
		if(len(node.untried_actions) == 0):
			_max = 0
			i = 0 
			for i in range(len(node.childs)):
				if(node.childs[i].ucb1 > _max):
					_max = node.childs[i].ucb1 
			child = node.childs[i]
			self.select(child)

		else:
			isEnd, winner = node.isTerminal()
			if(isEnd):
				update(node,winner)
			else:
				new_state, action = self.expand(node)
				if(node.symbol == "X"):
					new_symbol = "O"
				else:
					new_symbol = "X"

				child = Node(new_state,node,new_symbol)

				node.childs.append(child)
				return child;
				
				


	def expand(self,node):
		temp_action = random.choice(node.untried_actions)
		node.untried_actions.remove(temp_action)

		return node.move(temp_action), temp_action
			
	def simulate(self,node):
		#from node, get all possible randoms and select one, repeat
		temp_node = deepcopy(node)

	#	def __init__(self,state: tuple = None,parent: object = None, symbol: str = None):
		while(True):
			new_state = temp_node.move(random.choice(temp_node.get_legal_actions()))
			if(temp_node.symbol == "X"):
				new_symbol = "O"
			else:
				new_symbol = "X"
			child = Node(new_state, temp_node,new_symbol)
			temp_node.childs.append(child)
			isEnd, winner = self.isTerminal(child.state)
			if not (isEnd):
				temp_node = child
				continue
			else:
				child.printBoard()
				self.backprop(node,winner)
				break

	def update(self,node,winner):
		if(node.symbol == winner):
			node.win += 1
		node.simulations += 1
		node.calculate_ucb1()


	def backprop(self,node,winner):

		temp_node = node
		while(temp_node.parent != None):
			self.update(temp_node,winner)
			temp_node = temp_node.parent


		

	def runSearch(self,state,timeout):
		pass
	def bestPlay(self,state):
		pass

if __name__ == "__main__":
	state = [[' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ']]
	for i in range(3):
		agent = mctsAgent(state)
		child_node = agent.select(agent.root_node)
		agent.simulate(child_node)



	agent.print_tree()

