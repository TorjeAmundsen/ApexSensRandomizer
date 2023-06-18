import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import *
import re
import json
import random
import keyboard
import os
import icon
import base64
import time
import threading
import webbrowser
import datetime
import winreg
import vdf


def select_folder():
    gameDirPath = filedialog.askdirectory()
    directory.set(gameDirPath)


def validate_number_input(text):
    return re.match(r'^\d*\.?\d{0,2}$', text) is not None or text == ""


def validate_purenumber_input(text):
    return text.isdigit() or text == ""


# Toggle function - flips the "running" switch on/off
def toggle():
    global running
    running = not running
    sensStateToggle = ["Not running", "Press " + updateBindModifiers() + "!"]
    # List of widgets that will be disabled when the randomizer is running
    disabledElementsWhileRunning = [gameDir, selectFolder, dpiEntry, minSensEntry,
                                    maxSensEntry, autoexecButton, baseSensEntry,
                                    randomizeBindButton, enableBindButton, disableBindButton,
                                    useTimerBox, timerIntervalEntry,
                                    modifierBoxAlt, modifierBoxCtrl, modifierBoxShift]
    
    for element in disabledElementsWhileRunning: # Disables/enables the widgets
        element.configure(state=stateToggle[running])
    runButton.configure(text=btnText[running], bg=btnColor[running], activebackground=btnActive[0])
    if randomizeBind.get() == "Invalid":
        outputSensLabel.configure(text="Invalid binds!")
    elif randomizeBind.get() == "Bind":
        outputSensLabel.configure(text="Key not bound!")
    else:
        outputSensLabel.configure(text=sensStateToggle[running])
    print(btnText[running])


# Main randomization function that is called by your randomize hotkey and/or the timer
def randomize():
    minFloat = float(minSensEntry.get())
    maxFloat = float(maxSensEntry.get())
    initRNG = random.uniform(minFloat, maxFloat)
    actualSensNum = round(initRNG, 2)
    floatSens = float(actualSensNum)

    cmRev = str(round((360 / (0.022 * int(dpi.get()) * floatSens)) * 2.54, 1))

    formattedSens = cmRev + "cm/360 (" + f"{floatSens:.2f}" + " @ " + str(dpi.get()) + " DPI)"

    now = datetime.datetime.now()
    sensLog = open(sensLogTxt, "a")
    sensLog.write("\n[" + now.strftime("%Y-%m-%d %H:%M:%S] ") + formattedSens)

    liveSens = open(liveSensTxt, "w")
    liveSens.write(formattedSens)

    randomsens = open(directory.get() + "/cfg/randomsens.cfg", "w")
    randomsens.write("mouse_sensitivity " + f"{floatSens:.2f}")

    outputSensLabel.configure(text=formattedSens)


def findSteamDirectory():
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, R"SOFTWARE\WOW6432Node\Valve\Steam")
    path = winreg.QueryValueEx(key, "InstallPath")
    return path[0]


def apexLibraryPath(id):
    folders = vdf.load(open(rf"{findSteamDirectory()}\steamapps\libraryfolders.vdf"))
    vdfstring = folders.get("libraryfolders")

    for i in vdfstring.values():
        currentPath = i.get("path")
        for j in i.get("apps").keys():
            if j == id:
                return currentPath


def getApexPath():
    appmanifestpath = rf"{apexLibraryPath(apexID)}\steamapps\appmanifest_{apexID}.acf"
    appmanifest = vdf.load(open(appmanifestpath))
    for i in appmanifest.values():
        print("Path detected: ", rf"{apexLibraryPath(apexID)}\steamapps\common\{i.get('installdir')}")
        return rf"{apexLibraryPath(apexID)}\steamapps\common\{i.get('installdir')}"


def tryAutoDetectDirectory():
    try:
        directory.set(getApexPath())
        autoDetectDir.configure(bg=greenColors[theme.get()])
    except Exception as e:
        print(e)
        autoDetectDir.configure(bg=redColors[theme.get()])


