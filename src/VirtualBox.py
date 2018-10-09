import sys
import subprocess
import getopt
import json
import os
import time
import platform
from Helpers import File

class VirtualMachine:
    def __init__(self, name ="", id = ""):
        self.name = name
        self.UUID = id
        self.running = False
        self.groups = ""
        self.ostype = ""
        self.__path = "test"
            
    def fromJson(self,obj):
        self.__dict__ = json.loads(obj)

class VBoxManager:
    """VirtualBox Manager Module for Ittech24
    
        This will allow to have control over the installed virtual machines on the system
    """
    def __init__(self, path = None):
        self.version = None
        self.errorMessage = None
        self.path = ""
        self.active = False
        # Checking the undelying operating system to check where to find the needed executable
        if platform.system().lower() == "linux":
            self.path = "vboxmanage"
        elif platform.system().lower() == "windows":
            self.path = "\"{0}\\vboxmanage.exe\"".format(path)
        else:
            self.errorMessage = "Unknown operating system, cannot continue."        
        # Checking if we found a valid operating system
        if self.path != "":
            self.active = self.__check()
            self.virtualMachines = self.listVms()
            self.ScreenshotOutput = ""

    def startVm(self, name, headless = False):
        """Starts a virtual machine by it's name (name is case insensitive)
        """
        if self.active:
            if not self.isVmRunning(name):
                #trying to find the machine on the list of  machines
                machineId = self.__getMachineId(name)
                if machineId != None:
                    if headless:
                        return self.__executeCmd("startvm {0} --type headless".format(machineId))[0]
                    else:
                        return self.__executeCmd("startvm {0}".format(machineId))[0]
        return False
    
    def stopVm(self, name):
        """Stops a virtual machine by it's name"""
        if self.active:
            if self.isVmRunning(name):
                machineId = self.__getMachineId(name)
                if machineId != None:
                    return self.__executeCmd("controlvm {0} poweroff".format(name))
                else:
                    return False
            else:
                return False
        return False

    def pauseVm(self, name):
        """Pause a virtual machine by it's name"""
        if self.active:
            if self.isVmRunning(name):
                machineId = self.__getMachineId(name)
                if machineId != None:
                    return self.__executeCmd("controlvm {0} pause".format(name))
                else:
                    return False
            else:
                return False
        return False
        
    def resumeVm(self, name):
        """Resume a virtual machine by it's name"""
        if self.active:
            if self.isVmRunning(name):
                machineId = self.__getMachineId(name)
                if machineId != None:
                    return self.__executeCmd("controlvm {0} resume".format(name))
                else:
                    return false
            else:
                return False
        return False
    
    def resetVm(self, name):
        """Reset a virtual machine by it's name"""
        if self.active:
            if self.isVmRunning(name):
                machineId: self.__getMachineId(name)
                if machineId != None:
                    return self.__executeCmd("controlvm {0} reset".format(name))
                else:
                    return False
            else:
                return False
        return False
    
    def takeScreenshot(self, name):
        if self.active:
            if self.isVmRunning(name):
                dir_path = os.path.dirname(os.path.realpath(__file__))
                if self.ScreenshotOutput:
                    dir_path = self.ScreenshotOutput
                dir_path += "\\{0}_{1}.png".format(name,time.time())
                return self.__executeCmd("controlvm {0} screenshotpng \"{1}\"".format(name,dir_path))
            else:
                return False
        return False

    def setMachineDescription(self, name, description):
        if self.active:
            return self.__executeCmd("modifyvm {0} --description \"{1}\"".format(name,description))
        return False

    def isVmRunning(self, name):
        """Checks if a Virtual Machine is running"""
        if self.active:
            running = self.runningVms()

            if len(running) > 0:
                for vm in running:
                    if isinstance(vm, VirtualMachine):
                        vmName = vm.name.lower().replace(" ","")
                        name = name.lower().replace(" ", "")
                        if vmName == name:
                            return True
            return False
        return False

    def refreshVms(self):
        """Refresh list Virtual Machines that are currently created on the system"""
        if self.active:
            self.virtualMachines = self.listVms()

    def runningVms(self):
        """List Virtual Machines that are currently running on the system"""
        if self.active:
            virtualMachines = []
            outputStr = ""
            state, output = self.__executeCmd("list runningvms")
            if state:
                if output:
                    if isinstance(output, bytes):
                        outputStr = output.decode("utf8")
                    elif isinstance(output, str):
                        outputStr = output
                    vms = outputStr.split("\n")
                    for vmStr in vms:
                        separator = vmStr.find("{")
                        vmName = vmStr[0:separator].strip()
                        vmUUID = vmStr[separator:len(vmStr)].strip()
                        if len(vmName) > 1:
                            vmName = vmName.replace("\"","")
                            vmUUID = vmUUID.replace("{","")
                            vmUUID = vmUUID.replace("}","")
                            if vmName:
                                vm = VirtualMachine(vmName, vmUUID)
                                vm.running = self.isVmRunning(vm.name)
                                virtualMachines.append(vm)                        
            return virtualMachines
        return []

    def listVms(self):
        """List Virtual Machines that are currently created on the system"""
        if self.active:
            virtualMachines = []
            outputStr = ""
            state, output = self.__executeCmd("list vms")
            if state:
                if output:
                    if isinstance(output, bytes):
                        outputStr = output.decode("utf8")
                    elif isinstance(output, str):
                        outputStr = output
                    vms = outputStr.split("\n")
                    for vmStr in vms:
                        separator = vmStr.find("{")
                        vmName = vmStr[0:separator].strip()
                        vmUUID = vmStr[separator:len(vmStr)].strip()
                        if len(vmName) > 1:
                            vmName = vmName.replace("\"","")
                            vmUUID = vmUUID.replace("{","")
                            vmUUID = vmUUID.replace("}","")
                            if vmName:
                                vm = VirtualMachine(vmName, vmUUID)
                                vm.running = self.isVmRunning(vm.name)
                                virtualMachines.append(vm)                        
            return virtualMachines
        return []

    def __check(self):
        """Testing if there is a VBoxManager to use"""
        return self.__executeCmd("--version")[0]
    
    def __getMachineId(self, name):
        name = name.replace(" ","").lower()
        for machine in self.virtualMachines:
            machineName = machine.name.replace(" ","").lower()
            if machineName == name:
                return machine.UUID
        return None

    def __updateVmState(self, name, state):
        for vm in self.virtualMachines:
            if vm.name == name:
                vm.running = state
    
    def __getMachineInfo(self, name):
        if self.active:
            state, output = self.__executeCmd("showvminfo {0} --machinereadable".format(name))
            return output


    def __executeCmd(self, args = []):
        cmd = self.path
        if args:
            cmd += " "
            for arg in args:
                cmd += arg
        cmd = subprocess.Popen(cmd, shell=True,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE)
        output, error = cmd.communicate()
        if isinstance(output, bytes):
            if output:
                return True, output
            else:
                return False, None
        else:
            if isinstance(error,bytes):
                self.errorMessage = error.decode("utf8").strip()
            return False, None
