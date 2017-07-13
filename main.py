#!/usr/bin/env python3

import sys
import os
import subprocess
import time
import sqlite3
from datetime import date, datetime

#print(sys.version)
conn = sqlite3.connect('/home/pi/Documents/macatch/macatch.db')
c = conn.cursor()

# keep track of empty scans and restart the antenna
empty_count = 0

# path to project
path = "/home/pi/Documents/macatch/"

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


def enter_data_db(macdump):
	now = datetime.now()

	with open("/home/pi/Documents/macatch/MACcount.txt", "a") as myfile:
		myfile.write(str(len(macdump)) + "\t")
		myfile.write(str(now) + "\n")
		myfile.close()

	for x in macdump:
		c.execute("SELECT id FROM cellPhone WHERE name= ?", (x, ))
		
		dataID = None
		try:
			dataID = c.fetchone()[0]
			#print (x, " - Entry exists in database. id - ", dataID)
			#continue
		except:
			c.execute('''INSERT INTO cellPhone (name) 
        			VALUES ( ? )''', ( x, ) )
			conn.commit()
			c.execute("SELECT id FROM cellPhone WHERE name= ?", (x, ))
			dataID = c.fetchone()[0]
			#print(x, " - New Entry. \t id - ", dataID)
			#pass
		
		#print("ID - ", dataID, ",\t timestamp - " , now)
		c.execute("INSERT INTO cellInstance (cellPhone_id, dateTime) VALUES(?, ?)",
			(dataID, now))
		conn.commit()
		
	log = open('/home/pi/Documents/macatch/rawData.txt', 'a')
	log.write('')
	log.close()

# Function parses through the output data from tshark
# and stores the information in the desired format
def parse_data():
	global empty_count
	print("Accessing log file")
	try:
		log = open('/home/pi/Documents/macatch/rawData.txt', 'r+')
		print("Data acquired")
	except:
		print('File does not exist in the directory.')
		exit()

	MACList = []
	outputData = []

	try:
		# read through output text file and store in variable
		while (True):
			line = log.readline()
			if line == "":
				break
			else:
				entry = line.split('\t')
				if len(entry[0]) == 17:           # MAC address of length 17 charrachters 
					MACList.append(entry[0])
					outputData.append([entry[0],entry[1]])
		log.close()
		MACList = list(set(MACList))

		# Keep track, if the scans are coming back empty
		# Might indicate that the antenna is help up
		if (len(MACList) == 0):
			empty_count += 1
		else:
			empty_count = 0

			# Enter data in database
			#enter_data_db(MACList)

			myfile = open('/home/pi/Documents/macatch/output.txt', 'a')
			for i in range(len(outputData)):
				myfile.write(str(outputData[i][0]) + "\t")
				myfile.write(str(outputData[i][1]) + "\n")
			myfile.close()
		
		# if 3 scans give zero results - device might be held up
		# reboot the collection device
		if(empty_count >= 3):
			empty_count = 0
			#subprocess.Popen('sudo ifconfig wlan0 down', shell=True, executable="/bin/bash")
			subprocess.call(['bash', '/home/pi/Documents/macatch/bootDevice.sh'])


	except KeyboardInterrupt:
		log.close()
		print("exited by command")
		sys.exit()

# The function initializes tshark scan and stores the output to a text file
def poll_area():
	# clear output file of data from previous collection
	clear_file(path, "rawData.txt")

	print("opening process")
	# run collection and output data to txt file - specify scan time in duration
	proc = subprocess.Popen("stdbuf -oL tshark -I -i wlan0 -a duration:55 -Y 'wlan.fc.type == 0 && wlan.fc.subtype == 4' \
	 -T fields -e wlan.ta -e frame.time -e frame.time_relative -e wlan.da_resolved -e radiotap.dbm_antsignal -e wlan.bssid_resolved \
	 -e wlan_mgt.ssid -e wlan.sa > /home/pi/Documents/macatch/rawData.txt",
	shell=True,
	bufsize=1,
	stdout=subprocess.PIPE,
	stderr=subprocess.STDOUT)

	print("acquiring data...")
	# wait for process to complete
	proc.wait()
	#time.sleep(30)
	print("scan complete")
	#proc.terminate()
	#proc.poll()


# clear all files from previous runs
clear_file(path, "rawData.txt")
clear_file(path, "MACcount.txt")
clear_file(path, "output.txt")

while(1):
	# collect wireless data
	poll_area()
	# store data in desired format
	parse_data()