# Main "Start Randomizer" toggle button
def toggleSensRandomizer():
    generateAutoExec()
    try:
        if timerInterval.get() < 1:
            timerInterval.set(1)
    except:
        timerInterval.set(10)

    # Flips the "running" switch once it confirms autoexecs have been generated
    if os.path.isfile(directory.get() + "/cfg/enablerando.cfg"):
        toggle()
        if running:
                keyboard.add_hotkey(updateBindModifiers(), randomize)
                if timerCheck.get():
                    startThreadedFunction(timerLoop, timerInterval.get())
        else:
            keyboard.remove_all_hotkeys()
            event.clear()
    else: # Errors message if game directory is invalid / autoexecs were not generated
        runButton.configure(text="Invalid game path!", bg=btnColor[1])


# Starts the main timer loop on a separate thread
def startThreadedFunction(function, args, button=False):
    if button:
        for i in activeElements:
            i.configure(state=stateToggle[1])
        button.config(relief=SUNKEN)
    if function == recordKey and button:
        args.set("...")
        button.configure(state=stateToggle[0])

    newThread = threading.Thread(target=function, args=(args, button,))
    newThread.daemon = True
    newThread.start()


# Main timer loop
def timerLoop(delay, button):
    event.set()
    timer = 0
    randomize()
    while event.is_set():
        timer += 1
        if timer == delay*10:
            randomize()
            timer = 0
        time.sleep(0.1)


# Returns the combined bind with modifiers for your randomize hotkey to feed to the hotkey generator
def updateBindModifiers():
    combinedBind = randomizeBindButton.cget("text")

    if ctrlCheck.get():
        combinedBind = "Ctrl + " + combinedBind

    if altCheck.get():
        combinedBind = "Alt + " + combinedBind

    if shiftCheck.get():
        combinedBind = "Shift + " + combinedBind

    return combinedBind


# Records your binds when clicking the bind buttons
def recordKey(bind, button):
    k = keyboard.read_key()
    if (k.isalnum() and not len(k) > 1 or k.startswith("f")):
        if len(k) > 1:
            k = str(k).upper()
            bind.set(k)
        else:
            bind.set(k)
    else:
        bind.set("Invalid")
    button.config(relief=RAISED)
    for i in activeElements:
        i.configure(state=stateToggle[0])


# Generates or edits your autoexec/cfg files with your current settings
def generateAutoExec():
    saveConfig()
    enablerStr = """#Automatically generated by Apex Sens Randomizer

bind \"w\" \"+forward; exec randomsens\"
bind \"s\" \"+backward; exec randomsens\"
bind \"a\" \"+moveleft; exec randomsens\"
bind \"d\" \"+moveright; exec randomsens\""""
    disableStr = """#Automatically generated by Apex Sens Randomizer

unbind \"w\"
unbind \"s\"
unbind \"a\"
unbind \"d\"
bind \"w\" \"+forward; exec randomsens\"
bind \"s\" \"+backward; exec randomsens\"
bind \"a\" \"+moveleft; exec randomsens\"
bind \"d\" \"+moveright; exec randomsens\"
mouse_sensitivity """ + baseSens.get()

    autoexecStr = "#Automatically generated by Apex Sens Randomizer\n\nbind \"" + enableBind.get() + "\" \"exec enablerando\"\nbind \"" + disableBind.get() + "\" \"exec disablerando\""
    try:
        enableRando = open(directory.get() + "/cfg/enablerando.cfg", "w")
        enableRando.write(enablerStr)
    except FileNotFoundError:
        runButton.configure(text="Incorrect game path!", bg=btnColor[1], state="disabled")
        return
    
    try:
        disableRando = open(directory.get() + "/cfg/disablerando.cfg", "w")
        disableRando.write(disableStr)
    except FileNotFoundError:
        pass

    try:
        with open(directory.get() + "/cfg/autoexec.cfg", 'r+') as autoexec:
            lines = autoexec.readlines()
            line_number = None
            for i, line in enumerate(lines):
                if "enablerando" in line:
                    line_number = i
                    break
            if line_number is not None:
                lines[line_number] = "bind \"" + enableBind.get() + "\" \"exec enablerando\"" + "\n"
            with open(directory.get() + "/cfg/autoexec.cfg", 'w') as autoexec:
                autoexec.writelines(lines)
        
        with open(directory.get() + "/cfg/autoexec.cfg", 'r+') as autoexec:
            lines = autoexec.readlines()
            line_number = None
            for i, line in enumerate(lines):
                if "disablerando" in line:
                    line_number = i
                    break
            if line_number is not None:
                lines[line_number] = "bind \"" + disableBind.get() + "\" \"exec disablerando\"" + "\n"
            else:
                try:
                    lines[len(lines)] = lines[len(lines)] + "\n"
                    lines.append(autoexecStr)
                except:
                    lines.append(autoexecStr)
            with open(directory.get() + "/cfg/autoexec.cfg", 'w') as autoexec:
                autoexec.writelines(lines)
    except FileNotFoundError:
        with open(directory.get() + "/cfg/autoexec.cfg", 'x') as autoexec:
            autoexec.write(autoexecStr)
    finally:
        runButton.configure(text="Start Randomizer", bg="#b0ffb9")


