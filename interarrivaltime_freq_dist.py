from collections import defaultdict
import fonte_nossdav_properties as p
import operator
import numpy as np
import os
import pickle
#import datactrl_static_train as dcst
import packetsize_freq_dist as pfd
import matplotlib.pyplot as plt 

###############################################################################

def getTotalIATFreq(absFilePath):
    multiplier = 1000000

    totalIATFreq = defaultdict(int)
    totalTime = 0.0
    
    dataPackets = []
    readfp = open(absFilePath,'r')
    lines = readfp.readlines()
    for line in lines:
        if (pfd.isDataPacket(line)):
            dataPackets.append(line) 

    #print dataPackets
    startTime = int(np.ceil(float(dataPackets[0].split(',')[1])*multiplier))  #[1] is AT
    endTime = int(np.ceil(float(dataPackets[len(dataPackets)-1].split(',')[1])*multiplier))
    #endTime = 100*multiplier
    print "Endtime is ", endTime
    prevTime = startTime

    for index, pkt in enumerate(dataPackets[1:]):
        currTime = int(np.ceil(float(pkt.split(',')[1])*multiplier))
        iat = currTime - prevTime
        
        if iat>=0 and currTime<=endTime:
            totalIATFreq[iat] += 1
            prevTime = currTime

    readfp.close()
    totalTime += (endTime - startTime)

    sortedIATFreq = sorted(totalIATFreq.items(), key=operator.itemgetter(0,1))

    return sortedIATFreq, totalTime, dataPackets

###############################################################################

def getFinalIATFreq(totalIATFreq,totalTime,granularity):
    finalIATFreq = []
    for tuple in totalIATFreq:
        finalIATFreq.append((tuple[0],int(np.ceil((tuple[1]/totalTime)*granularity))))
    return finalIATFreq

#################################################################

def getCDF(totalIATFreq):
    cdfIATFreq = []
    totalFreq = 0
    for dataPoint in totalIATFreq:
        totalFreq += dataPoint[1]   #datapoint consists of (ms_of_IAT, No_of_pkts)

    cumulativeFreq = 0
    cdf = 0.123456789
    for dataPoint in totalIATFreq:
        cumulativeFreq += dataPoint[1]
        cdf = (cumulativeFreq*1.0)/(totalFreq*1.0)  #cdf here is a fraction
        cdfIATFreq.append((dataPoint[0],cdf))

    return cdfIATFreq


#################################################################

def reportBurstThreshold(filePath,threshold):
    fp = open(os.path.join(p.PLOT_PARENT_PATH,"burst_thresholds.txt"),'a')
    fp.write(filePath+","+str(threshold)+"\n")
    fp.close()
    return    

#################################################################

def createPlotFile(plotPath,finalIATFreq):
    writefp = open(plotPath,'w')
    c = 0
    for tuple in finalIATFreq:
        #writefp.write(str(c)+" "+str(tuple[0])+" "+str(tuple[1])+"\n")
        if c!=0:
            writefp.write("\n");
        writefp.write(str(tuple[0])+" "+str(tuple[1]))
        c += 1
    writefp.close()
    return True


#################################################################


def showPlotFile(plotPath, x, y):
    plt.plotfile(plotPath, delimiter=' ', cols=(0, 1), names=(x, y), marker='o');
    plt.show()


#################################################################

