import numpy as np
import random, math, time
from copy import deepcopy

from c4 import gameBoard

class Node:
    def __init__(self, gameBoard, parent: object = None, symbol: str = "X"):
        self.gb = gameBoard    
        self.state = self.gb.board

        self.rows, self.columns = 6,7

        self.parent = parent
        self.childs = []

        self.legal_actions = self.gb.get_legal_actions()
        self.untried_actions = self.gb.get_legal_actions()

        self.wins = 0
        self.visits = 0
        self.ucb1 = self.calculate_ucb1()

        self.symbol = symbol

        self.pAction = None


    def calculate_ucb1(self):
        if(self.visits == 0):
            return 0
        
        return self.wins/self.visits + np.sqrt(2)*np.sqrt(np.log(self.parent.visits)/self.visits)

    def select(self):
        foo = lambda x: x.ucb1
        return sorted(self.childs,key=foo)[-1]

    def expand(self):
        temp_action = random.choice(self.untried_actions)
       
        self.untried_actions.remove(temp_action)

        if(self.symbol == "X"):
            new_symbol = "O"
        else:
            new_symbol = "X"

        new_state = self.gb.move(new_symbol,temp_action)

        new_gb = gameBoard.gameBoard(new_state)
        child = Node(new_gb,self,new_symbol)
        child.pAction = temp_action
        self.childs.append(child)
        
        return child

    def simulate(self):

        gb = deepcopy(self.gb)
        isFinished, winner = gb.isTerminal()
        symbol = deepcopy(self.symbol)
        while not(isFinished):
            if(symbol == "X"):
                symbol = "O"
            else:
                symbol = "X"
            gb.board = gb.move(symbol,random.choice(gb.get_legal_actions()))
            isFinished, winner = gb.isTerminal()
            

        return winner

    def update(self, winner):
        if(self.symbol == winner or "TIE" == winner):
            self.wins += 1
        self.parent.visits += 1
    
    def backprop(self,winner):
        node = self
        node.visits += 1

        while node.parent is not None:
            node.update(winner)
            node.ucb1 = node.calculate_ucb1()
            node = node.parent

if __name__ == "__main__":
    start_time = time.time()
    state = [[' ', ' ', ' ', ' ', ' ', ' '],[' ', ' ', ' ', ' ', ' ', ' '],[' ', ' ', ' ', ' ', ' ', ' '],[' ', ' ', ' ', ' ', ' ', ' '],[' ', ' ', ' ', ' ', ' ', ' '],[' ', ' ', ' ', ' ', ' ', ' '],[' ', ' ', ' ', ' ', ' ', ' ']]
    root_gb = gameBoard.gameBoard(board=state)
    root_gb.printBoard()
    root_node = Node(gameBoard=root_gb)
    current_node = root_node

    for i in range(100000000):
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

    print("Process finished --- %s seconds ---" % (time.time() - start_time))

    def check_childs(node,state,the_node):
        for child in node.childs:                                                                                                         
            if(the_node != None): 
                break
            if(child.state == state):
                the_node = child
        
        if(the_node == None):
            for child in node.childs:
                if(the_node != None):
                    break
                check_childs(child,state,the_node)

    def best_move(state,symbol):
        the_node = None
        if(root_node.state == state):
            the_node = root_node
        else:
            check_childs(root_node,state,the_node)

        foo = lambda x:  x.visits
        action = sorted(the_node.childs,key=foo)[-1].pAction
        return action
        
        

    oState = state = [[' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ']]
    gb = gameBoard.gameBoard(state)

    symbol = "X"

    isFinished, winner = gb.isTerminal()
    while not(isFinished):
        symbol = "O"
        gb.move(symbol,best_move(gb.board,symbol))
        gb.printBoard()
        isFinished, winner = gb.isTerminal()

    if(winner == "X"):
        print("""
██╗    ██╗██╗███╗   ██╗███╗   ██╗███████╗██████╗        ██╗  ██╗    
██║    ██║██║████╗  ██║████╗  ██║██╔════╝██╔══██╗██╗    ╚██╗██╔╝    
██║ █╗ ██║██║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝╚═╝     ╚███╔╝     
██║███╗██║██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗██╗     ██╔██╗     
╚███╔███╔╝██║██║ ╚████║██║ ╚████║███████╗██║  ██║╚═╝    ██╔╝ ██╗    
╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝       ╚═╝  ╚═╝    
        """)
    else:
        print("""
██╗    ██╗██╗███╗   ██╗███╗   ██╗███████╗██████╗         ██████╗ 
██║    ██║██║████╗  ██║████╗  ██║██╔════╝██╔══██╗██╗    ██╔═══██╗
██║ █╗ ██║██║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝╚═╝    ██║   ██║
██║███╗██║██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗██╗    ██║   ██║
╚███╔███╔╝██║██║ ╚████║██║ ╚████║███████╗██║  ██║╚═╝    ╚██████╔╝
 ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝        ╚═════╝                                                  
        """)


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


"""