# Saves your current settings to config.json
def saveConfig():
    try:
        if timerInterval.get() < 1:
            timerInterval.set(1)
    except:
        timerInterval.set(10)

    dpi.set(dpi.get() or "800")
    minSens.set(minSens.get() or "0.7")
    maxSens.set(maxSens.get() or "3.8")
    baseSens.set(baseSens.get() or "1.5")
    if randomizeBind.get() == "Bind" or randomizeBind.get() == "Invalid" or randomizeBind.get() == "...":
        randomizeBind.set("x")
        if not any([ctrlCheck.get(), altCheck.get(), shiftCheck.get()]):
            altCheck.set(True)
    if enableBind.get() == "Bind" or enableBind.get() == "Invalid":
        enableBind.set("F6")
    if disableBind.get() == "Bind" or disableBind.get() == "Invalid":
        disableBind.set("F7")
    if float(maxSens.get()) < float(minSens.get()):
        maxSens.set(str(float(minSens.get()) + 1))

    configuration = {
        "directory": directory.get(),
        "dpi": dpi.get(),
        "min_sensitivity": minSens.get(),
        "max_sensitivity": maxSens.get(),
        "base_sensitivity": baseSens.get(),
        "randomize_bind": randomizeBind.get(),
        "randomize_bind_modifiers": [str(ctrlCheck.get()), str(altCheck.get()), str(shiftCheck.get())],
        "timer": [str(timerCheck.get()), str(timerInterval.get())],
        "enable_bind": enableBind.get(),
        "disable_bind": disableBind.get(),
        "theme": theme.get()
    }

    with open("config.json", "w") as config_file:
        json.dump(configuration, config_file, indent=4)


# Loads your config.json file to restore your settings when restarting the program
def loadConfig():
    try:
        with open("config.json", "r") as config_file:
            configuration = json.load(config_file)
            
            directory.set(configuration.get("directory", ""))
            dpi.set(configuration.get("dpi", ""))
            minSens.set(configuration.get("min_sensitivity", ""))
            maxSens.set(configuration.get("max_sensitivity", ""))
            baseSens.set(configuration.get("base_sensitivity"))
            randomizeBind.set(configuration.get("randomize_bind", ""))
            modifiers = configuration.get("randomize_bind_modifiers")
            ctrlCheck.set(modifiers[0])
            altCheck.set(modifiers[1])
            shiftCheck.set(modifiers[2])
            timer = configuration.get("timer")
            timerCheck.set(timer[0])
            timerInterval.set(timer[1])
            enableBind.set(configuration.get("enable_bind", ""))
            disableBind.set(configuration.get("disable_bind", ""))
            theme.set(configuration.get("theme", ""))
        
        print("Configuration loaded successfully")
    except FileNotFoundError:
        print("No configuration file found")


# Opens corresponding URL in a new tab when clicking my socials buttons
def openSite(url):
    webbrowser.open_new_tab(url)



