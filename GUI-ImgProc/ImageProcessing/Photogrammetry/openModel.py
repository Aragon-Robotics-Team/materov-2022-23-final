import os
import ctypes
import argparse


parser = argparse.ArgumentParser()

parser.add_argument('file', help = "file path pls :pleading_face:")

args = parser.parse_args()
filePath = args.file

os.startfile(filePath)

mymessage = 'Diseased Tissue Total Area: 56in^2\nDiameter: 26in\nHeight: 12in'
title = 'Print 3D - bowltest2'
ctypes.windll.user32.MessageBoxW(0, mymessage, title, 0)
