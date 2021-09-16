# Blender Auto Render

# Imports
import logging
import configparser
import os
from tkinter import filedialog as fd
import tkinter as tk 
import subprocess

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
    print("Starting Render with these settings:")
    settingsReadAll()
    confirmCheck = input("Start Render? (y/N)")
    if confirmCheck.upper() == "Y":
        FINALRenderer = settingsRead("renderer")
        FINALOutputRootFolder = settingsRead("outputfolder")
        for specificfile in blenderfiles:
            idandfile = specificfile.split("|||")
            idandfile[0] + ". " + idandfile[1]
            blenderfilename = idandfile[1]
            framerange = settingsRead("frames" + idandfile[0])
            framelist = frameRange.split("-")
            frameStart = framelist[0]
            frameEnd = framelist[1]
            proc = subprocess.Popen([FINALRenderer,'-b',blenderfilename,'-s',frameStart,'-e',frameEnd, '-o', outputFolder.replace("/", "\\") + "\\render_#####", '-a'],stdout=subprocess.PIPE)
            imagesSaved = 0
            print("RENDERING FILE")
            for line in iter(proc.stdout.readline,''):
                #print(line.rstrip())
                callback = checkLine(line.rstrip())
                if callback == True:
                    imagesSaved += 1
                    progressPercent = int(imagesSaved)/int(end)
                    print("PE|" + str(progressPercent))
                    comms = "{}/{} images saved. ".format(imagesSaved, str(int(end)-(int(start)-1)))
                    print("SM|" + "Rendering: {}".format(comms))
                #print('Saved:' in line.rstrip())
                if line.rstrip() == b'Blender quit':
                    t1 = time.time()
                    totalrendertime = "Total Render Time: " + str(t1-t0)
                    print("SM|" + "Render Finished - " + display_time(t1-t0))
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
    SET-START [frame start]
    SET-END [frame end]
    OPTIONS (shows current configuration options)
    RENDER (renders file or files with current configuration)
    RM [0 (no display), 1 (very little display), 2 complete verbose mode]
    HELP (shows this help menu)
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
    elif "SET-OUTPUT" in command:
        try:
            outputfolder = command.split(" ")[1]
            isFile = os.path.isdir(outputfolder)
            if isFile == True:
                settingsWrite("outputfolder", command.split(" ")[1])
            else:
                print("Please select a valid output location.")
        except:
            print("Please enter a value.")
    elif "SET-FRAME" in command:
        try:
            # Data will be submitted like: SET-FRAMES 2 1-520 
            blenderfileidselect = command.split(" ")[1]
            if blenderfileidselect > len(blenderfiles) + 1:
                print("The blender file you are trying to set frames for does not exist.")
            else:
                frameRange = command.split(" ")[2]
                settingsWrite("frames" + str(blenderfileidselect), frameRange)
        except:
            print("Please enter a frame start and end in this format: SET-FRAMES (Blender File Number) STARTFRAME-ENDFRAME")
    #elif "SET-END" in command:
    #    try: 
    #        test = int(command.split(" ")[1])
    #        settingsWrite("endframe", command.split(" ")[1])
    #    except:
    #        print("Please enter a number for a frame end.")
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
        
