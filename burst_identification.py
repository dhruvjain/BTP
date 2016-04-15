import os
import fonte_nossdav_properties as p
import sata
#import datactrl_static_train as dcst
import numpy as np
import packetsize_freq_dist as pfd
import pickle
import json

##########################################

def divideIntoBurstsForCurrentTrace (tracePath, threshold):

    print "Threshold for " + tracePath + " is " + str(threshold)

    bursts = []
    multiplier = 1000000

    readfp = open(tracePath,"r")
    lines = readfp.readlines()
    readfp.close()

    packets = []

    startTime = 20*multiplier
    endTIme = 140*multiplier

    for line in lines:
        if (pfd.isDataPacket(line)):
            tokens = line.split(',')
            seq = int(tokens[0])
            time = int(np.ceil(float(tokens[1])*multiplier))
            packetsize = int(tokens[3])

#            change

            if(time>=startTime and time <= endTIme):
                packets.append((seq,time,packetsize))

    dataPackets = []
    startTime = packets[0][1]
    prevTime = startTime
    dataPackets.append((packets[0][0],packets[0][1],0,packets[0][2]))
    
    prevPacketInvalid = False
    for packet in packets[1:]:
        
        if prevPacketInvalid:
            iat = int(np.ceil((packet[1] - prevTime)/2))
        else:
            iat = packet[1]-prevTime
            
        prevPacketInvalid = False

        if iat > 0:
            dataPackets.append((packet[0],packet[1],iat,packet[2]))
            prevTime = packet[1]
        else:
            prevPacketInvalid = True

    if dataPackets[1][2]<threshold:
        bursts.append([dataPackets[0]])
    for dataPacket in dataPackets[1:]:
        if dataPacket[2] > threshold:
            bursts.append([dataPacket])

    #print(bursts)

    pktCount = len(dataPackets)
    #pc = 0
    burstCount = len(bursts)
    #bc = 0
    for i in range(0,burstCount):
        startSeq = bursts[i][0][0]
        nextBurstStartSeq = 0
        if i < (burstCount-1):
            nextBurstStartSeq = bursts[i+1][0][0]
        for j in range(0,pktCount):
            if dataPackets[j][0] == startSeq:
                j += 1
                break
            j += 1
        if nextBurstStartSeq == 0:
            for k in range(j,pktCount):
                if dataPackets[k][2] > threshold:
                    print("Greater than threshold!")
                bursts[i].append(dataPackets[k])
        else:
            for k in range(j,pktCount):
                if dataPackets[k][0] == nextBurstStartSeq:
                    break
                if dataPackets[k][2] > threshold:
                    print("Greater than threshold!")
                bursts[i].append(dataPackets[k])
    
    return bursts    
        
##########################################

def divideIntoBursts (appName, threshold):

    traceParent = os.path.join(p.CSV_PARENT_PATH,appName)
    allTraces = [os.path.join(os.path.join(traceParent,d)) for d in os.listdir(traceParent)]
    traces = dcst.getStaticScenarioList(allTraces)
    if appName == "YouTube":
        traces.append(os.path.join(p.TRACE_PARENT_PATH,"Long.Traces","youtube_30mins.csv"))
    elif appName == "YouTubeLive":
        traces.append(os.path.join(p.TRACE_PARENT_PATH,"Long.Traces","youtubelive_90mins.csv"))
    
    allBursts = []

    for trace in traces:
        print("Divide into bursts for trace: "+trace)
        traceBursts = divideIntoBurstsForCurrentTrace(trace,threshold)
        for burst in traceBursts:
            allBursts.append(burst)
        #break
    #print(allBursts)
    print "Dumping allBursts objects for this app..."
    pickle.dump(allBursts,open(os.path.join(p.PROJECT_PARENT_PATH,"BURST",appName+".burst"),"wb"))
    print "Done!"

    return

##########################################

def main():

    #app_threshold_list = [('YouTube',35000),('HotStar',13000),('StarSports',47000),('YouTubeLive',20000)]
    #app_threshold_list = [('YouTube',35000)]

    appName = "YouTube"

    fp = open(os.path.join(p.PLOT_PARENT_PATH,"burst_thresholds.txt"),'r')
    lines = fp.readlines()
    fp.close()

    for line in lines:
        tokens = line.split(',')
        traceBursts = divideIntoBurstsForCurrentTrace(os.path.join(p.CSV_PARENT_PATH,appName,tokens[0]),int(tokens[1]))
        #print("Dumping all bursts for trace: " + tokens[0])
        print "Total burst = ", len(traceBursts)
        #pickle.dump(traceBursts,open(os.path.join(p.BURSTS_PARENT_PATH,appName,tokens[0].split('.')[0]+".burst"),"wb"))
        #print("Done!")

    return

##########################################

if __name__ == "__main__":
    main()
