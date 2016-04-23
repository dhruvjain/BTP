import os
import fonte_nossdav_properties as p
from collections import defaultdict
import re
import pylab

y_axis = {}
x_axis = {}

y_axis["burstsize"] = "Kilobytes"
y_axis["burstduration"] = "Seconds"
y_axis["interburstarrivaltime"] = "Seconds"
y_axis["bufferstatus"] = "Kilobytes"

y_axis["avgpktsize"] = "Bytes"
y_axis["avgpktiat"] = "Micro Seconds"
y_axis["pktiatless"] = "Micro Seconds (<1000)"
y_axis["pktiatmore"] = "Micro Seconds (>1000)"

x_axis["burstsize"] = "Bursts"
x_axis["burstduration"] = "Bursts"
x_axis["interburstarrivaltime"] = "Bursts"
x_axis["bufferstatus"] = "Bursts"
x_axis["avgpktsize"] = "Bursts"
x_axis["avgpktiat"] = "Bursts"

x_axis["pktiatless"] = "Packets"
x_axis["pktiatmore"] = "Packets"



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
        #print param_list
        
        already_visted = {
        'desktop': False,
        'app': False,
        'mob': False
        }

        pylab.clf()

        gettitlestr = param_list[0].split('/')[-1].split('_')[-1]
        feature = param_list[0].split('/')[-1].split('.')[0].split('_')[-1].split('-')[1]
        graph_feature = param_list[0].split('/')[-1].split('.')[0].split('_')[-1].split('-')[0]

        datalist = [ ( pylab.loadtxt(filename)) for filename in param_list ]

        for i,data in enumerate(datalist):
            
            l = param_list[i].split('/')[-1].split('_')[:2]
            label_name = ''.join(l)

            if label_name.startswith('desktop'):
                color = 'r'
                platform = 'desktop'
            elif label_name.startswith('app'):
                color = 'g'
                platform = 'app'
            elif label_name.startswith('mob'):
                color = 'b'
                platform = 'mob'

            if(already_visted[platform]):
                pylab.plot( data[:,0], data[:,1], color)
            else:
                pylab.plot( data[:,0], data[:,1], color, label = platform)                    
                already_visted[platform] = True


        pylab.legend()
        pylab.title(gettitlestr)
        

        if graph_feature == "cdf":
            pylab.ylabel("Y Axis Label - cdf")
            if feature in y_axis:
                pylab.xlabel("X Axis Label - "+y_axis[feature])
            else:
                pylab.xlabel("X Axis Label");
        elif feature in y_axis:
            pylab.ylabel("Y Axis Label - "+y_axis[feature])
            pylab.xlabel("X Axis Label - "+x_axis[feature])
        else:
            pylab.ylabel("Y Axis Label");
            pylab.xlabel("X Axis Label");

        path = os.path.join(p.IMAGES_PATH, graph_feature)
        if not os.path.exists(path):
            os.makedirs(path)

        filepath = os.path.join(path, gettitlestr+".png")
        pylab.savefig(filepath)

if __name__ == "__main__":


    tracefiles =  getTraceFiles(p.BURSTS_PLOT_PATH)
    ref_list = tracefiles[tracefiles.keys()[0]]
    for parameter in range(len(ref_list)):
        param_list=[]
        for platform in tracefiles.keys(): 
            param_list.append(tracefiles[platform][parameter])
        plotgraph(param_list)



