#!/bin/bash

mac="ec:9b:f3:f4:93:ed"

tshark -i wlan0 -Y "wlan.ra == $mac || wlan.sa == $mac || wlan.ta == $mac || wlan.da == $mac" -T fields -e wlan.ta -e frame.time > /home/pi/Documents/macatch/output.txt
