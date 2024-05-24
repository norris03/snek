# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "snek14",  # TODO: Your Battlesnake Username
        "color": "#FFFF00",  # TODO: Choose color
        "head": "fang",  # TODO: Choose head
        "tail": "block-bum",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
from minimax import *
from game_tree import *
from update_game_state import clean_game_state
def move(game_state: typing.Dict) -> typing.Dict:
    # Wir müssen auf jeden Fall noch implementieren,
    # dass selbst wenn die Schlange theoretisch geschlagen ist,
    # sie nicht Selbstmord begeht, weil die anderen Schlangen
    # nicht unbedingt die dafür notwendigen Moves ausführen
    game_state = clean_game_state(game_state)
    next_move = "down"
    n = Node(game_state)
    k = 2 
    num_enemy_snakes = len(game_state["board"]["snakes"])
    if num_enemy_snakes == 0:
        k = 3
    elif num_enemy_snakes == 1:
        k = 2
    elif num_enemy_snakes == 2:
        k = 1.5
    else:
        k = 1
    create_tree(n,k,True)
    best_score = minimax(n,k,-2**10,2**10,True)
    for child in n.children:
        if best_score == child.score:
            next_move = child.move
            print(next_move)
            break
    return {"move": next_move}
    
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    # board_width = game_state['board']['width']
    # board_height = game_state['board']['height']
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    if my_head["x"] == 0:
        is_move_safe["left"] = False
    if my_head["x"] == board_width-1:
        is_move_safe["right"] = False
    if my_head["y"] == 0:
        is_move_safe["down"] = False
    if my_head["y"] == board_height-1:
        is_move_safe["up"] = False

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    # my_body = game_state['you']['body']

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']
    snakes = game_state['board']['snakes']
    for i in range(0,len(snakes)):
        snake_body = snakes[i]["body"]
        if {"x":my_head["x"],"y":my_head["y"]-1} in snake_body:
            is_move_safe["down"] = False
        if {"x":my_head["x"],"y":my_head["y"]+1} in snake_body:
            is_move_safe["up"] = False
        if {"x":my_head["x"]-1,"y":my_head["y"]} in snake_body:
            is_move_safe["left"] = False
        if {"x":my_head["x"]+1,"y":my_head["y"]} in snake_body:
            is_move_safe["right"] = False

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
