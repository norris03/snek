def evalfunction(game_state):
    if len(game_state) == 0:
        return -2**10
    else:
        max_x = game_state["board"]["width"]
        max_y = game_state["board"]["height"]
        mid_x = max_x/2
        mid_y = max_y/2
        diff_x = abs(game_state["you"]["head"]["x"]-mid_x)
        diff_y = abs(game_state["you"]["head"]["y"]-mid_y)
        return game_state["you"]["health"]*10 - diff_x - diff_y