from dotenv import dotenv_values
from networktables import NetworkTables
import cv2 as cv2
import argparse
import apriltag

ip = dotenv_values(".env")["RIO_IP"]

if ip == "10.TE.AM.2":
    print("Error: specify an IP to connect to!")
    exit(0)

NetworkTables.initialize(server=ip)
sd = NetworkTables.getTable("SmartDashboard") # Use the smart dashboard table

# Get argparser for apriltag lib
parser = argparse.ArgumentParser(description='Detect AprilTags from video stream.')
apriltag.add_arguments(parser)
options = parser.parse_args()