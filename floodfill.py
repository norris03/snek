import numpy as np

def grid(game_state):
    game = game_state
    if len(game_state) == 0:
        return []
    #print(game)
    grid = np.zeros((game["board"]["width"],game["board"]["height"]))
    grid[game["you"]["body"][0]["x"]][game["you"]["body"][0]["y"]] = 8
    for bp in game["you"]["body"][1:]:
        grid[bp["x"]][bp["y"]] = 1
    for snake in game["board"]["snakes"]:
        for bp in snake["body"]:
            grid[bp["x"]][bp["y"]] = 2
    grid = np.rot90(grid)
    #print(grid)
    return grid

def inside(grid, i, j):
    grid_max_j = len(grid[0])-1
    grid_max_i = len(grid)-1
    if i < 0 or j < 0 or i > grid_max_i or j > grid_max_j:
        return False
    value = grid[i][j]
    if value != 0 and value != 8 and value != 4:
        return False
    else:
        return True


def inside(grid, i, j):
    return 0 <= i < len(grid) and 0 <= j < len(grid[0]) and grid[i][j] != 4 and grid[i][j] != 1 and grid[i][j] != 2

def scan(grid, l, r, j, s):
    span_added = False
    for i in range(l, r + 1):
        if not inside(grid, i, j):
            span_added = False
        elif not span_added:
            s.append([i, j])
            span_added = True
    return s

def fill(grid, i, j):
    if not inside(grid, i, j):
        return grid
    s = []
    s.append([i, j])
    while len(s) != 0:
        x, y = s.pop(0)
        l = x
        while inside(grid, l - 1, y):
            grid[l - 1][y] = 4
            l -= 1
        r = x
        while inside(grid, r, y):
            grid[r][y] = 4
            r += 1
        s = scan(grid, l, r - 1, y + 1, s)
        s = scan(grid, l, r - 1, y - 1, s)
    return grid


def flood_fill_score(game_state):
    game_grid = grid(game_state)
    game_grid = fill(game_grid, game_state["you"]["body"][0]["x"], game_state["you"]["body"][0]["y"])
    score = (game_grid == 4).sum()-1
    return score