# Theme toggle button. Under construction!
#def toggleTheme():
#    theme.set(not theme.get())
#    window.configure(bg=baseBackgroundColors[theme.get()])
#    for blank in blankElements:
#        blank.configure(bg=baseBackgroundColors[theme.get()], fg=foregroundColors[theme.get()])
#    for interactable in interactableElements:
#        interactable.configure(bg=interactableBackgroundColors[theme.get()], fg=foregroundColors[theme.get()])
#    for idiots in dumbInteractableElements:
#        style.map('TCombobox', fieldbackground=[('readonly', interactableBackgroundColors[theme.get()])])
#    print("Dark mode: ", theme.get())


icon = """AAABAAMAEBAAAAEABAAoAQAANgAAABgYAAABAAQA6AEAAF4BAAAgIAAAAQAEAOgCAABGAwAAKAAA
ABAAAAAgAAAAAQAEAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAP///wDs7OwA0dHRALq6ugCysrIA
rKysAJKSkgCIiIgAfX19AGdnZwBYWFgAT09PAEFBQQAvLy8AFhYWAAICAgAAAAx3d8AAAAAAYAAA
BgAAAAsACSAAsAAABQAEEABQAAAEAApQAEAAAAQACd4gQAAABAagDmBAAAAEA/3fIEAAAAUAIzIA
UAAACnhohoegAAADAAVQADAAAAUABEAAUAAACgAEQACgAAAPIARAAvAAAADjAzA+AAAAAA+6q/AA
APgfAADwDwAA4AcAAOAHAADgBwAA4AcAAOAHAADgBwAA4AcAAOAHAADgBwAA4AcAAOAHAADgBwAA
8A8AAPgfAAAoAAAAGAAAADAAAAABAAQAAAAAAMABAAAAAAAAAAAAAAAAAAAAAAAA////APr6+gDp
6ekA0dHRAMXFxQCtra0Am5ubAI2NjQB4eHgAampqAF5eXgBHR0cANDQ0ACAgIAAQEBAAAAAAAAAA
AA/8u7vP8AAAAAAAAPggAAACjwAAAAAAD1AAAAAABfAAAAAACgAAJzAAAKAAAAAA8wAAT2AAAD8A
AAAA4QAAAAAAAB4AAAAA4QAAKjAAAB4AAAAA4QAAT9pgAB4AAAAA4QAAGs31AB4AAAAA4QB7AAH4
AB4AAAAA4QCvUzb4AB4AAAAA4QBP///zAB4AAAAA4AACREQgAA4AAAAA5VVUQzRFVV4AAAAA+ZmZ
jMiZmZ8AAAAA4AAAB3AAAA4AAAAA4QAAB3AAAB4AAAAA8gAAB3AAAC8AAAAA9QAAB3AAAF8AAAAA
DAAAB3AAAMAAAAAAD3AAB3AAB/AAAAAAAPYAB3AAbwAAAAAAAA+0B3BL8AAAAAAAAAAP3d3wAAAA
AP4AfwD8AD8A+AAfAPgAHwDwAA8A8AAPAPAADwDwAA8A8AAPAPAADwDwAA8A8AAPAPAADwDwAA8A
8AAPAPAADwDwAA8A8AAPAPAADwD4AB8A+AAfAPwAPwD+AH8A/4H/ACgAAAAgAAAAQAAAAAEABAAA
AAAAwAIAAAAAAAAAAAAAAAAAAAAAAAD///8A7OzsAN7e3gC+vr4Ap6enAJiYmACKiooAcnJyAGdn
ZwBcXFwASUlJADU1NQAqKioAGxsbAAsLCwAAAAAAAAAAAAD//u7u7/8AAAAAAAAAAAAPpCERERJK
8AAAAAAAAAAP9AAAAAAAAE/wAAAAAAAADzAAAAAAAAAD8AAAAAAAAPgAAAAjIAAAAI8AAAAAAADx
AAAAr3AAAAAfAAAAAAAAsAAAAFpAAAAACwAAAAAAD5AAAAAAAAAAAAnwAAAAAA+QAAAARzAAAAAJ
8AAAAAAPkAAAAK+RIAAACfAAAAAAD5AAAACP//sQAAnwAAAAAA+QAAAAKJnfcAAJ8AAAAAAPkAAG
gwAAb5AACfAAAAAAD5AADPUAAG+QAAnwAAAAAA+QAAr8mZnfkAAJ8AAAAAAPkAAD/////iAACfAA
AAAAD5AAACREREEAAAnwAAAAAA+AAAAAAAAAAAAI8AAAAAAP2qqqqqmaqqqqrfAAAAAAD7VmZmZc
xWZmZlvwAAAAAA+AAAAAB3AAAAAI8AAAAAAPkAAAAAiAAAAACfAAAAAAD5AAAAAIgAAAAAnwAAAA
AADAAAAACIAAAAAMAAAAAAAA8QAAAAiAAAAAHwAAAAAAAPYAAAAIgAAAAG8AAAAAAAAOAAAACIAA
AADgAAAAAAAAD6AAAAiAAAAK8AAAAAAAAAD5AAAIgAAAnwAAAAAAAAAAD7IACIAAK/AAAAAAAAAA
AAD/pBmRSv8AAAAAAAAAAAAAAP////8AAAAAAAD/wAP//4AB//4AAH/+AAB//AAAP/wAAD/8AAA/
+AAAH/gAAB/4AAAf+AAAH/gAAB/4AAAf+AAAH/gAAB/4AAAf+AAAH/gAAB/4AAAf+AAAH/gAAB/4
AAAf+AAAH/wAAD/8AAA//AAAP/4AAH/+AAB//wAA//+AAf//wAP///AP/w=="""

