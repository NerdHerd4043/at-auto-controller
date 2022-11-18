def get_turn(center):
    x, _ = center
    # 1920 / 2 = 960 = center of screen/half of the screen
    return clamp_min_abs(-(960 - x) / 1920, 0.05)

def clamp_min_abs(value, min_abs):
    return value if abs(value) > min_abs else 0