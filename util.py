import cfg

def log(msg: str):
    # print log messages to console if debugging enabled
    if cfg.DEBUG:
        print(msg)

def get_other_player(player):
    """
    Get the alternate player (used to switch between for moves)
    :param player:
    :return:
    """
    if player == 1:
        return 2
    else:
        return 1