window = tk.Tk()
style = ttk.Style()
window.title("Apex Sens Randomizer")
window.resizable(False, False)

icondata = base64.b64decode(icon)
tempFile = "icon.ico"
iconfile = open(tempFile, "wb")
iconfile.write(icondata)
iconfile.close()
window.wm_iconbitmap(tempFile)
os.remove(tempFile)
window.columnconfigure(3, pad=10)

theme = tk.BooleanVar(window, 0)
directory = tk.StringVar()
dpi = tk.StringVar()
minSens = tk.StringVar()
maxSens = tk.StringVar()
baseSens = tk.StringVar()
randomizeBind = tk.StringVar(window, "Bind")
ctrlCheck = tk.BooleanVar()
altCheck = tk.BooleanVar()
shiftCheck = tk.BooleanVar()
timerCheck = tk.BooleanVar()
timerInterval = tk.IntVar()
timerInterval.set(10)
enableBind = tk.StringVar(window, "Bind")
disableBind = tk.StringVar(window, "Bind")


sensLogTxt = "sensitivity_log.txt"
liveSensTxt = "current_sensitivity.txt"

event = threading.Event()

running = False

#themeButton = tk.Button(window, text="Theme", command=toggleTheme)
#themeButton.grid(row=0, column=0, columnspan=1, sticky=tk.EW, padx=4)

gameDirLabel = tk.Label(window, text="Game directory:")
gameDirLabel.grid(row=0, column=0, sticky=tk.E, padx=4)

gameDir = tk.Entry(window, textvariable=directory)
gameDir.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

selectFolder = tk.Button(window, text="Browse...", command=select_folder)
selectFolder.grid(row=0, column=2, pady=5, sticky=tk.W)

dpiLabel = tk.Label(window, text="Mouse DPI:")
dpiLabel.grid(row=1, column=0, sticky=tk.E, padx=4)

dpiEntry = ttk.Combobox(window, values=["400", "800", "1600"], validate="key", textvariable=dpi)
dpiEntry.config(validatecommand=(window.register(validate_purenumber_input), "%P"))
dpiEntry.grid(row=1, column=1, padx=5, pady=5)

dpiEntry['state'] = 'readonly'

minSensLabel = tk.Label(window, text="Min sensitivity:")
minSensLabel.grid(row=2, column=0, sticky=tk.E, padx=4)

