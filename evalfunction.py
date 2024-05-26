from floodfill import flood_fill_score
def evalfunction(game_state):
    if len(game_state) == 0:
        return -2**20
    else:
        length = game_state["you"]["length"]
        number_of_enemies = len(game_state["board"]["snakes"])
        health = game_state["you"]["health"]
        head = game_state["you"]["body"][0]
        x = head["x"]
        y = head["y"]
        max_x = game_state["board"]["width"]
        max_y = game_state["board"]["height"]
        size_map = (max_x+1)*(max_y+1)
        length_map = (max_x+1)+(max_y+1)
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
        flood_score = flood_fill_score(game_state)
        if flood_score > length:
            if health <= 95:
                return - min_distance_to_food/length_map + flood_score/size_map  - number_of_enemies       
        return flood_score/size_map - number_of_enemies
