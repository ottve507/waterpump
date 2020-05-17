#!/usr/bin/python
import RPi.GPIO as GPIO
import time

#Check water function to look for changes in the pin
def check_water(shared_status_variable):
    if GPIO.input(shared_status_variable['water_level_pin']):
        shared_status_variable['water_level'] = "Has water"
    else:
        shared_status_variable['water_level'] = "No water"


#Initializing function from thread in main.py
def start_detecting_water(shared_status_variable):
    #GPIO SETUP
    GPIO.setmode(GPIO.BCM) #For checking numbers.
    GPIO.setup(shared_status_variable['water_level_pin'], GPIO.IN)
 
    # Infinite loop
    while True:
        time.sleep(5)
        check_water(shared_status_variable)
