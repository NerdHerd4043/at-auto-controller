from dotenv import dotenv_values
import cv2 as cv2


def round_iter(iterable):
    return [int(x) for x in iterable]


env = dotenv_values(".env")
LINE_LENGTH = 5
TEXT_COLOR = round_iter(env["TEXT_COLOR"].split(','))
LINE_COLOR = round_iter(env["LINE_COLOR"].split(','))
CENTER_COLOR = round_iter(env["CENTER_COLOR"].split(','))


def clamp_min_abs(value, min_abs):
    return value if abs(value) > min_abs else 0


def plot_quad(old_image, quad, alt_color=False):
    image = old_image

    color = CENTER_COLOR if alt_color else LINE_COLOR

    for edge in zip(quad[::], (*quad[1::], quad[0])):
        point_1, point_2 = edge
        image = cv2.line(image, 
                         round_iter(point_1),
                         round_iter(point_2),
                         color, 3)

    return image


def plot_point(old_image, center):
    image = old_image

    center = (int(center[0]), int(center[1]))
    image = cv2.line(image,
                     (center[0] - LINE_LENGTH, center[1]),
                     (center[0] + LINE_LENGTH, center[1]),
                     CENTER_COLOR,
                     3)
    image = cv2.line(image,
                     (center[0], center[1] - LINE_LENGTH),
                     (center[0], center[1] + LINE_LENGTH),
                     CENTER_COLOR,
                     3)
    return image


def plot_auto_state(image, auto_state):
    return cv2.putText(image, 
                       f"Autonomous: {'Enabled' if auto_state else 'Disabled'}",
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)


def plot_detecting(image, always_active, auto_state):
    text = "Enabled" if always_active or auto_state else "Disabled"
    if always_active:
        text += " -A"

    return cv2.putText(image, 
                    f"Detection: {text}",
                    (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)


def plot_text(image, center, text):
    center = (int(center[0]) + 4, int(center[1]) - 4)
    return cv2.putText(image, str(text), center, cv2.FONT_HERSHEY_SIMPLEX,
                       1, CENTER_COLOR, 3)


def nt_drive(sd, fwd, rot):
    sd.putNumber('drive_scalar', fwd)
    sd.putNumber('turn_scalar', rot)


def first(iterable, condition = lambda x: True):
    return next((x for x in iterable if condition(x)), None)


def get_img_dim(image):
    return len(image), len(image[0])
