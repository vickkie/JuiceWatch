# Uzi-charger-monitor
A program to monitor if charger is plugged out and act accordingly

You can install in cmd or python the program by running in root python scripts folder

//code
Python312\Scripts>pyinstaller --onefile --noconsole --hidden-import win10toast --additional-hooks-dir=. --icon=icons8-connect-48.ico battery_monitor.py


depends on :

//ensure to install in python before building THE APPlication..
import os,

import psutil,

import time,

from win10toast import ToastNotifier,

from tkinter import Tk, Label, Button, Entry, messagebox, Text, Toplevel, END,

import pystray,

from pystray import MenuItem as item,

from PIL import Image, ImageDraw,

import threading,

import sys,


free for modification and fair use

