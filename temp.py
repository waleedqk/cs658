#!/usr/bin/env python3

import sys
import os
import subprocess
import time
import sqlite3
from datetime import date, datetime

#print(sys.version)

#conn = sqlite3.connect('/home/wqkhan/Documents/raspberrypi/macatch/macatch.db')
#c = conn.cursor()

x = "ec:9b:f3:f4:93:ed"	#  "dc:53:60:a8:d5:0e"
dataID = None

path = "/home/wqkhan/Documents/raspberrypi/macatch/"

def cell_ping():
	global dataID
	global x
	
	c.execute("SELECT * FROM cellInstance WHERE cellPhone_id= ?", (dataID, ))
	try:
		data = c.fetchall()
		for row in data:
			print(row[0], "\t", row[1], "\t", row[2])
	except:
		print("No such entry in the database")

def find_my_phone():
	global dataID
	global x
	
	c.execute("SELECT id FROM cellPhone WHERE name= ?", (x, ))
	try:
		dataID = c.fetchone()[0]
		print (x, " - Entry exists in database. id - ", dataID)
		cell_ping()
	except:
		print("No such entry in the database")

# The function takes two paremeters:
# 1. directory - the folder where the file resides
# 2. file_name - the name of file to clear
# If the file exists, the function clears the contents of the file

def clear_file(directory, file_name):
	file_path = directory + file_name
	if (os.path.isfile(file_path)):
		try:
			with open(file_path, 'w') as myfile:
				myfile.write('')
				myfile.close()
		except:
			print("Error: Failed to clear file: ", file_path)
	else:
		myfile = open(file_path, 'a')
		myfile.write('')
		myfile.close()
		

#find_my_phone()
#clear_file(path, "output.txt")

subprocess.call(['bash', '/home/pi/Documents/macatch/bootDevice.sh'])


