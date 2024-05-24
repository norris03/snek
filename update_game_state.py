#from utils import pretty_print

def clean_game_state(game_state):
    del game_state["game"]
    game_state["board"]["snakes"] = [snake for snake in game_state["board"]["snakes"] if snake["id"] != game_state["you"]["id"]]
    for snake in game_state["board"]["snakes"]:
        del snake["head"]
        del snake["shout"]
        del snake["squad"]
        del snake["customizations"]
    del game_state["you"]["head"]
    del game_state["you"]["shout"]
    del game_state["you"]["squad"]
    del game_state["you"]["customizations"]
    return game_state

def update_game_state(game_state, move, is_our_turn):
    if len(game_state) == 0:
        return []
    game = game_state
    #print(game)
    max_x = game["board"]["width"]-1
    max_y = game["board"]["height"]-1
    # Update our snake, snake-on-snake collision and removing food done on enemies turn
    if is_our_turn == True:
        head = game["you"]["body"][0]
        if move == "up":
            game["you"]["body"].insert(0,{"x":head["x"],"y":head["y"]+1})
        elif move == "down":
            game["you"]["body"].insert(0,{"x":head["x"],"y":head["y"]-1})
        elif move == "right":
            game["you"]["body"].insert(0,{"x":head["x"]+1,"y":head["y"]})
        else:
            game["you"]["body"].insert(0,{"x":head["x"]-1,"y":head["y"]})
        #else:
         #   print(move, " isn't a legal move")

        # Out of bounds
        head = game["you"]["body"][0]
        if head["x"] < 0 or head["x"] > max_x or head["y"] < 0 or head["y"] > max_y:
            return []
        
        # CONSUMING
        if head in game["board"]["food"]:
            game["you"]["length"] += 1
            game["you"]["health"] = 100
        else:
            game["you"]["health"] -= 1
            if game["you"]["health"] == 0:
                return []
            else:
                game["you"]["body"].pop()

        # Self-collision
        if head in game["you"]["body"][1:]:
            return []
    else:
        dead_snakes = []
        number_of_enemies = len(game["board"]["snakes"])
        for i in range(0, number_of_enemies):
            head = game["board"]["snakes"][i]["body"][0]
            if move[i] == "up":
                game["board"]["snakes"][i]["body"].insert(0,{"x":head["x"],"y":head["y"]+1})
            elif move[i] == "down":
                game["board"]["snakes"][i]["body"].insert(0,{"x":head["x"],"y":head["y"]-1})
            elif move[i] == "right":
                game["board"]["snakes"][i]["body"].insert(0,{"x":head["x"]+1,"y":head["y"]})
            elif move[i] == "left":
                game["board"]["snakes"][i]["body"].insert(0,{"x":head["x"]-1,"y":head["y"]})
            else:
                print(move[i], " isn't a legal move")

            # Out of bounds
            head = game["board"]["snakes"][i]["body"][0]
            if head["x"] < 0 or head["x"] > max_x or head["y"] < 0 or head["y"] > max_y:
                dead_snakes.append(game["board"]["snakes"][i])
            
            # CONSUMING
            if head in game["board"]["food"]:
                game["board"]["snakes"][i]["length"] += 1
                game["board"]["snakes"][i]["health"] = 100
            else:
                game["board"]["snakes"][i]["health"] -= 1
                if game["board"]["snakes"][i]["health"] == 0:
                    dead_snakes.append(game["board"]["snakes"][i])
                else:
                    game["board"]["snakes"][i]["body"].pop()

            # Self-collision
            if head in game["board"]["snakes"][i]["body"][1:]:
                dead_snakes.append(game["board"]["snakes"][i])

        # Us-on-Snake Collision
        head = game["you"]["body"][0]
        length = game["you"]["length"]
        for i in range(0, number_of_enemies):
            if head in game["board"]["snakes"][i]["body"]:
                if head == game["board"]["snakes"][i]["body"][0] and length > game["board"]["snakes"][i]["length"]:
                    dead_snakes.append(game["board"]["snakes"][i])
                else:
                    return []
            if game["board"]["snakes"][i]["body"][0] in game["you"]["body"]:
                dead_snakes.append(game["board"]["snakes"][i])

        # Snake-on-Snake Collision
        for i in range(0, number_of_enemies):
            head = game["board"]["snakes"][i]["body"][0]
            length = game["board"]["snakes"][i]["length"]
            for j in range(0, number_of_enemies):
                if i == j:
                    continue
                if head in game["board"]["snakes"][j]["body"]:
                    if head == game["board"]["snakes"][j]["body"][0] and length > game["board"]["snakes"][j]["length"]:
                        dead_snakes.append(game["board"]["snakes"][j])
                    else:
                        dead_snakes.append(game["board"]["snakes"][i])

        
        #remove food
        eaten_apples = []
        for apple in game["board"]["food"]:
            if apple == game["you"]["body"][0]:
                eaten_apples.append(apple)
            for snake in game["board"]["snakes"]:
                if apple == snake["body"][0]:
                    eaten_apples.append(apple)
        for eaten_apple in eaten_apples:
            if eaten_apple in game["board"]["food"]:
                game["board"]["food"].remove(eaten_apple)
        
        #remove snakes
        for dead_snake in dead_snakes:
            if dead_snake in game["board"]["snakes"]:
                game["board"]["snakes"].remove(dead_snake)    

    return game

#state = clean_game_state(game_state=state)
#pretty_print(state)
#state = update_game_state(state, "up", is_our_turn=True)
#state = update_game_state(state, ["left","down"], is_our_turn=False)
#pretty_print(state)
#state = update_game_state(state, "right", is_our_turn=True)
#state = update_game_state(state, ["right"], is_our_turn=False)
#pretty_print(state)
#state = update_game_state(state, "right", is_our_turn=True)
#state = update_game_state(state, [""], is_our_turn=False)
#pretty_print(state)
#state = update_game_state(state, "right", is_our_turn=True)
#state = update_game_state(state, ["down","left"], is_our_turn=False)
#pretty_print(state)
