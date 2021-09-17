# Blender Auto Render

# Imports
import logging
import configparser
import os
from tkinter import filedialog as fd
import tkinter as tk 
import subprocess
import time
from pathlib import Path


root = tk.Tk() 
root.withdraw()
configFileName = "bar.config"

configFile = configparser.ConfigParser()

barrun = True
# Config Files
logging.basicConfig(filename="bar.log", encoding='utf-8', level=logging.INFO, format='%(asctime)s |||| %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p')
logFunction = logging.getLogger("bar.log")

blenderfiles = []
# ===========================================================================================================================

def select_file(filetype, filenameTitle):
    filetypes = (
        (filenameTitle, filetype),
        ('All files', '*.*')
    )
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    return filename

def log(message):
    logFunction.info(message)

def updateConfig(configSettings):
    configFile.read(configFileName)
    with open(configFileName, 'w') as configfile:
        configSettings.write(configfile)

def settingsRead(option):
    configFile = configparser.ConfigParser()
    configFile.read(configFileName)
    settings = configFile['ROOT']
    return settings[option]

def settingsReadAll():
    configFile = configparser.ConfigParser()
    configFile.read(configFileName)
    settings = configFile['ROOT']

    print("Renderer: {}\nOutput Folder: {}".format(settings["renderer"], settings["outputfolder"]))
    print("Blender Files:")
    for blenderfileX in blenderfiles:
        idandfile = blenderfileX.split("|||")
        print(idandfile[0] + ". " + idandfile[1])
        print("   -Frame Range: " + settings["frames" + idandfile[0]])

def settingsWrite(option, value):
    configFile = configparser.ConfigParser()
    configFile.read(configFileName)
    log("Changing setting {} from {} to {}".format(option, configFile["ROOT"][option], value))
    configFile['ROOT'][option] = value
    updateConfig(configFile)

def display_time(seconds, granularity=2):
    result = []
    intervals = (
        ('days', 86400),    # 60 * 60 * 24
        ('hours', 3600),    # 60 * 60
        ('minutes', 60),
        ('seconds', 1),
    )
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

def checkLine(temp):
    temp = temp.decode("utf-8")
    if "Saved: '" in temp:
        
        return True
    else:
        return False
def blenderRenderQueue():
    print("Checking Options")
    # PRE RENDER CHECKS
    if len(blenderfiles) < 1:
        print("You do not have a blender file added to render.")
        return
    for tryfile in blenderfiles:
        idandfile = tryfile.split("|||")
        idandfile[0] + ". " + idandfile[1]
        blenderfilename = idandfile[1]
        framerangecheck = settingsRead("frames" + idandfile[0])
        framerangeindividual = framerangecheck.split("-")
        startINT = framerangeindividual[0]
        endINT = framerangeindividual[1]
        if startINT > endINT:
            print("For file {} your frame start ({}) is greater than your frame end ({}).".format(idandfile[0], startINT, endINT))
            return
    
    print("Starting Render with these settings:")
    settingsReadAll()
    confirmCheck = input("Start Render? (y/N): ")
    if confirmCheck.upper() == "Y":
        FINALRenderer = settingsRead("renderer")
        FINALOutputRootFolder = settingsRead("outputfolder")
        for specificfile in blenderfiles:
            # Split the blender file path extention into just the name of the project
            blenderfilenameraw = specificfile.split("/")
            outputfolder = FINALOutputRootFolder + "/" + blenderfilenameraw[-1] + "/"
            # Splitting the blenderID and blender project path
            idandfile = specificfile.split("|||")
            idandfile[0] + ". " + idandfile[1]
            blenderfilename = idandfile[1]
            framerange = settingsRead("frames" + idandfile[0])
            framelist = framerange.split("-")
            frameStart = framelist[0]
            frameEnd = framelist[1]
            t0 = time.time()
            print("Starting render for "+blenderfilenameraw[-1]+"")
            #print([FINALRenderer,'-b',blenderfilename,'-s',frameStart,'-e',frameEnd, '-o', outputfolder + "\\render_#####", '-a'])
            proc = subprocess.Popen([FINALRenderer,'-b',blenderfilename,'-s',frameStart,'-e',frameEnd, '-o', outputfolder + "\\render_#####", '-a'],stdout=subprocess.PIPE)
            imagesSaved = 0
            for line in iter(proc.stdout.readline,''):
                callback = checkLine(line.rstrip())
                if callback == True:
                    imagesSaved += 1
                    progressPercent = int(imagesSaved)/int(frameEnd)
                    comms = "{}/{} images saved. ".format(imagesSaved, str(int(frameEnd)-(int(frameStart)-1)))
                    print("Rendering "+blenderfilenameraw[-1]+": {}".format(comms))
                #print('Saved:' in line.rstrip())
                if line.rstrip() == b'Blender quit':
                    t1 = time.time()
                    totalrendertime = "Total Render Time: " + str(t1-t0)
                    print("Render Finished for "+blenderfilenameraw[-1]+" - " + display_time(t1-t0))
        return

         


