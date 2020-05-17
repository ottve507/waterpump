import RPi.GPIO as GPIO
import time


#Class that will be used to control motor (initiated in main.py)
class Relay_Motor:
    
    
    def __init__(self, shared_status_variable):
        # PIN setup
        GPIO.setmode(GPIO.BCM) #will let us use pin numbers for referencing.
        GPIO.setup(shared_status_variable['motor_pin'], GPIO.OUT)
    
    def motor_on(self, shared_status_variable):
        print("motor on")
        GPIO.output(shared_status_variable['motor_pin'], GPIO.HIGH)  # Turn motor on
        
    def motor_off(self, shared_status_variable):
        print("motor off")
        GPIO.output(shared_status_variable['motor_pin'], GPIO.LOW)  # Turn motor off
            
    def turn_timed_motor_on(self, shared_status_variable, sleep_time):
        try:
            shared_status_variable['pump_started'] = "Pump started"
            self.motor_on(shared_status_variable)
            time.sleep(sleep_time)
            self.motor_off(shared_status_variable)
            shared_status_variable['pump_started'] = "Pump stopped"
        except KeyboardInterrupt:
            self.motor_off(shared_status_variable)
            shared_status_variable['pump_started'] = "Pump stopped"
            GPIO.cleanup(shared_status_variable)