minSensEntry = tk.Entry(window, validate="key", textvariable=minSens)
minSensEntry.config(validatecommand=(window.register(validate_number_input), "%P"))
minSensEntry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

maxSensLabel = tk.Label(window, text="Max sensitivity:")
maxSensLabel.grid(row=3, column=0, sticky=tk.E, padx=4)

maxSensEntry = tk.Entry(window, validate="key", textvariable=maxSens)
maxSensEntry.config(validatecommand=(window.register(validate_number_input), "%P"))
maxSensEntry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)

baseSensLabel = tk.Label(window, text="Default sensitivity:")
baseSensLabel.grid(row=4, column=0, sticky= tk.E, padx=4)

baseSensEntry = tk.Entry(window, validate="key", textvariable=baseSens)
baseSensEntry.config(validatecommand=(window.register(validate_number_input), "%P"))
baseSensEntry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.EW)

runButton = tk.Button(window, bg="#b0ffb9", text="Start Randomizer", command=toggleSensRandomizer)
runButton.grid(row=6, column=0, columnspan=2, rowspan=1, padx=25, ipady=15, sticky=tk.EW, pady=5)

autoexecButton = tk.Button(window, text="Save settings", command=generateAutoExec)
autoexecButton.grid(row=5, column=0, columnspan=2, padx=25, ipady=3, pady=2, sticky=tk.EW)


hotkeyLabelFrame = tk.LabelFrame(window, text="")
hotkeyLabelFrame.grid(row=1, column=2, rowspan=3, columnspan=2, sticky="NSEW")

autoDetectDir = tk.Button(window, text="Auto", command=tryAutoDetectDirectory)
autoDetectDir.grid(row=0, column=3, columnspan=1, padx=4, sticky=tk.EW)

randomizeBindButton = tk.Button(window, textvariable=randomizeBind, command=lambda: startThreadedFunction(recordKey, randomizeBind, randomizeBindButton))
randomizeBindButton.grid(row=1, column=3, columnspan=1, sticky=tk.EW, padx=4)

randomizeBindLabel = tk.Label(window, text="Randomize sens:")
randomizeBindLabel.grid(row=1, column=2, sticky=tk.E, padx=4)

modifierBoxCtrl = tk.Checkbutton(window, text="Ctrl", variable=ctrlCheck)
modifierBoxCtrl.grid(row=2, column=2, sticky=tk.W, padx=2)

modifierBoxAlt = tk.Checkbutton(window, text="Alt", variable=altCheck)
modifierBoxAlt.grid(row=2, column=2, columnspan=2)

modifierBoxShift = tk.Checkbutton(window, text="Shift", variable=shiftCheck)
modifierBoxShift.grid(row=2, column=3, sticky=tk.E, padx=2)

enableBindButton = tk.Button(window, text="Bind", textvariable=enableBind, command=lambda: startThreadedFunction(recordKey, enableBind, enableBindButton))
enableBindButton.grid(row=4, column=3, columnspan=1, sticky=tk.EW, padx=4)

enableBindLabel = tk.Label(window, text="Enable in-game:")
enableBindLabel.grid(row=4, column=2, sticky=tk.E, padx=4)

useTimerBox = tk.Checkbutton(window, text="Timer in seconds:", variable=timerCheck)
useTimerBox.grid(row=3, column=2, sticky=tk.W, padx=2)

timerIntervalEntry = tk.Entry(window, textvariable=timerInterval, validate="key", width=9, validatecommand=(window.register(validate_purenumber_input), "%P"))
timerIntervalEntry.grid(row=3, column=3, padx=2)

disableBindButton = tk.Button(window, text="Bind", textvariable=disableBind, command=lambda: startThreadedFunction(recordKey, disableBind, disableBindButton))
disableBindButton.grid(row=5, column=3, columnspan=1, sticky=tk.EW, padx=4)

disableBindLabel = tk.Label(window, text="Disable in-game:")
disableBindLabel.grid(row=5, column=2, sticky=tk.E, padx=4)

outputLabelFrame = tk.LabelFrame(window, text="Current sens")
outputLabelFrame.grid(row=6, column=2, columnspan=2, rowspan=2, padx=2, pady=4, ipadx=40, sticky="NSEW")

