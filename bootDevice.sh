#!/bin/bash

sudo ifconfig wlan0 down
sudo iwconfig wlan0 mode monitor
# sudo iwconfig wlan0 channel 6
sudo ifconfig wlan0 up
sudo ifconfig wlan0 promisc