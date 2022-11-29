'''
This code acquires data from the picoscope using rapid block mode and saves it into a text file. Should work for any picoscope model in principle. 
Make sure that the picoSDK is installed. 
Created by Ravi
Created on 25/10/2022
Modified on 29/11/2022
'''

import ctypes
from tabnanny import filename_only
import numpy as np
from picosdk.ps4000a import ps4000a as ps
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok
from math import ceil
from datetime import datetime
import pandas as pd
import time as tm
import os
from alive_progress import alive_bar, alive_it

os.system('cls')

#Enter the input variables for the picoscope. All the variables can be edited here. No edits needed in the program to use as is.

input_list = {'channels' :['A'],        # Channels to be turned on.
              'channelRange': 3,        # picoreadable_Values:volts {0:0.01, 1:0.02, 2:0.05, 3:0.1, 4:0.2, 5:0.5, 6:1, 7:2, 8:5, 9:10, 10:20, 11:50, 12:100, 13:200}
                                            #Enter picoscope readable values. 
              'triggerChan': 'A',       # Trigger channel
              'trigV': 0.002,           # Trigger voltage. Enter in volts.
              'timeI': 500,             # Time Interval in ns
              'preTT': 100e-6,          # Pre-trigger acquisition time. Enter in seconds
              'postTT': 10e-3,           # Post-trigger acquisition time. Enter in seconds.
              'nWaveform': 10000 }       # Number of waveforms to capture.
 
maxVolt = {0:0.01, 1:0.02, 2:0.05, 3:0.1, 4:0.2, 5:0.5, 6:1, 7:2, 8:5, 9:10, 10:20, 11:50, 12:100, 13:200} #Channel values in volts corresponding to picoscope readable number.
chanNo = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7} #Channel values

# Create channel handle and status ready for use
chandle = ctypes.c_int16()
status = {}

status["openunit"] = ps.ps4000aOpenUnit(ctypes.byref(chandle), None)

#Open the picoscope
def picoOpen():
    try:
        assert_pico_ok(status["openunit"])
    except:
        powerStatus = status["openunit"]

        if powerStatus == 286:
            status["changePowerSource"] = ps.ps4000aChangePowerSource(chandle, powerStatus)
        elif powerStatus == 282:
            status["changePowerSource"] = ps.ps4000aChangePowerSource(chandle, powerStatus)
        else: 
            raise

        assert_pico_ok(status["changePowerSource"])

picoOpen()

# Set the channels to be active during the acquisition
#ps.ps4000aSetChannel(handle, 
#                    channel number = 0-7(A-H), 
#                    enable = (0,1), 
#                    coupling type = (0,1) (AC/DC), 
#                    range = 0-11 (10mV - 50V)
#                    analog offset (V))



#Channel range for all the channels. Change the range here. 
channelRange = {'chARange' : input_list['channelRange'],
                'chBRange' : input_list['channelRange'],
                'chCRange' : input_list['channelRange'],
                'chDRange' : input_list['channelRange'],
                'chERange' : input_list['channelRange'],
                'chFRange' : input_list['channelRange'],
                'chGRange' : input_list['channelRange'],
                'chHRange' : input_list['channelRange']}
                
#Start with all channels off
#Channel A
status["setChA"] = ps.ps4000aSetChannel(chandle, 0, 0, 1, channelRange['chARange'], 0)
assert_pico_ok(status["setChA"])
#Channel B
status["setChB"] = ps.ps4000aSetChannel(chandle, 0, 0, 1, channelRange['chBRange'], 0)
assert_pico_ok(status["setChB"])
#Channel C
status["setChC"] = ps.ps4000aSetChannel(chandle, 0, 0, 1, channelRange['chCRange'], 0)
assert_pico_ok(status["setChC"])
#Channel D
status["setChD"] = ps.ps4000aSetChannel(chandle, 0, 0, 1, channelRange['chDRange'], 0)
assert_pico_ok(status["setChD"])
#Channel E
status["setChE"] = ps.ps4000aSetChannel(chandle, 0, 0, 1, channelRange['chERange'], 0)
assert_pico_ok(status["setChE"])
#Channel F
status["setChF"] = ps.ps4000aSetChannel(chandle, 0, 0, 1, channelRange['chFRange'], 0)
assert_pico_ok(status["setChF"])
#Channel G
status["setChG"] = ps.ps4000aSetChannel(chandle, 0, 0, 1, channelRange['chGRange'], 0)
assert_pico_ok(status["setChG"])
#Channel H
status["setChH"] = ps.ps4000aSetChannel(chandle, 0, 0, 1, channelRange['chHRange'], 0)
assert_pico_ok(status["setChH"])

