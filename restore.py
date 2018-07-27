
#!/usr/bin/env Python
# -*-coding:utf-8 -*-

import os
import time
from fabric.api import *

env.hosts = ['root@192.168.0.191']
env.key_filename = "/root/.ssh/id_rsa"
bklocation = '/backupquantum'

def findfile():
    filename = prompt("Please input the filename that you want to find(absolute path):")
    if os.path.exists(bklocation + filename):
        print("%s exists!" % filename)
        answer = input("Do you need to restore the file %s? (y/n)" % filename)
        if answer == "y":
            dirname,filname = os.path.split(filename)
            with cd(dirname):
                with lcd(bklocation + dirname):
                    put(filname,filname)
        elif answer == "n":
            print("The peocess findfile is over!")
        else:
            answer = input("please input y/n!")

    else:
        print("%s not exists! Please confirm the file name!" % filename)