def divideIntoBursts(dataPackets, height, tick, min_pkts):
    #By defining height I am removing small small packets spread across regions
    #By defining min_pkts I am removing very very small bursts with small amount of packets
    multiplier = 1000000
    bursts = []
    allBursts = []
    beg = 0  #has a burst begun?

    tick = tick*multiplier
    startTime = int(np.ceil(float(dataPackets[0].split(',')[1])*multiplier))
    endTime = startTime + tick
    No_of_pkts = 1
    total_pkts = 1
    prevTime = startTime
    prevTick_end = startTime  

    #Here I am storing the start time and end time of each bursts
    for index, pkt in enumerate(dataPackets[1:]):
        currTime = int(np.ceil(float(pkt.split(',')[1])*multiplier))
        if currTime<endTime:
            No_of_pkts += 1
            prevTime = currTime
        else:
            if No_of_pkts < height and beg == 1:
                if total_pkts >= min_pkts:
                    bursts.append([startTime*1.0/multiplier, prevTick_end*1.0/multiplier])
                startTime = currTime
                beg = 0
                total_pkts = 0
            
            if No_of_pkts < height and beg == 0:
                startTime = currTime
                total_pkts = 0

            if No_of_pkts >= height and beg == 0:
                beg = 1
                prevTick_end = prevTime
                total_pkts = No_of_pkts

            if No_of_pkts >= height and beg == 1:
                prevTick_end = prevTime
                total_pkts += No_of_pkts

            endTime = currTime + tick
            No_of_pkts = 1

    #Now I will make a list of bursts i.e. list of list of packets
    index = 0
    burst_no = 0
    while index < len(dataPackets) and burst_no < len(bursts):

        currTime = int(np.ceil(float(dataPackets[index].split(',')[1])*multiplier))
        
        while currTime < bursts[burst_no][0]*multiplier:
            index += 1
            currTime = int(np.ceil(float(dataPackets[index].split(',')[1])*multiplier))

        present_burst = []
        while currTime < bursts[burst_no][1]*multiplier:
            present_burst.append(dataPackets[index])
            index += 1
            currTime = int(np.ceil(float(dataPackets[index].split(',')[1])*multiplier))

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

def main():
    appNames = ['YouTube']

    for app in appNames:
        if os.path.exists(os.path.join(p.CSV_PARENT_PATH,app)):
            for filePath in os.listdir(os.path.join(p.CSV_PARENT_PATH,app)):
                if not filePath.startswith('.'):
                    absFilePath = os.path.join(p.CSV_PARENT_PATH,app,filePath)
                    
                    #totalIATFreq contains sorted IAT and no. of packets in that IAT
                    totalIATFreq, totalTime, dataPackets = getTotalIATFreq(absFilePath)

                    #cdfIATFreq is a list of tuples (ms_IAT, cdf_fraction)
                    #cdfIATFreq = getCDF(totalIATFreq)
                    
                    bursts, allBursts = divideIntoBursts(dataPackets, 50, 0.1, 150*3)
                    
                    print filePath
                    for i in bursts:
                        print i
                    
                    new_allBursts = change_allBursts(allBursts)
                    #this changes string to list of appropriate formats

                    #print len(bursts)
                    print "Dumping allBursts object for this app at " + os.path.join(p.BURSTS_PARENT_PATH, app, filePath.split('.')[0]+".burst")
                    pickle.dump(new_allBursts,open(os.path.join(p.BURSTS_PARENT_PATH, app, filePath.split('.')[0]+".burst"),"wb"))
                    print "Done!"
                
                    '''
                    if (createPlotFile(os.path.join(p.IAT_FREQ_DIST_PATH,filePath.split('.')[0]+"_total.plot"), totalIATFreq)):
                        print("Freq. distribution plot file for trace "+ str(filePath) +" successfully created.")

                    showPlotFile(os.path.join(p.IAT_FREQ_DIST_PATH,filePath.split('.')[0]+"_total.plot"), 'IAT in ms', 'total packets')

                    if (createPlotFile(os.path.join(p.IAT_FREQ_DIST_PATH,filePath.split('.')[0]+"_cdf.plot"), cdfIATFreq)):
                        print("CDF plot for trace " + str(filePath) + " successfully created.")

                    showPlotFile(os.path.join(p.IAT_FREQ_DIST_PATH,filePath.split('.')[0]+"_cdf.plot"), 'IAT in ms', 'cdf')
                    '''
    return

##################################################################

if __name__ == '__main__':
    main()
