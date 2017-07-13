#!/bin/bash

#clean the system at reboot

now=$(date +%d-%m-%Y-%H-%M-%S)

if [ -e "/home/pi/Documents/macatch/macatch.db" ]
then
 mv /home/pi/Documents/macatch/macatch.db /home/pi/Documents/macatch/DB/macatch_$now.db
fi

if [ -e "/home/pi/Documents/macatch/output.txt" ]
then
  mv /home/pi/Documents/macatch/output.txt /home/pi/Documents/macatch/DB/output_$now.txt
fi


cd /home/pi/Documents/macatch/; python createDB.py