outputSensLabel = tk.Label(window, text="Not running")
outputSensLabel.grid(row=6, column=2, columnspan=2, rowspan=2)

torjeLabel = tk.Label(window, text="Created by Torje:")
torjeLabel.grid(row=8, column=0, padx=3, pady=2)

twitchLink = tk.Label(window, text="Twitch", fg="#6441a5", cursor="hand2")
twitchLink.grid(row=8, column=1, pady=2, sticky=tk.W, padx=50)
twitchLink.bind("<Button-1>", lambda e: openSite("https://www.twitch.tv/torje"))

youtubeLink = tk.Label(window, text="YouTube", fg="#c4302b", cursor="hand2")
youtubeLink.grid(row=8, column=1, pady=2, sticky=tk.E)
youtubeLink.bind("<Button-1>", lambda e: openSite("https://www.youtube.com/channel/UCAUkwc3fVqhAtzk8reZfkJw"))

twitterLink = tk.Label(window, text="Twitter", fg="blue", cursor="hand2")
twitterLink.grid(row=8, column=1, pady=2, sticky=tk.W)
twitterLink.bind("<Button-1>", lambda e: openSite("https://twitter.com/Txrje"))

# Commented out temporarily, these lists are for a future dark theme/light theme toggle button.
#
#blankElements = [gameDirLabel, dpiLabel, minSensLabel, maxSensLabel, baseSensLabel, hotkeyLabelFrame,
#                 randomizeBindLabel, modifierBoxCtrl, modifierBoxAlt, modifierBoxShift, modifierBoxShift,
#                 enableBindLabel, useTimerBox, disableBindLabel, outputLabelFrame, outputSensLabel,
#                 torjeLabel, twitchLink, youtubeLink, twitterLink]
#interactableElements = [themeButton, gameDir, selectFolder, minSensEntry, maxSensEntry,
#                        baseSensEntry, autoexecButton, randomizeBindButton, enableBindButton,
#                        timerIntervalEntry, disableBindButton]
#dumbInteractableElements = [dpiEntry]


# A lot of these are for a future theme switcher, some are needed already though

baseBackgroundColors = ["#f0f0f0", "#151518"]
interactableBackgroundColors = ["#ffffff", "#1f1f22"]
foregroundColors = ["#000000", "#d0d0d0"]
greenColors = ["#b0ffb9", "#0c540e"]
greenActive = ["#b3e6b9", "#136115"]
redColors = ["#d48e8e", "#420b0b"]
redActive = ["#e09f9f", "#521212"]
btnColor = [greenColors[theme.get()], redColors[theme.get()]]
btnActive = [greenActive[0], redActive[0]]
stateToggle = ["normal", "disabled"]
btnText = ["Start Randomizer", "Stop Randomizer"]
activeElements = [randomizeBindButton, enableBindButton, disableBindButton, selectFolder, runButton,
                  autoexecButton, modifierBoxCtrl, modifierBoxAlt, modifierBoxShift, useTimerBox, timerIntervalEntry,
                  gameDir, selectFolder, dpiEntry, minSensEntry, maxSensEntry, baseSensEntry]

apexID = "1172470"

if __name__ == "__main__":
    loadConfig()
    window.mainloop()

#       To-do list (not the order these will be done in)
#
# 1.    Add default steam directory finding through windows registry reading to find steam installation folder,
#       then parsing libraryfolders.vdf to find other installation folders,
#       and also parsing appmanifest_<steamappid>.acf to find Apex's specific installation folder
#
#       1. DONE!
#
#
# 2.    Threaded bind hotkeys. Make the recordKey(button) function run on a separate thread
#       in order to free up UI customization while waiting for a keypress.
#       This should also fix the crash that happens when you click anything else in the window while the program
#       is still waiting for a keypress.
#
#       2. DONE!
#
#
# 3.    Dark theme. Save the retinas.
#
#
# 4.    Replace os.sleep with a time delta
#
#
# 5.    Check for updates on launch