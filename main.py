from dotenv import dotenv_values
from networktables import NetworkTables
import cv2 as cv2
import argparse
import apriltag

from helpers import (
    get_turn,
    plot_quad,
    plot_point,
    plot_auto_state,
    plot_detecting,
    plot_text,
    nt_drive,
    first
)

env = dotenv_values(".env")
ip = env["RIO_IP"]
drive_tag_id = int(env["DRIVE_TAG_ID"])

# Quick check that you actuall set the ip <3
if ip == "10.TE.AM.2":
    print("Error: specify an IP to connect to!")
    exit(0)

# connect to networktables and get smart dashboard
NetworkTables.initialize(server=ip)
sd = NetworkTables.getTable("SmartDashboard")

# Get argparser for apriltag lib
parser = argparse.ArgumentParser(description='Detect AprilTags from video stream.')
apriltag.add_arguments(parser)
parser.add_argument(
    '-a', '--always-active', 
    action='store_true',
    help='Always detect april tags (default: only detect tags when auto is active)'
    )
options = parser.parse_args()

# AprilTag detector and camera
detector = apriltag.Detector(options)
cam = cv2.VideoCapture(0)

loop = True
while loop:
    _, image = cam.read()

    auto_state = sd.getBoolean('auto_state', False)
    detecting = options.always_active or auto_state

    grayimg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if detecting:
        detections = detector.detect(grayimg)

        for tag in detections:
            image = plot_quad(image, tag.corners, tag.tag_id == drive_tag_id)
            # TODO: Unreflect this...
            # image = plot_text(image, tag.center, tag.tag_id) # Plotting tag id
            image = plot_point(image, tag.center)

        # control code goes here

    image = cv2.flip(image, 1)

    image = plot_auto_state(image, auto_state)
    image = plot_detecting(image, options.always_active, auto_state)

    cv2.imshow('Camera View', image)

    key = cv2.waitKey(1)
    if key == 13:
        loop = False

cv2.destroyAllWindows()