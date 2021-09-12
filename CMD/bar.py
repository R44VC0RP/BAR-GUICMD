# Blender Auto Render

# Imports
import logging
import configparser
import os

configFileName = "bar.config"

configFile = configparser.ConfigParser()

barrun = True
# Config Files
logging.basicConfig(filename="bar.log", encoding='utf-8', level=logging.INFO, format='%(asctime)s |||| %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p')
logFunction = logging.getLogger("bar.log")

blenderfiles = []
# ===========================================================================================================================

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
    #print(settings[option])
    #return settings

def settingsReadAll():
    configFile = configparser.ConfigParser()
    configFile.read(configFileName)
    settings = configFile['ROOT']
    print("Renderer: {}\nStart Frame: {}\nEnd Frame: {}\nOutput Folder: {}".format(settings["renderer"], settings["startframe"], settings["endframe"], settings["outputfolder"]))
    print("Blender Files:")
    for blenderfileX in blenderfiles:
        print(blenderfileX)

def settingsWrite(option, value):
    configFile = configparser.ConfigParser()
    configFile.read(configFileName)
    log("Changing setting {} from {} to {}".format(option, configFile["ROOT"][option], value))
    configFile['ROOT'][option] = value
    updateConfig(configFile)


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
        'startframe': '0',
        'endframe': '250',
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
            renderer = command.split(" ")[1]
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
    elif "SET-START" in command:
        try: 
            test = int(command.split(" ")[1])
            settingsWrite("startframe", command.split(" ")[1])
        except:
            print("Please enter a number for a frame end.")
    elif "SET-END" in command:
        try: 
            test = int(command.split(" ")[1])
            settingsWrite("endframe", command.split(" ")[1])
        except:
            print("Please enter a number for a frame end.")
    elif "OPTIONS" in command:
        
        settingsReadAll()
    elif "RENDER" in command:
        blenderRenderQueue()
    elif command == "EXIT":
        barrun = False
    elif "ADD" in command:
        try:
            blenderfile = command.split("ADD ")[1].replace('"', '')
            isFile = os.path.isfile(blenderfile)
            if isFile == True:
                blenderfiles.append(blenderfile)
                log("Adding {} to blender list.".format(blenderfile))
                print(blenderfile)
            else:
                print("Please select a valid blender file.")
        except:
            print("Please enter a value.")
    else:
        print("Command not found.")
        
