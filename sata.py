import os
import shutil

#########################################################################

def clearAll (path):
    
    status = True
    
    listFiles = [os.path.join(path,f) for f in os.listdir(path) if os.path.isfile(f)]
    listDirs = [os.path.join(path,d) for d in os.listdir(path) if os.path.isdir(d)]

    for each_file in listFiles:
        os.remove(each_file)

    try:
        for each_dir in listDirs:
            shutil.rmtree(os.path.join(path,each_dir))
    except:
        status = False

    return status

#########################################################################

def main():
    return

#########################################################################

if __name__ == "__main__":
    main()
