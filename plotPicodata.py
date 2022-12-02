'''#=
Program to read the data from the picoscope, plots and saves the peaks as peaks.txt into individual folders
'''
import matplotlib.pyplot as plt
import numpy as np
#from scipy import preprocessing
from scipy.signal import find_peaks
import os
import glob
import shutil
from alive_progress import alive_bar, alive_it
#Input parameters
input_list = {"path" : "PicoData_pos1_01_12_2022_*", #=Directory with the data files from the picoscope=#, 
                "threshold" : 2} #=specify threshold in mV=#)  
                                                


#Select the folder with folder names of the format PicoData_pos1_

path = "C:\\Users\\ojo96212\\Desktop\\Ravi\\PicoData\\Na22\\Set_10ms"
os.chdir(path)

# Determine the time scale of the plot

def scaleFinder(maxT):
    if (maxT > 1):
        ts = "s";
        f = 1;    
    elif (maxT*1000>1) & (maxT*1000 < 1000):
        ts = "ms";
        f = 1000;

    elif (maxT*1e6>1) & (maxT*1e6 < 1000):
        ts = "us";
        f = 1e6;

    elif (maxT*1e9>1) & (maxT*1e9 < 1000):
        ts = "ns";
        f = 1e9;
    
    return ts, f


#Write files to a text file
def writeFiles(filename, data):
    with open(filename,"w") as file:
        np.savetxt(file,data)
    file.close()
    #close(filename

#Check if a directory exists
def checkdir(directory):
    try: 
        if os.path.exists(directory):
            os.chdir(directory)
    except:
        print(f"{directory} doesn't exist")
        os.mkdir(directory)
        os.chdir(directory)
    

#Creates a null array
folders = glob.glob1(path,input_list["path"]);
s = glob.glob1(folders[1],"PicoData_pos1_*.txt");
n = len(folders)
lenS = 0

#Reads folders and sub-folders and saves the figs and peaks data in 
for fold in folders:
    i=1;
    pks = [];
    files = glob.glob1(os.path.join(path,fold),"PicoData_pos1_*.txt");
    os.system("cls")
    os.chdir(path);
    os.chdir(fold);
    checkdir("Data_processed")
    #with alive_bar(len(s), title = f"Reading and Plotting files from {os.path.basename(fold)}", bar = None, spinner = 'radioactive') as bar:
    for s in alive_it(files):

            data = np.loadtxt(os.path.join(path,fold,s), delimiter = ',');
            volt = data[:,1];
            t = data[:,0];
            maxT = max(t);
            ts, fact  = scaleFinder(maxT)
            plt = plt.plot(t*int(fact), volt,  linewidth =3, color = 'blue')
            plt.xlabel(f"t ({ts})")
            plt.ylabel("counts")
            plt.xlim([0,100])
            pk = find_peaks(volt, height = 0, threshold = input_list["threshold"])#, prominence = 10)
            dictk = pk[2];
            pk_ht = dictk["peak_heights"];
            if pk_ht == []:
                pk_ht = max(volt)
            
            pks = np.append(pks,pk_ht);
            #savefig(plt, "Na22_50ms_{str(i)*".png");
            #bar()
        
    savefile = f"peaks_{str(input_list['threshold'])}mV.txt"
    if os.path.isfile(savefile):
        os.remove(savefile)
        writeFiles(savefile,pks)
    else: 
        writeFiles(savefile,pks)
    os.chdir('..')
        #hist = plt.hist(pks, bins = 200, xlabel = "Voltage(mV)");

