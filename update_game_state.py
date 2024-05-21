state2 = {'game': {'id': '90aa8919-aa32-44c0-a3ea-f2b76dbff1f1', 'ruleset': {'name': 'standard', 'version': 'cli', 'settings': {'foodSpawnChance': 15, 'minimumFood': 1, 'hazardDamagePerTurn': 14, 'hazardMap': '', 'hazardMapAuthor': '', 'royale': {'shrinkEveryNTurns': 25}, 'squad': {'allowBodyCollisions': False, 'sharedElimination': False, 'sharedHealth': False, 'sharedLength': False}}}, 'map': 'standard', 'timeout': 500, 'source': ''}, 'turn': 5, 
         'board': {'height': 10,
                    'width': 10, 
                    'snakes': [
                        {'id': 'eacfa58f-5356-47e6-94aa-833295c6b96c', 'name': 'snek', 'latency': '4', 'health': 95, 'body': [{'x': 1, 'y': 0}, {'x': 1, 'y': 1}, {'x': 1, 'y': 2}], 'head': {'x': 1, 'y': 0}, 'length': 3, 'shout': '', 'squad': '', 'customizations': {'color': '#FFFF00', 'head': 'fang', 'tail': 'block-bum'}},
                        {'id': '3d6b6171-8a95-41d9-86a5-db01fa72e0aa', 'name': 'snek2', 'latency': '5', 'health': 95, 'body': [{'x': 9, 'y': 0}, {'x': 9, 'y': 1}, {'x': 9, 'y': 2}], 'head': {'x': 9, 'y': 0}, 'length': 3, 'shout': '', 'squad': '', 'customizations': {'color': '#FFFF00', 'head': 'fang', 'tail': 'block-bum'}},
                        {'id': 'fc917519-276a-4d76-b553-166cc4b4340b', 'name': 'snek3', 'latency': '3', 'health': 99, 'body': [{'x': 2, 'y': 0}, {'x': 5, 'y': 5}, {'x': 5, 'y': 6}, {'x': 5, 'y': 7}], 'head': {'x': 5, 'y': 4}, 'length': 4, 'shout': '', 'squad': '', 'customizations': {'color': '#FFFF00', 'head': 'fang', 'tail': 'block-bum'}}
                    ], 
        
        'food': [{'x': 0, 'y': 6}, {'x': 9, 'y': 4}, {'x': 6, 'y': 9}, {'x': 8, 'y': 6}, {'x': 0, 'y': 4},{"x":8,"y":0},{"x":0,"y":0}],
        'hazards': []}, 
         
         'you': {'id': '3d6b6171-8a95-41d9-86a5-db01fa72e0aa', 'name': 'snek2', 'latency': '0', 'health': 95, 'body': [{'x': 9, 'y': 0}, {'x': 9, 'y': 1}, {'x': 9, 'y': 2}], 'head': {'x': 9, 'y': 0}, 'length': 3, 'shout': '', 'squad': '', 'customizations': {'color': '#FFFF00', 'head': 'fang', 'tail': 'block-bum'}}}


def clean_game_state(game_state):
    del game_state["game"]
    game_state["board"]["snakes"] = [snake for snake in game_state["board"]["snakes"] if snake["id"] != game_state["you"]["id"]]
    return game_state