# ===========================================================================================================================
# COMMANDS
def help():
    print("""
========================================================================
    Commands:
    ADD [blender file location]
    SET-RENDERER [renderer location]
    SET-OUTPUT [output location]
    SET-FRAMES (Blender File Number) STARTFRAME-ENDFRAME
    OPTIONS (shows current configuration options)
    RENDER (renders file or files with current configuration)
    HELP (shows this help menu)
    GIF (seprate process to )
========================================================================
    """)


# ===========================================================================================================================

# Startup Sequence
try:
    testFile = open(configFileName, "r+")
except:        
    configFile['ROOT'] = {
        'renderer': "G:/main_gaming/steamapps/common/Blender/blender.exe",
        'frames1': '1-250',
        'frames2': '1-250',
        'frames3': '1-250',
        'frames4': '1-250',
        'frames5': '1-250',
        'outputfolder': 'A:/RENDER OUTPUT'
    }
    updateConfig(configFile)


print("""                                                                      
BBBBBBBBBBBBBBBBB               AAA               RRRRRRRRRRRRRRRRR   
B::::::::::::::::B             A:::A              R::::::::::::::::R  
B::::::BBBBBB:::::B           A:::::A             R::::::RRRRRR:::::R 
BB:::::B     B:::::B         A:::::::A            RR:::::R     R:::::R
  B::::B     B:::::B        A:::::::::A             R::::R     R:::::R
  B::::B     B:::::B       A:::::A:::::A            R::::R     R:::::R
  B::::BBBBBB:::::B       A:::::A A:::::A           R::::RRRRRR:::::R 
  B:::::::::::::BB       A:::::A   A:::::A          R:::::::::::::RR  
  B::::BBBBBB:::::B     A:::::A     A:::::A         R::::RRRRRR:::::R 
  B::::B     B:::::B   A:::::AAAAAAAAA:::::A        R::::R     R:::::R
  B::::B     B:::::B  A:::::::::::::::::::::A       R::::R     R:::::R
  B::::B     B:::::B A:::::AAAAAAAAAAAAA:::::A      R::::R     R:::::R
BB:::::BBBBBB::::::BA:::::A             A:::::A   RR:::::R     R:::::R
B:::::::::::::::::BA:::::A               A:::::A  R::::::R     R:::::R
B::::::::::::::::BA:::::A                 A:::::A R::::::R     R:::::R
BBBBBBBBBBBBBBBBBAAAAAAA                   AAAAAAARRRRRRRR     RRRRRRR

""")
print("===============================================================")
help()
log("-------------------------PROGRAM RESTARTED-------------------------")
print("===============================================================")
print("BAR is able to Queue up to 5 blender files at once.")
print("\nEnter Command:")
while barrun == True:
    command = input(">>> ").upper()
    if command == "HELP":
        help()
    elif "SET-RENDERER" in command:
        try:
            # Uncomment this line if you want to manually input the file location
            #renderer = command.split(" ")[1]
            renderer = select_file(".exe", "Renderer")
            isFile = os.path.isfile(renderer)
            if isFile == True:
                settingsWrite("renderer", command.split(" ")[1])
            else:
                print("Please select a valid blender program.")
        except:
            print("Please enter a value.")
    elif command == "SET-OUTPUT":

        folder_selected = fd.askdirectory(initialdir="/", title="Select Base Output Folder")
        if folder_selected != "":
            settingsWrite("outputfolder", folder_selected)
            print("Output Folder " + folder_selected)
        else:
            print("No Output Folder Selected")
    elif "SET-FRAMES" in command:
        try:
            # Data will be submitted like: SET-FRAMES 2 1-520 
            blenderfileidselect = command.split(" ")[1]
            if int(blenderfileidselect) >= len(blenderfiles) + 1:
                print("The blender file you are trying to set frames for does not exist.")
            else:
                frameRange = command.split(" ")[2]
                settingsWrite("frames" + str(blenderfileidselect), frameRange)
        except:
            print("Please enter a frame start and end in this format: SET-FRAMES (Blender File Number) STARTFRAME-ENDFRAME")
    elif "OPTIONS" in command:
        settingsReadAll()
    elif "RENDER" in command:
        blenderRenderQueue()
    elif command == "EXIT":
        barrun = False
    elif "ADD" in command:
        if len(blenderfiles) <= 5:    
            try:
                # Uncomment this line if you want to manually input the file location
                #blenderfile = command.split("ADD ")[1].replace('"', '')
                blenderfile = select_file(".blend", "Blender File")
                isFile = os.path.isfile(blenderfile)
                if isFile == True:
                    blenderfileID = len(blenderfiles) + 1
                    blenderfiles.append(str(blenderfileID) + "|||" + blenderfile)
                    log("Adding {} to blender list.".format(blenderfile))
                    print("Adding {} to blender list.".format(blenderfile))
                else:
                    print("Please select a valid blender file.")
            except:
                print("Please enter a value.")
        else:
            print("You can only have 5 blender files in the queue at one time.")
    else:
        print("Command not found.")
        
