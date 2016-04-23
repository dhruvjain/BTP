from collections import defaultdict
import fonte_nossdav_properties as p
import operator
import numpy as np
import os
import pickle

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
        proto) or (":eapol" in proto) or (packetSize<=68):  #or ("192.168" in src) 
        isData = False

    return (isData)


###############################################################################

def getTotalIATFreq(absFilePath):

    totalIATFreq = defaultdict(int)
    totalTime = 0.0
    
    dataPackets = []
    readfp = open(absFilePath,'r')
    lines = readfp.readlines()

    startTime = 0*p.multiplier
    endTime = 10000000*p.multiplier
    for line in lines:
        if (isDataPacket(line)):
            pkt_at = int(np.ceil(float(line.split(',')[1])*p.multiplier))
            if pkt_at >= startTime and pkt_at <= endTime:
                dataPackets.append(line) 

    startTime = int(np.ceil(float(dataPackets[0].split(',')[1])*p.multiplier))  #[1] is AT
    endTime = int(np.ceil(float(dataPackets[len(dataPackets)-1].split(',')[1])*p.multiplier))

    prevTime = startTime

    for index, pkt in enumerate(dataPackets[1:]):
        currTime = int(np.ceil(float(pkt.split(',')[1])*p.multiplier))
        iat = currTime - prevTime
        
        if iat>=0 and currTime<=endTime:
            totalIATFreq[iat] += 1
            prevTime = currTime

    readfp.close()
    totalTime += (endTime - startTime)

    sortedIATFreq = sorted(totalIATFreq.items(), key=operator.itemgetter(0,1))

    return sortedIATFreq, totalTime, dataPackets


#################################################################

def divideIntoBursts(dataPackets, height, tick, min_pkts):
    #By defining height I am removing small small packets spread across regions
    #By defining min_pkts I am removing very very small bursts with small amount of packets
    bursts = []
    allBursts = []
    beg = 0  #has a burst begun?

    tick = tick*p.multiplier
    startTime = int(np.ceil(float(dataPackets[0].split(',')[1])*p.multiplier))
    endTime = startTime + tick
    No_of_pkts = 1
    total_pkts = 1
    prevTime = startTime
    prevTick_end = startTime  

    #Here I am storing the start time and end time of each bursts
    for index, pkt in enumerate(dataPackets[1:]):
        currTime = int(np.ceil(float(pkt.split(',')[1])*p.multiplier))

        if currTime<endTime:
            No_of_pkts += 1
            prevTime = currTime
        else:
            if (No_of_pkts < height and beg == 1) or (currTime >= (prevTime+tick)):
                if total_pkts >= min_pkts:
                    bursts.append([startTime*1.0/p.multiplier, prevTick_end*1.0/p.multiplier])
                startTime = currTime
                beg = 0
                total_pkts = 0
            
            elif No_of_pkts < height and beg == 0:
                startTime = currTime
                total_pkts = 0

            elif No_of_pkts >= height and beg == 0:
                beg = 1
                prevTick_end = prevTime
                total_pkts = No_of_pkts

            elif No_of_pkts >= height and beg == 1:
                prevTick_end = prevTime
                total_pkts += No_of_pkts

            endTime = currTime + tick
            No_of_pkts = 1

    #Now I will make a list of bursts i.e. list of list of packets
    index = 0
    burst_no = 0
    while index < len(dataPackets) and burst_no < len(bursts):

        currTime = int(np.ceil(float(dataPackets[index].split(',')[1])*p.multiplier))
        
        while currTime < bursts[burst_no][0]*p.multiplier:
            index += 1
            currTime = int(np.ceil(float(dataPackets[index].split(',')[1])*p.multiplier))

        present_burst = []
        while currTime < bursts[burst_no][1]*p.multiplier:
            present_burst.append(dataPackets[index])
            index += 1
            currTime = int(np.ceil(float(dataPackets[index].split(',')[1])*p.multiplier))

        present_burst.append(dataPackets[index])  #appending the last packet of burst
        allBursts.append(present_burst)   
        burst_no += 1
        index += 1

    return bursts, allBursts

#################################################################

def change_allBursts(allBursts):

    new_allBursts = []
    for burst in allBursts:
        new_burst = []
        for packet in burst:
            new_packet = packet[:-1].split(',')
            new_packet[1] = float(new_packet[1])
            new_packet[3] = int(new_packet[3])
            new_burst.append(new_packet)

        new_allBursts.append(new_burst)

    return new_allBursts

#################################################################

def dumpBurst(app, filePath, new_allBursts):

    print filePath
    
    if "all" not in filePath:
        print "Total no. of bursts = ", len(new_allBursts)
        path = os.path.join(p.BURSTS_PARENT_PATH, app, filePath.split('.')[0]+".burst")
        pickle.dump(new_allBursts, open(path,"wb"))
        return

    num_videos = 7
    min_len_video = 200
    count_videos = 1
    l_ibat = []
    videos = []

    for index, burst in enumerate(new_allBursts[1:]):
        ibat = new_allBursts[index+1][0][1] - new_allBursts[index][len(new_allBursts[index])-1][1]
        l_ibat.append(ibat)

    l_ibat.sort()
    threshold = l_ibat[-num_videos] - 1

    for index, burst in enumerate(new_allBursts[1:]):
        ibat = new_allBursts[index+1][0][1] - new_allBursts[index][len(new_allBursts[index])-1][1]
        if ibat < threshold  and index!= (len(new_allBursts[1:])-1):
            videos.append(burst)
        elif count_videos <= num_videos:
            if index == (len(new_allBursts[1:])-1):
                videos.append(burst)

            if videos is not []:
                if videos[-1][-1][1] - videos[0][0][1] < min_len_video:
                    continue

            print "Total no. of bursts = ", len(videos)
            path = os.path.join(p.BURSTS_PARENT_PATH, app, filePath.split('.')[0]+"_"+str(count_videos)+".burst")
            print path
            pickle.dump(videos, open(path,"wb"))
            count_videos += 1
            videos = []

    print "Done!! Total ", (count_videos - 1), "found"

#################################################################

#totalIATFreq contains sorted IAT and no. of packets in that IAT
def main():
    appNames = ['YouTube']

    for app in appNames:
        if os.path.exists(os.path.join(p.CSV_PARENT_PATH,app)):
            for filePath in os.listdir(os.path.join(p.CSV_PARENT_PATH,app)):
                if not filePath.startswith('.'):

                    absFilePath = os.path.join(p.CSV_PARENT_PATH,app,filePath)
                    totalIATFreq, totalTime, dataPackets = getTotalIATFreq(absFilePath)
                    bursts, allBursts = divideIntoBursts(dataPackets, 55, 0.1, 600)
                    new_allBursts = change_allBursts(allBursts)
                    dumpBurst(app, filePath, new_allBursts)

    return

##################################################################

if __name__ == '__main__':
    main()
