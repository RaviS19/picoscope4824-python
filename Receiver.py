while True:
    try:
        import os
        mod = 'socket'
        import socket
        mod = 'alive_progress'
        from alive_progress import alive_bar
        break
    except ImportError as e:
        print(f"\n {mod} not found. Installing {mod}")
        os.system(f"pip -m install {mod}")
        #subprocess.check_call([sys.executable, "-m", "pip", "install", mod])
        print(f"{mod} module installed")

s = socket.socket()
s.bind(('130.246.70.168', 8000)) #Specify the ip address of the receiver here
s.listen()

#Destination path for the incoming files.
destPath = 'C:\\Users\\ojo96212\\Desktop\\Ravi\\PicoData\\Na22\\Set_10ms'

if not os.path.exists(destPath):
    os.mkdir(destPath)
else:
    pass

print('Waiting for the client...')
while True:
    client, address = s.accept()
    print(f'{address} connected')
    os.system('cls')
    # client socket and makefile wrapper will be closed when 'with' exits.
    with client, client.makefile('rb') as clientfile:
        while True:
            folder = clientfile.readline()
            if not folder:  # When client closes connection folder == b''
                break
            folder = folder.strip().decode()
            folder = os.path.basename(folder)
            no_files = int(clientfile.readline())                       
            # put in different directory in case server/client on same system
            folderpath = os.path.join(destPath, folder)
            if os.path.exists(folderpath):
                print("Folder exists. Looking for unsaved files.")
                with alive_bar(no_files, title = f'Checking for new files in {folder}... ', bar = None ,spinner = 'triangles') as bar:
                    for i in range(no_files):
                        bar()
                        filename = clientfile.readline().strip().decode()
                        filesize = int(clientfile.readline())
                        data = clientfile.read(filesize)
                        if os.path.exists(os.path.join(folderpath, filename)):
                            continue
                        else:
                            print(f'Receiving file: {filename} ({filesize} bytes)')
                            with open(os.path.join(folderpath, filename), 'wb') as f:
                                f.write(data)          
            else:
                #print(f'Receiving folder: {folder} ({no_files} files)')
                os.makedirs(folderpath)
                with alive_bar(no_files, title = f'Receiving folder: {folder}...', bar = 'fish', spinner = 'fish2' ) as bar:
                    for i in range(no_files):
                        filename = clientfile.readline().strip().decode()
                        filesize = int(clientfile.readline())
                        data = clientfile.read(filesize)
                        if not os.path.exists(os.path.join(folderpath, filename)):
                            with open(os.path.join(folderpath, filename), 'wb') as f:
                                f.write(data)
                        bar()
    break
s.close()
input('Press enter to exit...')
