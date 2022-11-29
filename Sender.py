'''
Python script to send files over the network to the specified IP address. Shows the progress of the transfer of files. 
Alive_progress package can be installed or the lines 8, 24 and 33 can be commented
Created by Ravi
Date - 10/11/2022
'''

import socket
import sys
import os
from alive_progress import alive_bar, alive_it
import shutil

os.system('cls')
def send_string(sock, string):
    sock.sendall(string.encode() + b'\n')


def send_int(sock, integer):
    sock.sendall(str(integer).encode() + b'\n')

#Sends the files from the specified folder(s) to the receiver
def transmit_files(sock, folder):
    print(f'Sending folder: {folder}')
    send_string(sock, folder)
    files = os.listdir(folder)
    send_int(sock, len(files))
    with alive_bar(len(files), title = f'Transferring files in {os.path.basename(folder)}  ', bar = None ,spinner = 'radioactive') as bar:
        for file in files:
            path = os.path.join(folder, file)
            filesize = os.path.getsize(path)
            #print(f'Sending file: {file} ({filesize} bytes)')
            send_string(sock, file)
            send_int(sock, filesize)
            with open(path, 'rb') as f:
                sock.sendall(f.read())
            bar()

s = socket.socket() #Open the socket for data transmission
s.connect(('130.246.70.168', 8000)) #Address of the receiver
with s:
    path =  "C:\\Users\\CLFAdmin\Desktop\\Picodata\\Na22" #Path with the data folder from picoscope. 
    folder = os.listdir(path)
    count = 0;
    for f in folder:
        print(len(folder)-count, "folders to be copied")
        transmit_files(s, os.path.join(path,f))
        print(f"\n Files transferred. Deleting {f} ...\n")
        shutil.rmtree(os.path.join(path,f)) #Removes the folder after copying. Can be commented to preserve the original folder. 
        os.system('cls')
        count = count+1