#Channels to be turned on. No input needed here. 
onChannel = {'A': "setChA",
             'B': "setChB", 
             'C': "setChC",
             'D': "setChD",
             'E': "setChE", 
             'F': "setChF", 
             'G': "setChG", 
             'H': "setChH"}



print('Channels to turn on (A-H)')
channels = input_list['channels']

for c in channels:    
    status[onChannel[c]]  = ps.ps4000aSetChannel(chandle, 
                                                 chanNo[c],
                                                 1,
                                                 1,
                                                 channelRange['chARange'], 0)
    assert_pico_ok(status["setChA"])
    
print('Number of on-channels: ', len(channels))



#Trigger channel
#ps.ps4000aSetSimpleTrigger(handle, 
#                           enable = 0-1,
#                           channel = 0-7,
#                           threshold in ADC counts,
#                           threshold direction = 2 (for rising. Ref ps4000a script for different types of trigger), 
#                           delay (s), autotrigger time (set 0 to trigger on signal))
while True:
        trigChan = input_list['triggerChan']
        if trigChan in channels:
            print('\nTrigger set to ', trigChan)
            trigChanNo = chanNo[trigChan]
            break
        else:
            print('\nEnter the correct trigger')
            
    
maxVoltage = maxVolt[channelRange['ch'+trigChan+'Range']]
print('\nMaximum voltage for this channel is', maxVoltage, )

#Trigger voltage setup. Enter the trigger voltage.
while True:
    trigVolt = input_list['trigV']
    if float(trigVolt) < 0:
        print('\nEnter a positive value')
        continue
    elif float(trigVolt) > float(maxVoltage):
        print('\nEnter a value less than', maxVoltage, 'V')
        continue
    else:
        print('\nTrigger Voltage will be set to ', trigVolt, 'V')
        break
            
trigADC = ceil(float(trigVolt)/maxVoltage*(2**15-1))

    
status["trigger"] = ps.ps4000aSetSimpleTrigger(chandle, 1, trigChanNo, trigADC, 2, 0, 0)

s = input_list['timeI']
s = float(s)
if s < 25:
    print('\nMinimum resolution is 25 ns, time interval set to 25 ns')
    timebase = 1
else:
    timebase = round(s/12.5-1)
    timeInt = 12.5*(timebase+1)*1e-9
    print('\nSelected time resolution is ', round(timeInt*1e9), 'ns')
    

timeInt = 12.5*(timebase+1)*1e-9            # Time interval calculated frim time base
timeAcqPreTrig = input_list['preTT']        # Pre-trigger acquisition time
timeAcqPostTrig = input_list['postTT']      # Post-trigger acquistion 
    
#print('Time interval selected: ', ceil(timeInt*1e9), 'ns')
#Number of pre and post trigger samples to be collected
preTrigSamples = ceil(float(timeAcqPreTrig)/timeInt)
postTrigSamples = ceil(float(timeAcqPostTrig)/timeInt)
print('Samples: ', preTrigSamples, postTrigSamples)
maxSamples = preTrigSamples + postTrigSamples
#print(timebase)
while True:
                totalDataForm = input_list['nWaveform']
                try:
                    totalDataForm = int(totalDataForm)
                    if isinstance(int(totalDataForm), int) == True:
                        print(totalDataForm, 'waveforms will be captured and saved')
                        break
                    else:
                        continue
                except ValueError:
                    print('Enter an integer')


count = 1;
t1 = 0;
t2=0;

