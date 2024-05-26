from floodfill.py import flood_fill_score
def evalfunction(game_state):
    if len(game_state) == 0:
        return -2**20
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
            bonus = 100
        else:
            bonus = 0
        flood_score = flood_fill_score(game_state)
        return bonus - 3*min_distance_to_food-(diff_x + diff_y)-200*len(game_state["board"]["snakes"])+flood_score
