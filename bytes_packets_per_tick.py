import numpy as np
import os
#import datactrl_static_train as dcst
from collections import defaultdict
import operator
import fonte_nossdav_properties as p
import sys

#################################################################

''' Return whether the current line represents a data packet '''

def isDataPacket(line):

    packetSize = int(line.split(',')[3])

    isData = True
    proto = line.split(',')[2]
    src = line.split(',')[4]
    dest = line.split(',')[5]
    if ("db-lsp-disc" in proto) or (":pkcs" in proto) or (":dns" in
        proto) or (":icmp" in proto) or (":arp" in proto) or (":igmp" in
        proto) or (":ntp" in proto) or ("dcp-etsi" in proto) or (":xmpp" in
        proto) or (":nbdgm" in proto) or (":nbns" in proto) or (":bjnp" in
        proto) or (":bootp" in proto) or (":vssmonitoring" in
        proto) or (":stun" in proto) or (":portcontrol" in proto) or (":echo" in
        proto) or (":eapol" in proto) or ("192.168" in src) or (packetSize<=68):
        isData = False

    return (isData)

#################################################################

def getBytesPerTick(absFilePath,tick):

    downloadPackets = []
    bytesPerTick = []
    tick = int(tick*1000000)

    readfp = open(absFilePath,'r')
    lines = readfp.readlines()
    startTime = int(float(lines[0].split(',')[1])*1000000)
    
    for line in lines:
        if (isDataPacket(line)):
            downloadPackets.append(line)
    readfp.close()
    
    endTime = int(float(downloadPackets[len(downloadPackets)-1].split(',')[1])*1000000)

    startTime += (endTime - startTime)%tick
    currStartTime = startTime
    currAccumulatedBytes = 0

    for line in downloadPackets:
        tokens = line.split(',')
        packetSize = int(tokens[3])
        time = int(float(tokens[1])*1000000)
        if time >= startTime:
            if time == endTime:
                bytesPerTick.append(currAccumulatedBytes+packetSize)
            elif (time - currStartTime) > tick:
                currStartTime = currStartTime+tick
                bytesPerTick.append(currAccumulatedBytes)
                currAccumulatedBytes = packetSize
            else:
                currAccumulatedBytes += packetSize

    return bytesPerTick

#######################################################################################################

def getPacketsPerTick(absFilePath,tick):

    downloadPackets = []
    packetsPerTick = []
    multiplier = 1000000
    tick = int(tick*multiplier)

    readfp = open(absFilePath,'r')
    lines = readfp.readlines()
    startTime = int(float(lines[0].split(',')[1])*multiplier)

    for line in lines:
        if (isDataPacket(line)):
            downloadPackets.append(line)
    readfp.close()

    endTime = int(float(downloadPackets[len(downloadPackets)-1].split(',')[1])*1000000)
    
    startTime = 20*multiplier
    endTime = 140*multiplier
          
    startTime += (endTime - startTime)%tick
    currStartTime = startTime
    currAccumulatedPackets = 0
   
    for line in downloadPackets:
        tokens = line.split(',')
        time = int(float(tokens[1])*multiplier)
        if time >= startTime:
            if time == endTime:
                packetsPerTick.append(currAccumulatedPackets+1)
            elif (time - currStartTime) > tick:
                currStartTime = currStartTime+tick
                packetsPerTick.append(currAccumulatedPackets)
                currAccumulatedPackets = 1
            else:
                currAccumulatedPackets += 1

    return packetsPerTick

#################################################################

def writeAsArray (perTickList, filePath, borp, tick):

    arr = "a = ["
    for i in perTickList:
        arr += str(i)+" "
    arr = arr[:-1]
    arr += "];\n"
    arr += "psd(a);\n"
    arr += "saveas(gcf,"
    arr += "'psd_" + filePath.split('.')[0] + "', 'epsc')\n"
    

    targetDir = os.path.join(p.PLOT_PARENT_PATH,"Matlab.Arrays")
    if not(os.path.exists(targetDir)):
        os.mkdir(targetDir)

    targetDir = os.path.join(targetDir, borp + "_" + tick)
    if not(os.path.exists(targetDir)):
        os.mkdir(targetDir)
    
    fp = open(os.path.join(targetDir, filePath.split('.')[0]+".txt"), "w")
    fp.write(arr)
    fp.close()

    return

#################################################################

def main(argv):
    #appNames = ['YouTube','TED','HotStar','YouTubeLive','StarSports','TimesNow','Skype','GoogleHangouts','ooVoo']
    appNames = ['YouTube']
    tick = float(argv[1])

    if argv[0] == 'b':
        bytes = True
    elif argv[0] == 'p':
        bytes = False
    else:
        print "Invalid option"
        sys.exit(0)

    for app in appNames:
        if os.path.exists(os.path.join(p.CSV_PARENT_PATH,app)):
            for filePath in os.listdir(os.path.join(p.CSV_PARENT_PATH,app)):
                if not filePath.startswith('.'):
                    absFilePath = os.path.join(p.CSV_PARENT_PATH,app,filePath)
                    if bytes:
                        #print "Calling getBytesPerTick"
                        bytesPerTick = getBytesPerTick(absFilePath,tick)
                        writeAsArray(bytesPerTick,filePath,argv[0],argv[1])
                    else:
                        packetsPerTick = getPacketsPerTick(absFilePath,tick)
                        writeAsArray(packetsPerTick,filePath,argv[0],argv[1])
                    print("Data generated for "+filePath+".")
    return

################################################################

if __name__ == "__main__":
    main(sys.argv[1:])

