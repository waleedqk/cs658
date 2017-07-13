#!/usr/bin/env python3

import sys
import os
import subprocess
import time
import sqlite3
from datetime import date, datetime

db_list = list()
loc = '/home/wqkhan/Documents/raspberrypi/macatch/DriveData/Exp1/'
x = "d8:96:95:09:a7:a8" #"ec:9b:f3:f4:93:ed"
dataID = None
conn = None
c = None

def list_db():
	global db_list, loc
	files = os.listdir(loc)
	for file in files:
	    db_list.append(file)
	#print(db_list)

def db_connect(db_name):
	global loc, conn, c
	add = loc + db_name
	conn = sqlite3.connect(add)
	c = conn.cursor()
	find_my_phone()
	c.close()

def cell_ping():
	global dataID, x, c
	
	c.execute("SELECT * FROM cellInstance WHERE cellPhone_id= ?", (dataID, ))
	try:
		data = c.fetchall()
		for row in data:
			print(row[0], "\t", row[1], "\t", row[2])
	except:
		print("No such entry in the database")

def find_my_phone():
	global dataID, x, c
	
	c.execute("SELECT id FROM cellPhone WHERE name= ?", (x, ))
	try:
		dataID = c.fetchone()[0]
		print (x, " - Entry exists in database. id - ", dataID)
		cell_ping()
	except:
		print("No such entry in the database")



list_db()

for db in db_list:
	db_connect(db)
	