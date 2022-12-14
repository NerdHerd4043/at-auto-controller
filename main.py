from dotenv import dotenv_values
from networktables import NetworkTables
import cv2 as cv2
import argparse
import apriltag

from helpers import (
    plot_quad,
    plot_point,
    plot_auto_state,
    plot_detecting,
    plot_text,
    first,
    speed,
)

env = dotenv_values(".env")
ip = env["RIO_IP"]

# Just a note that these names don't provide value any longer, what does it mean to be tag 11?
# At that point why not just store the variable directly.
#
# The value gained from the old variable name was that it was the id of the tag meant for driving
# In this case wouldn't "drive_tag_id" and "drop_tag_id" be more apt names?
#
# In most scenarios, you want the names to represent what they *do* not what they *are*,
# Don't name them their values, if you were to do that you might as well just use those values
# Purpose and intent matter far more than value
drive_tag_id = int(env["DRIVE_TAG_ID"])
drop_tag_id = int(env["DROP_TAG_ID"])

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

        # def need to talk to you about python for loops, but in effect you are
        # looping over *every* detection and calling it tag 11, and similar in the
        # below for loop, in technicality you are drawing two boxes for every tag
        # also, the boolean in the third argument just controls the color of the box
        # drawn :P (you can take a gander either by looking at it in helpers, or
        # hovering over the function call, it should give you a function definition)
        for tag in detections:
            image = plot_quad(image, tag.corners, tag.tag_id == drive_tag_id)
            # TODO: Unreflect this...
            # image = plot_text(image, tag.center, tag.tag_id) # Plotting tag id
            image = plot_point(image, tag.center)

        # for tag_0 in detections:
        #     image = plot_quad(image, tag_0.corners, tag_0.tag_id == drive_tag_id_0)
        #     image = plot_point(image, tag_0.center)

        drive_tag = first(detections, lambda tag: tag.tag_id == drive_tag_id)
        drop_tag = first(detections, lambda tag: tag.tag_id == drop_tag_id)


        # something in my sleep eluded brain doesn't like this if statement,
        # but I'm not entirely sure what lmao
        if drive_tag:
            sd.putNumber("Turn_Value", (tag.center[0] - 960)/2000)
            sd.putNumber("Drive_Value", speed(tag.corners))
        elif drop_tag:
            sd.putBoolean("Drop_Tubes", True)
        else:
            sd.putNumber("Turn_Value", 0)
            sd.putNumber("Drive_Value", 0)
            sd.putBoolean("Drop_Tubes", False)

    image = cv2.flip(image, 1)

    image = plot_auto_state(image, auto_state)
    image = plot_detecting(image, options.always_active, auto_state)

    cv2.imshow('Camera View', image)

    key = cv2.waitKey(1)
    if key == 13:
        loop = False

cv2.destroyAllWindows()