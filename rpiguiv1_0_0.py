#!/usr/bin/env python

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

import subprocess
import os
from gpiozero import CPUTemperature
import dictionary


root = Tk();
root.title("RPI Info GUI v1.0.0")
root.geometry('{}x{}'.format(300, 300))

rawModel = subprocess.check_output("cat /proc/cpuinfo | grep 'Revision' | awk '{print $3}' | sed 's/^1000//'", shell=True)
rawHostname = subprocess.check_output("hostname")
rawIp = subprocess.check_output(["hostname", "-I"])
rawSSID = subprocess.check_output("iwlist wlan0 scan | grep 'ESSID' | sed -e 's/ESSID://' -e 's/\"//g' -e 's/^ *//g'", shell=True)

decodedModel = rawModel.decode("utf-8")
modelVer = dictionary.model.get(decodedModel.rstrip())

hostname = rawHostname.decode("utf-8")
ip = rawIp.decode("utf-8")
ssid = rawSSID.decode("utf-8")

def loop():
    cpu = CPUTemperature()
    temp = cpu.temperature
    cpuLabel.config(text=str(temp))
    cpuLabel.pack()
    cpuLabel.after(2000, loop)

hardware = Label(root, text="Hardware Information", bg='black', fg='white')
hardware.pack(fill=X)

cpuTitle = Label(root, text="CPU Temperature", bg="grey")
cpuTitle.pack(fill=X)

cpuLabel = Label(root, fg="green")
cpuLabel.pack(pady=5)

modelTitle = Label(root, text="Raspberry Pi Model", bg="grey")
modelTitle.pack(fill=X)

modelLabel = Label(root, text=modelVer, fg="green")
modelLabel.pack(pady=5)

network = Label(root, text="Network Information", bg='black', fg='white')
network.pack(fill=X)

hostnameTitle = Label(root, text="Hostname", bg="grey")
hostnameTitle.pack(fill=X)

hostnameLabel = Label(root, text=hostname, fg="green")
hostnameLabel.pack()

ipTitle = Label(root, text="IP Address", bg="grey")
ipTitle.pack(fill=X)

ipLabel = Label(root, text=ip, fg="green")
ipLabel.pack()

ssidTitle = Label(root, text="SSID", bg="grey")
ssidTitle.pack(fill=X)

ssidLabel = Label(root, text=ssid, fg="green")
ssidLabel.pack()

root.after(500, loop);
root.mainloop()
