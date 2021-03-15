#!/usr/bin/python
# -*- coding:utf-8 -*-

# importing the required libraries

import threading

# Couldn't find gspread module - Added subprocess - SOURCE: https://stackoverflow.com/questions/51292611/importerror-no-module-named-gspread
import sys, subprocess
#subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'gspread'])
#subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'oauth2client'])
import os
import csv
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd4in2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

##TESTING CODE
'''epd = epd4in2.EPD()
epd.init()
epd.Clear()

Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
draw = ImageDraw.Draw(Himage)
draw.text((0, 0), 'Combining Ex Scripts', font = font35, fill = 0)
draw.text((40, 100), 'TEST2', font = font24, fill = 0)
draw.text((80, 200), 'I\'m surprised this is working\nDoes this wrap it?', font = font18, fill = 0)
epd.display(epd.getbuffer(Himage))'''

import gspread
from oauth2client.service_account import ServiceAccountCredentials


# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
##your key.json file will be downloaded from Google & named like 'YOURUSERkey...####x.json'

# authorize the clientsheet 
client = gspread.authorize(creds)


# get the instance of the Spreadsheet
sheet = client.open('Messageboard') ##You'll need to change the name of your sheet to match (or vice versa)

# read old vaues from last tme

filename = "log.csv"  # log file to check previous data
## you'll likely get an error the first time, as the cell may be null. Also, it's expecting a string!
## also, if you keep getting errors. You can remove log.csv and create a new file called log.csv to replace it.

f = open(filename, 'r')
csv_f = csv.reader(f)

for row in csv_f:
    A2old = row[0]
    B2old = row[1]
    C2old = row[2]
    D2old = row[3]
    
print("getting data from sheet")

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

# get the cells in the first column

A2 = (sheet_instance.acell('A2').value)
B2 = (sheet_instance.acell('B2').value)
C2 = (sheet_instance.acell('C2').value)
D2 = (sheet_instance.acell('D2').value)

# write values to text log file
csv = open(filename, 'w')
csv.write(A2)
csv.write(",")
csv.write(B2)
csv.write(",")
csv.write(C2)
csv.write(",")
csv.write(D2)
csv.write(",")
csv.close

# check if there is any new data since last time

if (A2old != A2 or B2old != B2 or C2old != C2 or D2old != D2):

    # e-Paper display stuff

    epd = epd4in2.EPD()
    epd.init()
    epd.Clear()
    # Drawing on the Horizontal Frame image / to Switch (swap epd.width and epd.height)
    Limage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Limage)
    print ("rendering display")
    draw.text((2, 0), A2, font = font35, fill = 0) ##First Name
    draw.text((2, 50), B2, font = font35, fill = 0) ##Last Name
    draw.text((2, 100), "is here to see you from:", font = font24, fill = 0)
    draw.text((2, 150), C2, font = font35, fill = 0) ##Company Name
    draw.text((2, 250), "Comments:", font = font24, fill = 0)
    draw.text((2, 280), D2, font = font18, fill = 0)##Comments (char limit is around 40 or 50)
  
    
    #print(var1, ":", var2, "     ", var3, ":", var4)

    epd.display(epd.getbuffer(Limage))
    epd.sleep()
    print("sleeping")
    
else:
    print("there was no new data")
