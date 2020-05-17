#import motion_detection as motion_detection
import webstream as webstream
import water_level as water_level
from relay import Relay_Motor
import subprocess
import sys 


from threading import Thread as thread
from flask import Flask, json, request
from logger import Logger

#Load config (has information about login, path to api, and certificate file location)
with open('lib/config.json') as json_data_file:
    config = json.load(json_data_file)

#Variable that is shared between the different threads
global shared_status_variable

#initializing variables
api = Flask("API")
shared_status_variable = {'water_level': "Not detected", 'pump_started': "Not detected", 'water_level_pin': 16, 'motor_pin': 21}
motor = Relay_Motor(shared_status_variable)
loggervariable = Logger(config) #used for e-mail

#Initializing API route for getting water level
@api.route('/water_level_call', methods=['GET'])
def water_level_call():
  print("Checking water level")
  return json.dumps(shared_status_variable)
  
#Stopping the motor
@api.route('/stop_pump_call', methods=['GET'])
def stop_pump_call():
    print("Starting pump")
    motor.motor_off(shared_status_variable)
    return json.dumps(shared_status_variable)

#Starting motor with the seconds provided.
@api.route("/start_pump_time_call", methods=['POST'])
def start_pump_time_call():
    req_data = request.get_json()
    print(int(req_data['time']))
    motor.turn_timed_motor_on(shared_status_variable, int(req_data['time']))
    return json.dumps('')
    
#Restart server
@api.route('/restart_server_call', methods=['GET'])
def restart_server_call():
    print("Restart server")
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print("output")
    
#Stop server
@api.route('/stop_server_call', methods=['GET'])
def stop_server_call():
    print("Stopping server")
    sys.exit()
    

#Starting the threads and API-server 
#Port 3000 will be used for node server
#Port 5000 will be used for flask server
#Port 8000 will be used for web-cam

def start():

    try:    
        water_thread = thread(target = water_level.start_detecting_water, args=[shared_status_variable])
        webcam_thread = thread(target = webstream.webstream_start, args=[shared_status_variable])
        
        webcam_thread.start()
        water_thread.start()
        api.run(host='0.0.0.0')
    
    except Exception as e:
        loggervariable.send_email("Error message: " + e)

start()