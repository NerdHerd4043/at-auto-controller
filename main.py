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
options = parser.parse_args()