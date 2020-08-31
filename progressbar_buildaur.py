#!/usr/bin/python3
# This module is written and maintained by lxgr and licensed under the GPL v3

import os
import sys
import math
import time

def format_bytes(size):
    power = 2**10
    n = 0
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 1))+' '+power_labels[n]

def progress(i, max, string):
    width, height = os.get_terminal_size()
    pl=round(math.log(width/57 ,1.01644658))
    string=' '+string+200*' '
    print('\r('+(len(str(max))-len(str(i)))*' '+str(i)+'/'+str(max)+')'+string[:width-16+(6-2*len(str(max)))-pl]+'['+round((i/max)*pl)*'#'+(pl-round((i/max)*pl))*'-'+'] '+(3-len(str(round((i/max)*100))))*' '+str(round((i/max)*100))+'%', end='', flush=True)

def dload(current, max, string, current_old, time_old):
    time_now=time.time()
    speed=(current-current_old)/(time_now-time_old)
    width, height = os.get_terminal_size()
    pl=round(math.log(width/57 ,1.01644658))
    string=' '+string+200*' '
    m, s = divmod(round((max-current)/speed), 60)
    print('\r'+string[:width-28-len(format_bytes(current))-pl]+format_bytes(current)+'iB'+(8-len(format_bytes(speed)))*' '+format_bytes(speed)+'iB/s '+(2-len(str(m)))*'0'+str(m)+':'+(2-len(str(s)))*'0'+str(s)+' ['+round((current/max)*pl)*'#'+(pl-round((current/max)*pl))*'-'+'] '+(3-len(str(round((current/max)*100))))*' '+str(round((current/max)*100))+'%', end='', flush=True)
    return current, time_now