def update_game_state(game_state,move,our_turn):
    if len(game_state) == 0:
        return []
    #print("Previous state:")
    #print(game_state)
    #print("================")
    enemies = [snake for snake in game_state["board"]["snakes"] if snake["id"] != game_state["you"]["id"]]
    min_x = 0
    min_y = 0
    max_x = game_state["board"]["width"]-1
    max_y = game_state["board"]["height"]-1
    if our_turn == True:
        our_head = game_state["you"]["head"]
        our_body = game_state["you"]["body"]
        if move == "up":
            new_head = {"x":our_head["x"],"y":our_head["y"]+1}
        elif move == "right":
            new_head = {"x":our_head["x"]+1,"y":our_head["y"]}
        elif move == "down":
            new_head = {"x":our_head["x"],"y":our_head["y"]-1}
        elif move == "left":
            new_head = {"x":our_head["x"]-1,"y":our_head["y"]}

        # hit wall death
        if new_head["x"] > max_x or new_head["y"] > max_y or new_head["x"] < min_x or new_head["y"] < min_y:
            return []

        # eat stuff
        food_eaten = False
        if new_head in game_state["board"]["food"]:
            game_state["board"]["food"].remove(new_head)
            food_eaten = True

        #change game_state
        if food_eaten == True:
            game_state["you"]["health"] = 101
            game_state["you"]["length"] = game_state["you"]["length"] + 1
        else:
            #game_state["you"]["health"] = game_state["you"]["health"] - 0.5
            game_state["you"]["body"].pop()

        #self collision
        if new_head in our_body:
            return []
        
        game_state["you"]["body"].insert(0,new_head)
        game_state["you"]["head"] = new_head
        #for enemy in enemies:
        #    enemy["health"] = enemy["health"] - 0.5
        
    else:
        i = -1
        eaten_food = []
        # update position of enemies
        for enemy in enemies:
            i += 1
            enemy_head = enemy["head"]
            new_head = enemy_head
            if move[i] == "up":
                new_head = {"x":enemy_head["x"],"y":enemy_head["y"]+1}
            elif move[i] == "right":
                new_head = {"x":enemy_head["x"]+1,"y":enemy_head["y"]}
            elif move[i] == "down":
                new_head = {"x":enemy_head["x"],"y":enemy_head["y"]-1}
            elif move[i] == "left":
                new_head = {"x":enemy_head["x"]-1,"y":enemy_head["y"]}
            #wall collision
            if new_head["x"] > max_x or new_head["y"] > max_y or new_head["x"] < min_x or new_head["y"] < min_y:
                game_state["board"]["snakes"].remove(enemy)
                continue
            #eating food, dont immeadiately remove pof, other could theoretically also eat it, wait till collision fight resolution
            food_eaten = False
            if new_head in game_state["board"]["food"]:
                eaten_food.append(new_head)
                food_eaten = True
            if food_eaten == True:
                enemy["health"] = 100.5
                enemy["length"] = enemy["length"] + 1
            else:
                #enemy["health"] = enemy["health"] - 0.5
                enemy["body"].pop()
            
            #self collision
            if new_head in enemy["body"]:
                game_state["board"]["snakes"].remove(enemy)
                continue

            enemy["body"].insert(0,new_head)
            enemy["head"] = new_head
        # multiple enemies could eat food at same time (resolution via collision later)
        
        for eaten_piece_of_food in eaten_food:
            if eaten_piece_of_food in game_state["board"]["food"]:
                game_state["board"]["food"].remove(eaten_piece_of_food)
        
    # adjust health
    for snake in game_state["board"]["snakes"]:
        snake["health"] -= 0.5
    game_state["you"]["health"] -= 0.5
    
    # health 0
    if game_state["you"]["health"] == 0:
        return []
    for enemy in enemies:
        if enemy["health"] == 0:
            game_state["board"]["snakes"].remove(enemy)

    #head-to-head collisions between snakes
    for enemy in enemies:
        if game_state["you"]["head"] == enemy["head"]:
            if game_state["you"]["length"] <= enemy["length"]:
                return []
            if game_state["you"]["length"] > enemy["length"]:
                game_state["board"]["snakes"].remove(enemy)

    for enemy in enemies:
        other_enemies = [snake for snake in enemies if snake["id"] != enemy["id"]]
        for other_enemy in other_enemies:
            if enemy["head"] == other_enemy["head"]:
                #print("=========COLLISION=========")
                if enemy["length"] <= other_enemy["length"]:
                    if enemy in game_state["board"]["snakes"]:####sdasikjdhgasg
                        game_state["board"]["snakes"].remove(enemy) ####sdasikjdhgasgdaj
                #elif enemy["length"] == other_enemy["length"]:      
                 #   game_state["board"]["snakes"].remove(enemy)
                    # DA ER ALLE DURCHGEHT REICHTE ES NUR JETZIGEN ZU ENTFERNEN
                    #game_state["board"]["snakes"].remove(other_enemy)
                elif enemy["length"] > other_enemy["length"]:
                    if other_enemy in game_state["board"]["snakes"]:
                        game_state["board"]["snakes"].remove(other_enemy)
    # regular collisions with other snakes
    for enemy in enemies:
        if game_state["you"]["head"] in enemy["body"]:
            return []
    for snake in game_state["board"]["snakes"]:
        other_snakes = [snek for snek in game_state["board"]["snakes"] if snek["id"] != snake["id"]]
        for other_snake in other_snakes:
            if snake["head"] in other_snake["body"]:
                game_state["board"]["snakes"].remove(snake)
    #print("New state:")
    #print(game_state)
    #print("================")
    return game_state

#state2 = clean_game_state(state2)
#state2 = update_game_state(state2,"left",True)
#state = update_game_state(state,["right","left"],False)