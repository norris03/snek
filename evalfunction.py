def evalfunction(game_state):
    if len(game_state) == 0:
        return -2**10
    else:
        head = game_state["you"]["body"][0]
        x = head["x"]
        y = head["y"]
        max_x = game_state["board"]["width"]
        max_y = game_state["board"]["height"]
        mid_x = max_x/2
        mid_y = max_y/2
        diff_x = abs(x-mid_x)
        diff_y = abs(y-mid_y)
        food = game_state["board"]["food"]
        min_distance_to_food = max_x+max_y
        for pof in food:
            distance_to_food = abs(x-pof["x"])+abs(y-pof["y"])
            if distance_to_food < min_distance_to_food:
                min_distance_to_food = distance_to_food
        if game_state["you"]["health"] >= 96:
            bonus = 1000
        else:
            bonus = 0
        return bonus - 3*min_distance_to_food-(diff_x + diff_y)
