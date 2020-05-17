sudo mongod --dbpath /home/pi/waterpump/nodewebapp/data &
sudo node /home/pi/waterpump/nodewebapp/app &
cd /home/pi/waterpump/pythonserver
sudo python3 main.py