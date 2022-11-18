from dotenv import dotenv_values
from networktables import NetworkTables
import cv2 as cv2
import argparse
import apriltag

from helpers import get_turn

ip = dotenv_values(".env")["RIO_IP"]

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

    if options.always_active or sd.getBoolean('auto_state', False):
        grayimg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        detections = detector.detect(grayimg)
    
        for detection in detections:
            pass

    cv2.imshow('Camera View', image)

    key = cv2.waitKey(10)
    if key == 13:
        loop = False

cv2.destroyAllWindows()