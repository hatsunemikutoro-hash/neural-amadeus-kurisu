def calc_budget(length: int) -> int:
    if length <= 3:
        return 0
    elif length <= 15:
        return 100
    elif length <= 50:
        return 300
    else:
        return 800

