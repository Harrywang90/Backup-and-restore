#!/usr/bin/env Python
# -*- coding:utf-8 -*-

import time
import os
import paramiko
from fabric.api import *
from fabric.colors import *

env.hosts = ['192.168.0.191']
env.user = 'root'
env.key_filename = '/root/.ssh/id_rsa'
#backupdir = ['home','home2','home3','project','apps']
backupdir = ["/home"]
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
key =paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa')
bksvpath = '/backupquantum/'
host='192.168.0.191'

def get_fullbackup(directory):
    with settings(warn_only=True):
    # if occupy error or warn ,ignore and continue
        with cd(directory):
    # change the remote working directory to the directory that needed backup

        #    if not os.path.exists(bksvpath + directory):
        #        print('not exists   Mking dir.......')
        #        with lcd(bksvpath):
        #            local('mkdir -p %s ' % directory)
        #    else:
        #        print('exists!') 
            with lcd(bksvpath + directory):  #local change to the path where backupfile locate  
                for dire in get_dir(directory):   # get the directory in the remote working directory
                    get_fullbackup(dire)          # if it's directory ,go back cicle 
                for fil in get_file(directory):   # get the file in the remote working directory
                    file_get = get(fil, fil)      # to the local path 
                    absolute_file = run("pwd") + "/" + fil
                    local("echo %s \<--- %s/%s >> /backupquantum/backup.log" % (file_get, host, absolute_file))
                    # note the backup log 

def get_incbackup(directory):
    with settings(warn_only=True):
        with cd(directory):
            if not os.path.exists(bksvpath + directory):
                # print('/backupquantum/%s do  not exists.That will do fullback the directory' % directory)
                get_fullbackup(directory)
            else:
                # print('/backupquantum/%s do exists.Please go on.' % directory ) 
                with lcd(bksvpath + directory):
                for dire in get_dir(directory):
                        get_incbackup(dire)
                    for fil in get_file(directory):
                        # file_absolute = os.path.abspath(fil) 
                        os.chdir(bksvpath + directory)
                        # print(os.listdir('./'))
                        lo = local("pwd")
                        # print("lo = %s " % lo)
                        if not os.path.exists(fil):
                            # print('fil is %s ' % fil)
                            # print('file_absolute is %s' % file_absolute)
                            # print('%s  not exists ,,need backup!' % fil)
                            file_get = get(fil,fil)
                            absolute_file = run("pwd") + '/' + fil
                            #print('absolute_file is %s' % absolute_file)
                            local("echo %s \<--- %s/%s >> /backupquantum/backup.log" % (file_get, host, absolute_file))
                        elif os.path.exists(fil):
                            #print("%s  exists, need judge mtime" % fil)
                            #remo_modify_time = run("stat %s | grep Modify | awk '{print $2i$3}' i=' '" % fil)
                            #remote_modify_time = remo_modify_time.split('.')[0]
                            #local_modify_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.stat(fil).st_mtime
)) 
                            #print('%s modify remo: %s   local : %s' % (fil, remote_modify_time, local_modify_time))    
                          

                            #According to test , it's not right to judge by mtime!
                            #So dicede to judge by MD5sum
                            remo_md5 = run("md5sum %s | awk '{print$1}'" % fil)
                            # print("%s de re_md5 is %s" % (fil,remo_md5))
                            s = os.popen("md5sum %s | awk '{print$1}'" % fil)
                            local_md5 = s.readlines()[0].split()[0]
                            # print("%s de local_md5 is %s" % (fil,local_md5))                            
                            if remo_md5 == local_md5:
                                print("File %s is not changed!" % fil)
                            else:
                                file_get = get(fil,fil)
                                absolute_file = run("pwd") + '/' + fil
                                local("echo %s \<--- %s/%s >> /backupquantum/backup.log" % (file_get, host, absolute_fil
e))

def get_dir(dire):
    ssh.connect(host,22,env.user,pkey=key)
    stdin,stdout,stderr = ssh.exec_command("cd %s &&ls -l | grep '^d'| awk '{print i$9}' i=`pwd`'/'" % dire)
    #print('host %s ---dir %s :' % (host,backupdir[0]))
    dir_resault = []
    for i in stdout.readlines():
        dir_resault.append(i.split('\n')[0])
    # print(dir_resault)
    
    ssh.close()
    return dir_resault

def get_file(dire):
    ssh.connect(host,22,env.user,pkey=key)
    stdin,stdout,stderr = ssh.exec_command("cd %s && ls -al | grep '^-'| awk '{print$9}' | egrep -v *\\.trn$\|*\\.dsn$\|
*\\.tran$\|*\\.fsdb$\|*\\.vcd$ " % dire)
    file_resault = []
    for i in stdout.readlines():
        file_resault.append(i.split('\n')[0])
    # print(file_resault)
    ssh.close()
    return file_resault


def test(dire):
    with settings(warn_only=True):
        pass




def run_backup():
    backupdate = time.strftime("%Y-%m-%d", time.localtime())
    backup_start_time = time.strftime("%H:%M", time.localtime())
    local("echo ========================================================================================================
================ >> /backupquantum/backup.log")
    local("echo ==================%s=start=backup===================== >> /backupquantum/backup.log" % backupdate)
    local("echo ==================start=time==%s=========================== >> /backupquantum/backup.log" % backup_start
_time)
    #local_modify_time = os.stat('/root/test/backup.log').st_ctime
    #print(backupdate)
    #print(backup_start_time)
    for i in backupdir:
        get_incbackup(i)
    backupdate_end = time.strftime("%Y-%m-%d", time.localtime())
    backup_end_time = time.strftime("%H:%M", time.localtime())
    local("echo ====================%s=end=backup===================== >> /backupquantum/backup.log" % backupdate_end)
    local("echo ====================end=time==%s=========================== >> /backupquantum/backup.log" % backup_end_t
ime)
~               
                                                            
                
