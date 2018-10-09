#!/usr/bin/python3
""" Testing pylint"""
import sys
import os
import platform
import subprocess
import getopt
import pymysql
import pymssql
import json
import jsonpickle
from VirtualBox import VBoxManager
from VirtualBox import VirtualMachine

class CreateUser:
    """Creates a user on the database"""
    def __init__(self, username, password):
        self.username = username
        self.password = password
    def create(self):
        """Creates a user on the database"""
        try:
            db_connection = pymysql.connect("container.ittech24.co.uk", "sysadmin",
                                        "!512Cf61b", "ittech24")
        except pymysql.OperationalError:
            print("Error connecting to database")
        cursor = db_connection.cursor()
        sql = "select * from ittech24.users WHERE username='"+ self.username +"'"
        print(sql)
        cursor.execute(sql)
        data = cursor.fetchone()
        if data is None:
            print("user %s " % data[1])
        else:
            sql = "INSERT INTO ittech24.users (username,password) VALUES " \
                  "('"+self.username+"' ,PASSWORD('"+self.password+ "'))"
            cursor.execute(sql)
            subprocess.Popen("mkdir /var/ftp/"+self.username, shell=True,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
            subprocess.Popen("chown ftp:ftp /var/ftp/"+self.username, shell=True,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
def main(argv):
    username = None
    password = None
    print(platform.system())
    manager = VBoxManager("C:\Program Files\Oracle\VirtualBox")
    while True:
        command = input("Command: ")
        command = command.lower()    
        if manager.active:
            if command == "start":
                machine = input("Machine: ")
                if manager.startVm(machine):
                    print("Machine {0} started successfully".format(machine))
                else:
                    print("Machine {0} failed to start.".format(machine))
            if command == "startheadless":
                machine = input("Machine: ")
                if manager.startVm(machine, True):
                    print("Machine {0} started successfully".format(machine))
                else:
                    print("Machine {0} failed to start.".format(machine))
            if command == "pause":
                machine = input("Machine: ")
                if manager.pauseVm(machine):
                    print("Machine {0} paused successfully".format(machine))
                else:
                    print("Machine {0} failed to pause.".format(machine))            
            if command == "resume":
                machine = input("Machine: ")
                if manager.resumeVm(machine):
                    print("Machine {0} resumed successfully".format(machine))
                else:
                    print("Machine {0} failed to resume.".format(machine))
            if command == "reset":
                machine = input("Machine: ")
                if manager.resetVm(machine):
                    print("Machine {0} reseted successfully".format(machine))
                else:
                    print("Machine {0} failed to reset.".format(machine))
            if command == "stop":
                machine = input("Machine: ")
                if manager.stopVm(machine):
                    print("Machine {0} stopped successfully".format(machine))
                else:
                    print("Machine {0} failed to stop.".format(machine))
            if command == "screenshot":
                machine = input("Machine: ")
                if manager.takeScreenshot(machine):
                    print("Machine {0} screenshot created successfully".format(machine))
                else:
                    print("Machine {0} failed to create screenshot.".format(machine))
            if command == "description":
                machine = input("Machine: ")
                description = input("Description: ")
                if manager.setMachineDescription(machine, description):
                    print("Machine {0} description changed successfully".format(machine))
                else:
                    print("Machine {0} failed to change machine description.".format(machine))
            if command == "list":
                machines = manager.listVms()
                machinesJson = jsonpickle.encode(machines)
                for vm in machines:
                    print(vm.name + "-> " +vm.UUID)
                    # print(machinesJson)
            if command == "running":
                machines = manager.runningVms()
                machinesJson = jsonpickle.encode(machines)
                for vm in machines:
                    print(vm.name)
                    print(machinesJson)
            if command == "json":
                test = open("test.json","r")
                test3 = test.read()
                test1 = jsonpickle.decode(test3)
                test4 = VirtualMachine()
                test4.fromJson(test3)
                print(test4.name)
            if command == "quit":
                break
    try:
        opts, args = getopt.getopt(argv, "u:p:", ["username=", "password="])
    except getopt.GetoptError:
        print("Please choose a username and a password")
        sys.exit(2)
    print(opts)
    for opt, arg in opts:
        if opt == "-u":
            username = arg
        if opt == "-p":
            password = arg

    if username != None and password != None:
        user = CreateUser(username, password)
        user.create()

if __name__ == "__main__":
    main(sys.argv[1:])

