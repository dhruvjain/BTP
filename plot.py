import os
import fonte_nossdav_properties as p
from collections import defaultdict
import re
import pylab
def getTraceFiles (tracePath):
    # Get a list of all capture files
    traceFilePaths = defaultdict(list)
    
    for d in os.listdir(tracePath):
        folderlist = []
        if os.path.isdir(os.path.join(tracePath,d)):
            for f in os.listdir(os.path.join(tracePath,d)):
                if not f.startswith('.') and os.path.isfile(os.path.join(tracePath,d,f)):
                    folderlist.append(os.path.join(tracePath,d,f))

            folderlist.sort()
            traceFilePaths[d]=folderlist
 

    return traceFilePaths
    

def plotgraph(param_list):

        pylab.clf()
        l =  param_list[0].split('/')[-1].split('_')[2:]
        gettitlestr = ''.join(l)

        datalist = [ ( pylab.loadtxt(filename)) for filename in param_list ]
        #labels = ['mobile','desktop','app']
        for i,data in enumerate(datalist):
            l = param_list[i].split('/')[-1].split('_')[:2]   
            label_name = ''.join(l)
            pylab.plot( data[:,0], data[:,1], label = label_name)

        pylab.legend()
        pylab.title(gettitlestr)
        pylab.xlabel("X Axis Label")
        pylab.ylabel("Y Axis Label")
        pylab.savefig("/home/dhruv/Desktop/BTP/images/"+gettitlestr+".png")

if __name__ == "__main__":
    tracefiles =  getTraceFiles(p.BURSTS_PLOT_PATH)
    ref_list = tracefiles[tracefiles.keys()[0]]
    for parameter in range(len(ref_list)):
        param_list=[]
        for platform in tracefiles.keys(): 
            param_list.append(tracefiles[platform][parameter])
        plotgraph(param_list)


