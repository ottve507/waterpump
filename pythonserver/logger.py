import smtplib
import datetime
import csv
import datetime as dt
import time
import traceback

class Logger:
    
    #Constructor for setting up database location, e-mail address to use etc.
    def __init__(self, config):
        self.config = config
        self.from_addr_username = config['e-mail']['from_addr_username']
        self.from_addr_password = config['e-mail']['from_addr_password']
        self.from_addr_smtp = config['e-mail']['from_addr_smtp']
        self.to_addr = config['e-mail']['to_addr']
    

    #send_email: Sends email to check what has happened
    def send_email(self, message):
        print(message)
        msg = "\r\n".join([
        "Subject: Waterpump update! \n" ,
        message,
        ])
        server = smtplib.SMTP(self.from_addr_smtp)
        server.ehlo()
        server.starttls()
        server.login(self.from_addr_username,self.from_addr_password)
        server.sendmail(self.from_addr_username, self.to_addr, msg)
        server.quit()
