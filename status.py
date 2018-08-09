#!/usr/bin/env python2
# Python script for controling status light and shutdown button on raspberry pi
# Author : Ethan Brierley
#services are dnsmasq, hostapd, apache2

print ("Importing libraries")

from gpiozero import LED
from gpiozero import Button
import time
import sys
import subprocess

ledPin = LED(14) # Pin for simple status LED
powerButtonPin = Button(18) # No longer needed.
statusButtonPin = Button(22) # Pin for showing the status of the server on the LED
statusButtonPin2 = Button(22)

start_time = time.time()

def Poweroff():
    ledPin.on()
    time.sleep(1)
    print ("Shutting down")
    command = "/usr/bin/sudo /sbin/reboot now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print (str(output))
    print ("end")

def clean():
    print ("Cleaning Pins")
    ledPin.off()

def checkForKeyWords(service):
    if "dnsmasq" not in service:
        print ("dnsmasq not found")
        return False
    if "hostapd" not in service:
        print ("hostapd not found")
        return False
    if "apache2" not in service:
        print ("apache2 not found")
        return False
    return True

def checkStatus():
    proc = subprocess.Popen('pstree', stdout=subprocess.PIPE)
    tmp = proc.stdout.read()
    tmp = tmp.replace("|", "")
    tmp = tmp.replace("-", "")
    tmp = tmp.replace("{", "")
    tmp = tmp.replace("}", "")
    tmp = tmp.replace("[", "")
    tmp = tmp.replace("]", "")
    tmp = tmp.replace(" ", "")
    tmp = tmp.replace("`", "")
    tmp = tmp.replace("*", "")
    tmp = tmp.replace("(", "")
    tmp = tmp.replace(")", "")
    tmp = tmp.replace("|", "")
    tmp = tmp.split("\n")
    if checkForKeyWords(tmp) == False:
        return 2
    return 1

def moveLogs():
    print ("Reorganizing logs and removing old logs. ")
    pass
    #Code that moves logs.







clean()
while True:
    if powerButtonPin.is_pressed:
        ledPin.on()
        Poweroff()
    while statusButtonPin.is_pressed:
        pass
    if checkStatus() == 2:
        statusButtonPin2.on
    else:
        statusButtonPin2.off
    if time.time() - start_time > 86400: #86400 is the number of seconds in 24hours.
        print ("Script has been running for 24 hours")
        start_time = time.time()
        moveLogs()
