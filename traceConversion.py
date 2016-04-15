import os
import subprocess
import fonte_nossdav_properties as p

################################################################################

def getTraceFiles (tracePath):
    # Get a list of all capture files
    traceFilePaths = []
    for d in os.listdir(tracePath):
	if os.path.isdir(os.path.join(tracePath,d)):
		for f in os.listdir(os.path.join(tracePath,d)):
			if not f.startswith('.') and os.path.isfile(os.path.join(tracePath,d,f)):
				traceFilePaths.append(os.path.join(tracePath,d,f))
    return traceFilePaths

################################################################################

def convertPCAPtoCSV (traceFilePaths):
    # Convert ARO capture (CAP) files to CSV files
    CSVParentPath = p.CSV_PARENT_PATH
    successStatus = True
    for traceFile in traceFilePaths:
        tsharkCommand = ["tshark", "-r", traceFile, "-T", "fields", "-e",
                         "frame.number", "-e", "frame.time_relative", "-e",
                         "frame.protocols", "-e", "frame.len", "-e", "ip.src",
                         "-e", "ip.dst", "-E", "separator=,"]
        appName = traceFile.split('/')[-2]
        CSVDir = os.path.join(CSVParentPath,appName)
        if not os.path.exists(CSVDir):
            os.makedirs(CSVDir)
        CSVFile = os.path.join(CSVDir, traceFile.split('/')[-1].split('.')[0]+".csv")
        print("Converting file: "+str(CSVFile))
        filePointer = open(CSVFile,"w")
        # Executing tshark cap-to-csv command with desired parameters
        # Storing output in desired csv files in the "Intermediate" directory
        exitStatus = subprocess.call(tsharkCommand, stdout=filePointer)
        filePointer.close()
        # exit status 0 indicates success
        if (exitStatus!=0):
            successStatus = False
            break
        else:
            print("Converted.")
    return successStatus
        
################################################################################
        
def main():
    # Get path to the input trace repository
    tracePath = p.PCAP_PARENT_PATH
    #print "tracePath: "+tracePath
    traceFilePaths = getTraceFiles(tracePath)
    print "traceFilePaths: ", traceFilePaths
    successStatus = convertPCAPtoCSV(traceFilePaths)
    if (successStatus):
        print("Conversion completed successfully.")
    else:
        print("Error encountered.")
    
################################################################################

if __name__ == '__main__':
    main()

################################################################################
