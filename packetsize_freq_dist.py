import numpy as np
import os
#import datactrl_static_train as dcst
from collections import defaultdict
import operator
import fonte_nossdav_properties as p

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

#################################################################

def getTotalPSFreq(absFilePath):

    totalPSFreq = defaultdict(int)
    totalTime = 0.0
    
    #appPath = os.path.join(p.CSV_PARENT_PATH,app)
    #traceFiles = [os.path.join(appPath,f) for f in os.listdir(appPath) if os.path.isfile(os.path.join(appPath,f))]
    #listStaticScenarioPath = dcst.getStaticScenarioList(traceFiles)
    
    #for dataPath in listStaticScenarioPath:
    #print absFilePath
    readfp = open(absFilePath,'r')
    lines = readfp.readlines()
    startTime = float(lines[0].split(',')[1])
    endTime = float(lines[len(lines)-1].split(',')[1])
    countData = 0
    countTotal = 0
    for line in lines:
        countTotal += 1
        if (isDataPacket(line)):
            tokens = line.split(',')
            packetSize = int(tokens[3])
            totalPSFreq[packetSize] += 1
            countData += 1
    readfp.close()
    totalTime += (endTime - startTime)
	
    print("Stats for file: " + str(absFilePath.split('/')[-1]) + ": ")
    print("Data Packets / Total Packets = "+str(countData)+" / "+str(countTotal)+"; Percentage = "+str(countData*100/countTotal))

    sortedPSFreq = sorted(totalPSFreq.items(), key=operator.itemgetter(0,1))
            
    return sortedPSFreq, totalTime
    
#################################################################

def getFinalPSFreq(totalPSFreq,totalTime,granularity):
    granularPSFreq = []
    for tuple in totalPSFreq:
        if int(np.ceil((tuple[1]/totalTime)*granularity)) > 1:
            granularPSFreq.append((tuple[0], int(np.ceil((tuple[1]/totalTime)*granularity))))
    return granularPSFreq

#################################################################

def getCDF(totalPSFreq):
    cdfPSFreq = []
    totalFreq = 0
    for dataPoint in totalPSFreq:
        totalFreq += dataPoint[1]
    cumulativeFreq = 0
    cdf = 0.123456789
    for dataPoint in totalPSFreq:
        cumulativeFreq += dataPoint[1]
        cdf = (cumulativeFreq*1.0)/(totalFreq*1.0)
        #print cumulativeFreq
        cdfPSFreq.append((dataPoint[0],cdf))
    return cdfPSFreq

#################################################################

def createPlotFile(plotPath,finalPSFreq):
    c = 0
    writefp = open(plotPath,'w')
    for tuple in finalPSFreq:
        writefp.write(str(c)+" "+str(tuple[0])+" "+str(tuple[1])+"\n")
        c += 1
    writefp.close()
    return True

#################################################################

def main():
    #appNames = ['YouTube','TED','HotStar','YouTubeLive','StarSports','TimesNow','Skype','GoogleHangouts','ooVoo']
    appNames = ['YouTube']
    for app in appNames:
        if os.path.exists(os.path.join(p.CSV_PARENT_PATH,app)):
            for filePath in os.listdir(os.path.join(p.CSV_PARENT_PATH,app)):
                absFilePath = os.path.join(p.CSV_PARENT_PATH,app,filePath)
                totalPSFreq, totalTime = getTotalPSFreq(absFilePath)
                cdfPSFreq = getCDF(totalPSFreq)
                #print(totalPSFreq)
                #print(totalTime)
                #finalPSFreq = getFinalPSFreq(totalPSFreq,totalTime,granularity=180)
                if (createPlotFile(os.path.join(p.PS_FREQ_DIST_PATH,filePath.split('.')[0]+"_total.plot"), totalPSFreq)):
                    print("Freq. distribution plot file for trace "+ str(filePath) +" successfully created.")
                if (createPlotFile(os.path.join(p.PS_FREQ_DIST_PATH,filePath.split('.')[0]+"_cdf.plot"), cdfPSFreq)):
                    print("CDF plot for trace " + str(filePath) + " successfully created.")
                
    return

################################################################

if __name__ == "__main__":
    main()
