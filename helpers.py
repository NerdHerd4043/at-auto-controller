from dotenv import dotenv_values
import cv2 as cv2


def round_iter(iterable):
    return [int(x) for x in iterable]


env = dotenv_values(".env")
TEXT_COLOR = round_iter(env["TEXT_COLOR"].split(','))
LINE_COLOR = round_iter(env["LINE_COLOR"].split(','))
NORMAL_COLOR = env["NORMAL_COLOR"].split(',')


def get_turn(center):
    x, _ = center
    # 1920 / 2 = 960 = center of screen/half of the screen
    return clamp_min_abs(-(960 - x) / 1920, 0.05)


def clamp_min_abs(value, min_abs):
    return value if abs(value) > min_abs else 0


def plot_quad(old_image, quad):
    image = old_image

    for edge in zip(quad[::], (*quad[1::], quad[0])):
        point_1, point_2 = edge
        image = cv2.line(image, 
                         round_iter(point_1),
                         round_iter(point_2),
                         LINE_COLOR, 3)

    return image