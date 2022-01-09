from os import fdopen
from typing import DefaultDict
import numpy as np
import random
from numpy.lib.function_base import _diff_dispatcher, diff

from numpy.testing._private.utils import _assert_valid_refcount
from c4 import gameBoard
from copy import deepcopy
import math
import pickle
import pyautogui

import time

start_time = time.time()

class Node:
    def __init__(self, gameBoard, parent: object = None, symbol: str = 1):
        self.gb = gameBoard
    
        self.state = deepcopy(self.gb.board)

        self.rows, self.columns = 6,7

        self.parent = parent
        self.childs = []

        self.legal_actions = self.gb.get_legal_actions()
        self.untried_actions = self.gb.get_legal_actions()
        self.wins = 0
        self.visits = 0
        self.ucb1 = self.calculate_ucb1()

        self.symbol = symbol

        self.action = None

    def calculate_ucb1(self):
        if(self.visits == 0):
            return math.inf
        ####aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        if(self.parent.parent == None):
            self.parent.visits = 0
            for child in self.parent.childs:
                self.parent.visits += child.visits
        ########################################a
        #print(self.wins/self.visits + np.sqrt(2)*np.sqrt(np.log(self.parent.visits)/self.visits))
        return self.wins/self.visits + np.sqrt(2)*np.sqrt(np.log(self.parent.visits)/self.visits)

    def select(self):
        foo = lambda x:  x.ucb1
        return sorted(self.childs,key=foo)[-1]

    def expand(self):
        temp_action = random.choice(self.untried_actions)
       
        self.untried_actions.remove(temp_action)

        if(self.symbol == 1):
            new_symbol = 2
        else:
            new_symbol = 1

        new_state = self.gb.move(new_symbol,temp_action)

        new_gb = gameBoard.gameBoard(new_state)
        child = Node(new_gb,self,new_symbol)
        ###############################
        child.action = temp_action
        ###############################
        self.childs.append(child)
        
        return child

    def simulate(self):

        gb = deepcopy(self.gb)
        isFinished, winner = gb.isTerminal()
        symbol = deepcopy(self.symbol)
        while not(isFinished):
            if(symbol == 1):
                symbol = 2
            else:
                symbol = 1
                
            gb.board = gb.move(symbol,random.choice(gb.get_legal_actions()))

            isFinished, winner = gb.isTerminal()
        return winner

    def update(self, winner):
        if(self.symbol == winner or "TIE" == winner):
            self.wins += 1
        self.visits += 1
    
    def backprop(self,winner):
        node = self
        while node.parent is not None:
            node.update(winner)
            node.ucb1 = node.calculate_ucb1()
            node = node.parent

if __name__ == "__main__":
    state = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0]]
    root_gb = gameBoard.gameBoard(board=state)
    root_node = Node(gameBoard=root_gb) 
    current_node = root_node
    for i in range(80000000):

        if(i % 10000 == 0):        
            pyautogui.press("alt")                
        if(len(current_node.untried_actions) == 0):
            isFinished,winner = current_node.gb.isTerminal()
            if(isFinished):
                current_node.backprop(winner)
                current_node.gb.printBoard()
                current_node = root_node
            else:
                current_node = current_node.select()  
            
        else:    
            current_node = current_node.expand()

            winner = current_node.simulate()
            
            current_node.backprop(winner)
            current_node.gb.printBoard()
            
            current_node = root_node
            print(i)
     
   # with open('/Users/martintin/Desktop/connect4/root_node.pickle', 'wb') as f:
  #      pickle.dump(root_node, f)
#aaaaaaaaaaaaa
    print("Process finished --- %s seconds ---" % (time.time() - start_time))


    def check_childs(node,state,the_node):
        for child in node.childs:
            if(the_node[0] != None):
                break
            if(child.state == state):
                the_node[0] = child
        
        if(the_node[0] == None):
            for child in node.childs:
                check_childs(child,state,the_node)
                if(the_node[0] != None):
                    break

    def best_move(state,symbol):
        the_node = [None]
        if(root_node.state == state):
            the_node[0] = root_node
        else:
            check_childs(root_node,state,the_node)

        foo = lambda x:  x.visits
        a = the_node[0].childs
        action = sorted(a,key=foo)[-1].action
        return action
        
        

    state = [[0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0]]
    gb = gameBoard.gameBoard(state)

    symbol = 1

    isFinished, winner = gb.isTerminal()
    while not(isFinished):
        print("HI")
        if(symbol == 1):
            symbol = 2
        else:
            symbol = 1
        gb.board = gb.move(symbol,best_move(gb.board,symbol))
        gb.printBoard()
        isFinished, winner = gb.isTerminal()

    while(True):
        symbol = 0
        computerFirst = False
        if(input("do u want to go first (y for yes, n for no)") == "y"):
            symbol = 1
        else:
            symbol = 2

    
        while not(isFinished):
            if(symbol == 1):
                symbol = 2
                gb.board = gb.move(symbol,int(input("Enter move: ")))
            elif(symbol == 2):
                symbol = 1
                gb.board = gb.move(symbol, best_move(gb.board,symbol))
            gb.printBoard()
            isFinished, winner = gb.isTerminal()
        print("PLAY AGAIN")

        """
       ---------
|0000000|
|0000000|
|0000100|
|0020200|
|0010200|
|0120120|
---------


        """







    """

    --------
    |      |
    |XOXOXO|
    |XOXOXO|
    |XOXOXO|
    |XOXOXO|
    |XOXOXO|
    |XOXOXO|
    --------
    ---------
    |0211200|
    |0122121|
    |0211121|
    |2122112|
    |1211221|
    |2122122|
    ---------
    18410069


    ---------
    |2201211|
    |1102122|
    |2211121|
    |1122112|
    |2211221|
    |1122122|
    ---------
    20848053
    """

