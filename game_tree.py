import itertools 
from update_game_state import update_game_state
from collections import Counter
import copy

class Node:
    def __init__(self,game_state):
        self.game_state = game_state
        self.children = []
        self.move = ""
        self.score = -2**10
    def add_child(self,child_node):
        self.children.append(child_node)
    def score_this(self, value):
        self.score = value

def create_tree(node, depth, our_turn):
    moves = ["up","right","down","left"]
    if depth == 0:
        return 
    if our_turn == True:
        for move in moves:
            new_game_state = copy.deepcopy(node.game_state)
            new_game_state = update_game_state(new_game_state,move,True)
            child_node = Node(new_game_state)
            child_node.move = move
            node.add_child(child_node)
            create_tree(child_node,depth - 0.5, False)
    else:
        #print("====")
        #print(node.game_state)
        #print("====")

        #print(len(node.game_state["board"]["snakes"]))
        if len(node.game_state) == 0:
            return 
        
        for move in itertools.product(moves,repeat = len(node.game_state["board"]["snakes"])):
            new_game_state = copy.deepcopy(node.game_state)
            new_game_state = update_game_state(new_game_state,move,False)
            child_node = Node(new_game_state)
            node.add_child(child_node)
            create_tree(child_node, depth - 0.5, True)