# Begin the acquisition
while True:
    try:
        divider = 0; 
        divider = input('Enter the number of samples per set to save: ') #Number of samples to save per acquisition
        print(divider)
        divider = int(divider)
        loop = ceil(totalDataForm/divider)
        os.system('cls')
        print("\n\n\n")
        
        #Acquisition loop
        with alive_bar(loop, title = f'Acquiring data...', bar=None, spinner = 'elements') as bar:
            for i in range(loop):
                os.system('cls')
                acquired = divider * i #Number of acquired waveforms
                rem = totalDataForm%divider
                remains = totalDataForm-acquired-rem
                if remains > 0:
                    cap = divider   
                elif remains <= 0:
                    cap = rem
        
                timeIntervalns = ctypes.c_float()
                returnedMaxSamples = ctypes.c_int32()
                oversample = ctypes.c_int16(1)

                # Time base setting
                #ps.ps4000aGetTimebase2(handle = chandle,
                #                       timebase = 8 (gives the sampling interval = (timebase-2)/62500000),
                #                       noSamples = maxSamples,
                #                       pointer to timeIntervalNanoseconds = ctypes.byref(timeIntervalns),
                #                       pointer to maxSamples = ctypes.byref(returnedMaxSamples),
                #                       segment index = 0
                #print(timebase, maxSamples, timeIntervalns.value, returnedMaxSamples.value, chandle)
                status["getTimebase2"] = ps.ps4000aGetTimebase2(chandle,
                                                                timebase,
                                                                maxSamples,
                                                                ctypes.byref(timeIntervalns),
                                                                ctypes.byref(returnedMaxSamples), 0)
                assert_pico_ok(status["getTimebase2"]);

                    
                #Number of waveforms to be save in rapid block mode. 
                # Set number of captures
                # handle = chandle
                # nCaptures = enter a value
                #print('\nSetting captures...')
                status["SetNoOfCaptures"] = ps.ps4000aSetNoOfCaptures(chandle, int(cap))
                assert_pico_ok(status["SetNoOfCaptures"]);
                    
                # Allocate memory segments
                # handle = chandle
                # nSegments = 10
                nMaxSamples = ctypes.c_int32(0)
                status["setMemorySegments"] = ps.ps4000aMemorySegments(chandle,
                                                                        cap,
                                                                        ctypes.byref(nMaxSamples))
                assert_pico_ok(status["setMemorySegments"]);
                val = ctypes.c_int16(maxSamples)
            
                status["getMaximumValue"]  = ps.ps4000aMaximumValue(chandle,ctypes.byref(val))
                
                
                #Buffer values for A    
                buffer = {'A' : {}, 
                        'B' : {},
                        'C' : {},
                        'D' : {},
                        'E' : {},
                        'F' : {},
                        'G' : {},
                        'H' : {}}

                '''
                Assign number of buffers for the channels based on user input
                Takes the user input
                '''
                for c in channels:
                    newDict = {}
                    for i in range(cap):
                        dictEle = 'buffer'+c+str(i)
                        newDict[dictEle] = (ctypes.c_int16 * maxSamples)()
                    buffer[c] = newDict

                # set data buffers
                # ps4000aSetDataBuffer(handle = chandle,
                #                      channel = PS4000A_CHANNEL_A = 0
                #                      buffer = bufferAX (where X = segmentIndex)
                #                      bufferLength = maxSamples
                #                      segmentIndex = X
                #                      mode = PS4000A_RATIO_MODE_NONE = 0)
                    fooBuffer = buffer[c] #creates a temporary buffer to store the data for channel X
                    for i in range(cap):
                        dataBuffer = "setDataBuffers"+c+str(i)
                        buffSet = 'buffer'+c+str(i)
                        status[dataBuffer] = ps.ps4000aSetDataBuffer(chandle,
                                                                    0,
                                                                    ctypes.byref(fooBuffer[buffSet]),
                                                                    maxSamples,
                                                                    i,
                                                                    0)

                # Run in rapid block mode
                # ps.ps4000aRunBlock(handle = chandle
                #                   number of pre-trigger samples = preTriggerSamples
                #                   number of post-trigger samples = PostTriggerSamples
                #                   timebase 
                #                   time indisposed ms = None (not needed in the example)
                #                   segment index = 0
                #                   lpReady = None (using ps4000aIsReady rather than ps4000aBlockReady)
                #                   pParameter = None

                #print('\nRunning scope for capture...')
                #print(f'''                 -----------------------------------------------------------------------------------------------------------------------------------------------------
                #                                                    
                #                                                                Acquiring dataset {str(count)}
                #                                                    
                #    -----------------------------------------------------------------------------------------------------------------------------------------------------''')
                status["runBlock"] = ps.ps4000aRunBlock(chandle,
                                                        preTrigSamples,
                                                        postTrigSamples,
                                                        timebase, 
                                                        None,
                                                        0,
                                                        None,
                                                        None)
                assert_pico_ok(status["runBlock"])
                
                


                # create overflow location
                overflow = (ctypes.c_int16 * cap)()
                # create converted type maxSamples
                cmaxSamples = ctypes.c_int32(maxSamples)

                # Check for data collection to finish using ps4000aIsReady
                ready = ctypes.c_int16(0)
                check = ctypes.c_int16(0)
                while ready.value == check.value:
                    status["isReady"] = ps.ps4000aIsReady(chandle, ctypes.byref(ready))
                #print('Is ready status:',status["isReady"])    
                # Retried data from scope to buffers assigned above
                # ps.ps4000aGetValuesBulk(handle = chandle, 
                #                         noOfSamples = cmaxSamples
                #                         fromSegmentIndex = 0
                #                         toSegmentIndex = 9
                #                         downSampleRatio = 1
                #                         downSampleRatioMode = PS4000A_RATIO_MODE_NONE
                #                         pointer to overflow = ctypes.byref(overflow)

                # ps.ps4000aGetValuesOverlappedBulk(handle = chandle, 
                #                         startIndex = 0
                #                         noOfSamples = cmaxSamples
                #                         downSampleRatio = 1
                #                         downSampleRatioMode = PS4000A_RATIO_MODE_NONE
                #                         fromSegmentIndex = 0
                #                         toSegmentIndex = 9
                #                         pointer to overflow = ctypes.byref(overflow)
                
                
                status["getValuesBulk"] = ps.ps4000aGetValuesBulk(chandle,
                                                                ctypes.byref(cmaxSamples),
                                                                0,
                                                                cap-1,
                                                                1,
                                                                0,
                                                                ctypes.byref(overflow))
                assert_pico_ok(status["getValuesBulk"])

                # find maximum ADC count value
                # handle = chandle
                # pointer to value = ctypes.byref(maxADC)
                maxADC = ctypes.c_int16(32767)


                # Create time data
                time = np.linspace(0, (cmaxSamples.value - 1) * timeIntervalns.value, cmaxSamples.value)
                #indices = np.where(time > float(timeAcqPostTrig) * 1e9)
                #time = np.delete(time,indices)

                #Create a null storage for the values
                adc2mVCh = {'A':{}, 
                    'B':{}, 
                    'C':{}, 
                    'D':{}, 
                    'E':{}, 
                    'F':{}, 
                    'G':{}, 
                    'H':{}}
                timesec = time*1e-9 
                foldname =  "PicoData_pos1_"+datetime.now().strftime("%d_%m_%Y_%H%M%S")+"_30VBias_"+str(i+1)
                os.mkdir('C:/Users/CLFAdmin/Desktop/Picodata/Na22/'+foldname)
                os.chdir('C:/Users/CLFAdmin/Desktop/Picodata/Na22/'+foldname)
                tAcq = round(tm.process_time()-t1,3);
                t2 =  round(tm.process_time(),3);
                print('Data Acquired in ',tAcq,'s. Saving data...\n')
                
                #Loop the contents and save the files
                #with alive_bar(cap, title = 'Saving data...', bar=None, spinner = 'elements') as bar:
                for x in range(cap):
                # os.system('cls')
                    for c in channels:
                        k = adc2mVCh[c]
                        j = buffer[c]
                        chRange = f'ch{c}Range'
                        buffMax = f'buffer{c}{str(x)}'
                        k = adc2mV(j[buffMax], channelRange[chRange], maxADC)

                    data = [timesec, k]
                    data = np.transpose(data)

                    filename =  foldname+"_"+str(x+1)+".txt"
                    np.savetxt(filename, data, fmt="%2.10f", delimiter=", ")

                    tSave = round(tm.process_time()-t2,3);
                    t1 = round(tm.process_time(),3);
                print('\n Your dataset of', i+1,' signals was saved in',tSave, 's')
                count = count+1
                bar()
                
                #Save input list
                with open("input_data.txt",'w') as f:
                    f.write(str(input_list))
                f.close()
            
        print('\nTotal time in ',round(tm.process_time(),3), 's')
        break
    
    except:
        print('Enter a smaller divider\n')
        contStr = input('Continue? [y/n]: ')
        if contStr == 'y':
            continue
        elif contStr == 'n':
            break
        else:
            print('Enter y or n')
            
    
#Close the scope
status["close"] = ps.ps4000aCloseUnit(chandle)
assert_pico_ok(status["close"])



input('\nPress enter to quit... ')

