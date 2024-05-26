from evalfunction import evalfunction
def minimax(node, depth, alpha, beta, our_turn):
    if depth == 0 or len(node.game_state) == 0:
        return evalfunction(node.game_state)
    if our_turn:
        maxEval = -2**20
        for child in node.children:
            eval = minimax(child, depth - 0.5, alpha, beta, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        node.score_this(maxEval)
        return maxEval
    else:
        minEval = 2**20
        for child in node.children:
            eval = minimax(child, depth - 0.5, alpha, beta, True)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        node.score_this(minEval)
        return minEval
