# Raspberry Pi watering system

This project uses a node webserver and a python back-end to control a watering system. The watering system consists of a webcam, water level sensor, and 12 V pump (controlled with a relay).

I’ve used this system to water multiple plants (19 in total) during the summer months.

![Watering system](/media/pumpsystem.PNG)


* [Installation](#Installation)
** [Software installation](##Software-installation)


# Installation

## Software installation

Pre-requisites:
-	Raspberry Pi (with Raspbian installed)
-	Node.js 
-	Python3 
-	Mongodb

**Step 1 - Clone**: cd to /home/pi/ and git clone the project. It is important that the home directory of this project is "/home/pi/waterpump" as we will use this location for starting the different servers automatically on boot.

**Step 2 - Install dependencies**: cd in nodewebapp and run 
```
npm install .
```

**Step 3 - Clear db**: Clear out any old database information (if needed). Mongodb runs the database part of the nodejs webserver and should be fairly easy to install. I used the following command:
```
sudo apt install mongodb
```
The database for the webapp will be setup in waterpump/nodewebapp/data. To remove the database (i.e. remove any register user), just stop the mongodb server and delete the content inside of that folder.

**Step 4 - Setup autostart**: All of the components/servers of the watering system need to start when the Raspberry Pi is booted. To enable this we will need to change the "rc.local" file to tell the Raspberry what servers to start on boot:
```
sudo nano /etc/rc.local
```
Add the following line:
```
sh /home/pi/waterpump/launcher.sh &
```
The "launcher.sh" file will perform the actual initiation of servers in the background. To start the servers individually you can try using the commands performed inside the script.

**Step 5 - Security config**: For security purposes, the authentication-secret in "waterpump/nodewebapp/config/main.js" should be changed to something else.

## Hardware installation

The following parts are needed:
* [Raspberry Pi](https://www.kjell.com/se/produkter/dator/raspberry-pi/raspberry-pi-4-model-b-enkortsdator-2-gb-ram-p88180)

* [Pin wires - female to female](https://cdon.se/hem-tradgard/dupont-10-cm-kabel-hona-hona-for-t-ex-kopplingsplatta-arduino-p36235360?gclid=Cj0KCQjw2PP1BRCiARIsAEqv-pRGPYSliWqKih87pdQxgjBltUapsjvtk_-qEq6ANRwFi1F6YjiAT3kaAgrKEALw_wcB&gclsrc=aw.ds)

* [Pin wires - male to male](https://www.kjell.com/se/produkter/el-verktyg/arduino/tillbehor/delbar-kopplingskabel-40-pol-15-cm-hane-hona-p87076?gclid=Cj0KCQjw2PP1BRCiARIsAEqv-pR295gkMshaOOeSRsJyPcc90cM93qskixhjnBih_f7xH-DxT0LYcZQaAnKKEALw_wcB&gclsrc=aw.ds)

* [Pump 12 V](https://www.kjell.com/se/produkter/el-verktyg/arduino/tillbehor/vatskepump-240-lh-p87079)

* [Relay](https://www.kjell.com/se/produkter/el-verktyg/arduino/moduler/relamodul-for-arduino-1x-p87032)

* [Power adapter](https://www.kjell.com/se/produkter/el-verktyg/stromforsorjning/natadaptrar/acdc-natadaptrar/fast-utspanning/switchad-natadapter-12-v-dc-12-w-p44382)

* [Hose to fit pump](https://www.kjell.com/se/produkter/el-verktyg/arduino/tillbehor/vatskeslang-med-klammor-2-meter-p87083)

* [Water level sensor](https://www.kjell.com/se/produkter/el-verktyg/arduino/tillbehor/vattensensor-och-jordfuktsmatare-for-arduino-p87066)

* [Raspberry Pi camera](https://www.kjell.com/se/produkter/dator/raspberry-pi/raspberry-pi-kameramodul-v2-p88053)

* [Hose to fit connectors]( https://badspecialisten.se/p/badkar/reservdelar-badkar/slangar-badkar/luftslang-6mm/?utm_source=Google%20Shopping&utm_campaign=Productfeed&utm_medium=cpc&utm_term=2750&gclid=Cj0KCQjw2PP1BRCiARIsAEqv-pR7YyPtSewpr_M8ciQi8Zkedy1050CzwmmaGz8UODgGVreVsg_VPwcaAvTuEALw_wcB)

* [Hose connections – example](https://www.hydrogarden.se/odlingssystemkrukor/bevattning-pumpar/tropf-blumat-bevattningssystem/blumat-t-koppling-838mm.html)


### Wiring of water level sensor and motor

![Sensor](/media/water_sensor.png)
![Motor + relay](/media/relay_fritzing.png)

When splicing my power adapter, I found that the solid/dashed lines on wires are used to indicate polarity. Usually the wire with the white stripe or the dashed lines carries the "positive" (+) end, while the other, unmarked wire carries the "negative" (-) end.
![Power adapter](/media/power_adapter.png)

### Installation of Raspberry Pi Camera

I thought that this [Guide]( https://thepihut.com/blogs/raspberry-pi-tutorials/16021420-how-to-install-use-the-raspberry-pi-camera) was pretty useful. 

## Introduction to software architecture

The watering system uses the following servers (initiated from launcher.sh):

* **Node.js webb-app (nodewebbapp/app.js)**: The node.js web-app will be responsible for creating a webpage on which (only) one user can register. 
   
* **Mongodb server (nodewebbapp/data)**: Mongodb is the database used for the Node.js-server. It allows for user registration and login functionality.

* **Python server (pythonserver/main.py)**: The python server delivers the actual functionality of the watering system.

The watering system uses the following ports:
* 3000: Webserver
* 8000: Webcam
* 5000: Python API

![High level architecture](/media/high_level_architecture.png)

## Detailed description of key parts of the software

### Python-server:
 * The server is started in pythonserver/main.py. It sets up a global variable which can be shared between the different scripts and classes of the server. Besides starting the webcam-feed, motor functionality, and water-level meter the file/script also starts an API-server (flask). This API-server is used for controlling the watering system from the webapp.
* The webcam-feed (pythonserver/webstream.py) is delivered through a socket which creates a webserver. This webserver is used in an iframe-window in the webapp.
 * Water level meter (pythonserver/water_level.py) is updated with a global variable set in main.py. It is then delivered to the webapp through the API.
 * The motor is controlled in (pythonserver/relay.py).

### Node.js webapp:
The user can login, see the webcam-feed, see the water level, and start the water pump for a selected number of seconds. The user also has the possibility to restart the server and stop the python-server, thereby eliminating the possibility to start the pump.

Some important files in the webapp:
* nodewebbapp/app.js: Start of the webserver.
* nodewebbapp/config/main.js: Includes the “secret” used for authentication (change to something else).
* nodewebbapp/models/user.js: Sets the model schema of the user (what is stored in the database). It also declares a number of useful functions connected to a User (e.g. when registering a user).
* nodewebbapp/routes/index.js: This route file both declares paths that will generate views but also contains API-endpoints, which in turn call the API-endpoints of the python-server. As an example, the Node GET API-endpoint "/check_water_level" will call the python-server's GET API-endpoint "/water_level_call" to fetch information about the water level.
* nodewebapp/views/index.ejs: This is the view that will be presented once the user is logged in. It includes a couple of javascript functions that call the different API-endpoints in "nodewebbapp/routes/index.js".

The only API-endpoint that cannot be triggered from the webapp's GUI is "/stop_server". I've chosen to not display this functionality as triggering this function by accident would stop the possibility to water the plants.

## Other:

Some additional work to make the system even more secure remains. Would be nice to ensure that the API-endpoints of the python-server are password protected (ideally with the password of the registered user). For now, only expose port 3000 for external uses if the watering system is deployed.
