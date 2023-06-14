import tkinter as tk
from tkinter import ttk, filedialog
import re
import json
import random
import keyboard
import os
from os import path
import icon
import base64


def select_folder():
    gameDirPath = filedialog.askdirectory()
    gameDir.delete(0, tk.END)
    gameDir.insert(0, gameDirPath)


def validate_number_input(text):
    return re.match(r'^\d*\.?\d{0,2}$', text) is not None or text == ""


def validate_purenumber_input(text):
    return text.isdigit() or text == ""


running = False

def toggle():
    global running
    global runButton
    btnText = ["Start Randomizer", "Stop Randomizer"]
    btnColor = ["#b0ffb9", "#d48e8e"]
    btnActive = ["#b3e6b9", "#e09f9f"]
    stateToggle = ["normal", "disabled"]
    sensStateToggle = ["Not running", "Press " + updateBindModifiers() + "!"]
    running = not running
    runButton.configure(text=btnText[running], bg=btnColor[running], activebackground=btnActive[0])
    gameDir.configure(state=stateToggle[running])
    dpiEntry.configure(state=stateToggle[running])
    minSensEntry.configure(state=stateToggle[running])
    maxSensEntry.configure(state=stateToggle[running])
    autoexecButton.configure(state=stateToggle[running])
    saveButton.configure(state=stateToggle[running])
    randomizeBindButton.configure(state=stateToggle[running])
    enableBindButton.configure(state=stateToggle[running])
    disableBindButton.configure(state=stateToggle[running])
    selectFolder.configure(state=stateToggle[running])
    modifierBoxAlt.configure(state=stateToggle[running])
    modifierBoxCtrl.configure(state=stateToggle[running])
    modifierBoxShift.configure(state=stateToggle[running])
    outputSensLabel.configure(text=sensStateToggle[running])
    print(btnText[running])


def randomize():
    if isConfigured():
        randomsens = open(directory + "/cfg/randomsens.cfg", "w")
        minFloat = float(minSensEntry.get())
        maxFloat = float(maxSensEntry.get())
        initRNG = random.uniform(minFloat, maxFloat)
        actualSensNum = round(initRNG, 2)
        floatSens = float(actualSensNum)
        print(f"{floatSens:.2f}")
        sensLog = open(sensLogTxt, "a")
        cmRev = str(round((360 / (0.022 * int(dpi) * floatSens)) * 2.54, 1))
        formattedSens = cmRev + "cm/360 (" + f"{floatSens:.2f}" + " @ " + str(dpi) + " DPI)"
        sensLog.write("\n")
        sensLog.write(formattedSens)
        randomsens.write("mouse_sensitivity " + f"{floatSens:.2f}")
        outputSensLabel.configure(text=formattedSens)
    


def toggleSensRandomizer():
    toggle()
    reloadData()
    if running:
            save_configuration()
            keyboard.add_hotkey(updateBindModifiers(), randomize)
    else:
        keyboard.remove_all_hotkeys()

def record_key(event):
    key = event.char
    #randomizeBind.insert(0, key)

def recordKey(): #Function for clicking the bind button for "Randomize sens"
    k = keyboard.read_key()
    if (k.isalnum() and not len(k) > 1 or k.startswith("f")):
        if len(k) > 1:
            k = str(k).upper()
            randomizeBindButton.configure(text=k)
        else:
            randomizeBindButton.configure(text=k)
    else:
        randomizeBindButton.configure(text="Invalid")

def recordKey2(): #Function for clicking the bind button for "Enable in-game"
    k = keyboard.read_key()
    if (k.isalnum() and not len(k) > 1 or k.startswith("f")):
        if len(k) > 1:
            k = str(k).upper()
            enableBindButton.configure(text=k)
        else:
            enableBindButton.configure(text=k)
    else:
        enableBindButton.configure(text="Invalid")

def recordKey3(): #Function for clicking the bind button for "Disable in-game"
    k = keyboard.read_key()
    if (k.isalnum() and not len(k) > 1 or k.startswith("f")):
        if len(k) > 1:
            k = str(k).upper()
            disableBindButton.configure(text=k)
        else:
            disableBindButton.configure(text=k)
    else:
        disableBindButton.configure(text="Invalid")

#Please ignore the disgusting repeating recordKey functions, I'll figure out a better way to do that when I've written Python for more than half a day LOL

def generateAutoExec():
    save_configuration()
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
bind \"d\" \"+moveright; exec randomsens\""""

    autoexecStr = "#Automatically generated by Apex Sens Randomizer\n\nbind \"" + enable_bind + "\" \"exec enablerando\"\nbind \"" + disable_bind + "\" \"exec disablerando\""
    try:
        enableRando = open(directory + "/cfg/enablerando.cfg", "w")
        enableRando.write(enablerStr)
        runButton.configure(text="Start Randomizer")
    except FileNotFoundError:
        runButton.configure(state="disabled", text="Incorrect game path!")
    
    try:
        disableRando = open(directory + "/cfg/disablerando.cfg", "w")
        disableRando.write(disableStr)
    except:
        runButton.configure(text="Incorrect game path!")
    try:
        with open(directory + "/cfg/autoexec.cfg", 'r+') as autoexec:
            lines = autoexec.readlines()
            line_number = None
            for i, line in enumerate(lines):
                if "enablerando" in line:
                    line_number = i
                    break
            if line_number is not None:
                lines[line_number] = "bind \"" + enable_bind + "\" \"exec enablerando\"" + "\n"
            with open(directory + "/cfg/autoexec.cfg", 'w') as autoexec:
                autoexec.writelines(lines)
        
        with open(directory + "/cfg/autoexec.cfg", 'r+') as autoexec:
            lines = autoexec.readlines()
            line_number = None
            for i, line in enumerate(lines):
                if "disablerando" in line:
                    line_number = i
                    break
            if line_number is not None:
                lines[line_number] = "bind \"" + disable_bind + "\" \"exec disablerando\"" + "\n"
            with open(directory + "/cfg/autoexec.cfg", 'w') as autoexec:
                autoexec.writelines(lines)
    except FileNotFoundError:
        with open(directory + "/cfg/autoexec.cfg", 'x') as autoexec:
            autoexec.write(autoexecStr)


# INCOMPLETE ABOVE, FINISH KEY BIND FUNCTION FIRST

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


gameDirLabel = tk.Label(window, text="Game directory:")
gameDirLabel.grid(row=0, column=0, sticky=tk.E, padx=4)

gameDir = tk.Entry(window)
gameDir.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

selectFolder = tk.Button(window, text="Browse...", command=select_folder)
selectFolder.grid(row=0, column=2, pady=5, sticky=tk.W)

dpiLabel = tk.Label(window, text="Mouse DPI:")
dpiLabel.grid(row=1, column=0, sticky=tk.E, padx=4)

dpiEntry = ttk.Combobox(window, values=["400", "800", "1600"])
dpiEntry.config(validatecommand=(window.register(validate_purenumber_input), "%P"))
dpiEntry.grid(row=1, column=1, padx=5, pady=5)

hotkeyLabelFrame = tk.LabelFrame(window, text="")
hotkeyLabelFrame.grid(row=1, column=2, rowspan=2, columnspan=2, sticky="NSEW")

minSensLabel = tk.Label(window, text="Min sensitivity:")
minSensLabel.grid(row=2, column=0, sticky=tk.E, padx=4)

minSensEntry = tk.Entry(window, validate="key")
minSensEntry.config(validatecommand=(window.register(validate_number_input), "%P"))
minSensEntry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

maxSensLabel = tk.Label(window, text="Max sensitivity:")
maxSensLabel.grid(row=3, column=0, sticky=tk.E, padx=4)

maxSensEntry = tk.Entry(window, validate="key")
maxSensEntry.config(validatecommand=(window.register(validate_number_input), "%P"))
maxSensEntry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)


runButton = tk.Button(window, bg="#b0ffb9", text="Start Randomizer", command=toggleSensRandomizer)
runButton.grid(row=5, column=0, columnspan=2, rowspan=2, padx=5, ipady=15, sticky=tk.EW, pady=5)

autoexecButton = tk.Button(window, text="Generate autoexec", command=generateAutoExec)
autoexecButton.grid(row=4, column=1, columnspan=1, padx=5, pady=10, sticky=tk.EW)

hotkeysLabel = tk.Label(window, text="Hotkey/binds:   ")
hotkeysLabel.grid(row=0, column=2, columnspan=2, sticky=tk.E)

randomizeBindButton = tk.Button(window, text="Bind", command=recordKey)
randomizeBindButton.grid(row=1, column=3, columnspan=1, sticky=tk.EW, padx=6)

randomizeBindLabel = tk.Label(window, text="Randomize sens:")
randomizeBindLabel.grid(row=1, column=2, sticky=tk.E, padx=4)

ctrlCheck = tk.BooleanVar()
altCheck = tk.BooleanVar()
shiftCheck = tk.BooleanVar()

def updateBindModifiers():
    global modified_string
    modified_string = randomizeBindButton.cget("text")

    if ctrlCheck.get():
        modified_string = "Ctrl + " + modified_string

    if altCheck.get():
        modified_string = "Alt + " + modified_string

    if shiftCheck.get():
        modified_string = "Shift + " + modified_string

    return modified_string

modifierBoxCtrl = tk.Checkbutton(window, text="Ctrl", variable=ctrlCheck)
modifierBoxCtrl.grid(row=2, column=2, sticky=tk.W, padx=2)

modifierBoxAlt = tk.Checkbutton(window, text="Alt", variable=altCheck)
modifierBoxAlt.grid(row=2, column=2, columnspan=2)

modifierBoxShift = tk.Checkbutton(window, text="Shift", variable=shiftCheck)
modifierBoxShift.grid(row=2, column=3, sticky=tk.E, padx=2)

enableBindButton = tk.Button(window, text="Bind", command=recordKey2)
enableBindButton.grid(row=3, column=3, columnspan=1, sticky=tk.EW, padx=6)

enableBindLabel = tk.Label(window, text="Enable in-game:")
enableBindLabel.grid(row=3, column=2, sticky=tk.E, padx=4)

disableBindButton = tk.Button(window, text="Bind", command=recordKey3)
disableBindButton.grid(row=4, column=3, columnspan=1, sticky=tk.EW, padx=6)

disableBindLabel = tk.Label(window, text="Disable in-game:")
disableBindLabel.grid(row=4, column=2, sticky=tk.E, padx=4)

#separator1 = ttk.Separator(window, orient="horizontal")
#separator1.grid(row=1, column=2, columnspan=2, sticky="NEW")

#separator2 = ttk.Separator(window, orient="horizontal")
#separator2.grid(row=2, column=2, columnspan=2, sticky="SEW")

#separator3 = ttk.Separator(window, orient="vertical")
#separator3.grid(row=1, column=2, rowspan=2, sticky="NSW")

#separator4 = ttk.Separator(window, orient="vertical")
#separator4.grid(row=1, column=3, rowspan=2, sticky="NSE")

def load_configuration():
    try:
        with open("config.json", "r") as config_file:
            configuration = json.load(config_file)
            
            gameDir.insert(0, configuration.get("directory", ""))
            dpiEntry.set(configuration.get("dpi", ""))
            minSensEntry.insert(0, configuration.get("min_sensitivity", ""))
            maxSensEntry.insert(0, configuration.get("max_sensitivity", ""))
            if configuration.get("randomize_bind", "") != "":
                randomizeBindButton.configure(text=configuration.get("randomize_bind", ""))
            modifiers = configuration.get("randomize_bind_modifiers")
            if modifiers:
                ctrlCheck.set(modifiers[0])
                altCheck.set(modifiers[1])
                shiftCheck.set(modifiers[2])
            if configuration.get("enable_bind", "") != "":
                enableBindButton.configure(text=configuration.get("enable_bind", ""))
            if configuration.get("disable_bind", "") != "":
                disableBindButton.configure(text=configuration.get("disable_bind", ""))
        
        print("Configuration loaded successfully")
    except FileNotFoundError:
        print("No configuration file found")

load_configuration()

def reloadData():

    global directory
    global dpi
    global min_sensitivity
    global max_sensitivity
    global randomize_bind
    global randomize_bind_button
    global enable_bind
    global disable_bind

    directory = gameDir.get()
    dpi = dpiEntry.get()
    min_sensitivity = minSensEntry.get()
    max_sensitivity = maxSensEntry.get()
    randomize_bind_button = randomizeBindButton.cget("text")
    randomize_bind = updateBindModifiers()
    enable_bind = enableBindButton.cget("text")
    disable_bind = disableBindButton.cget("text")

    print(directory, dpi, min_sensitivity, max_sensitivity, randomize_bind, enable_bind, disable_bind)

reloadData()

sensLogTxt = "sensitivity_log.txt"
liveSensTxt = "current_sensitivity.txt"

def save_configuration():
    reloadData()
    try:
        configuration = {
            "directory": directory,
            "dpi": dpi,
            "min_sensitivity": min_sensitivity,
            "max_sensitivity": max_sensitivity,
            "randomize_bind": randomize_bind_button,
            "randomize_bind_modifiers": [str(ctrlCheck.get()), str(altCheck.get()), str(shiftCheck.get())],
            "enable_bind": enable_bind,
            "disable_bind": disable_bind
        }
            
        with open("config.json", "w") as config_file:
            json.dump(configuration, config_file, indent=4)
            
        print(directory, dpi, min_sensitivity, max_sensitivity, randomize_bind, randomize_bind, enable_bind, disable_bind)
        if not isConfigured():
            runButton.configure(text="Fill in all settings correctly first!", bg="#d48e8e")
        else:
            runButton.configure(state="normal")
    except:
        runButton.configure(text="Fill in all settings first!", state="disabled")

def isConfigured():
    if "" in {directory, dpi, min_sensitivity, max_sensitivity} or "Bind" in {randomize_bind_button, enable_bind, disable_bind} or float(max_sensitivity) < float(min_sensitivity) or "Invalid" in {randomize_bind_button, enable_bind, disable_bind}:
        return False
    else:
        return True

saveButton = tk.Button(window, text="Save settings", command=save_configuration)
saveButton.grid(row=4, column=0, columnspan=1, pady=5, padx=5, sticky=tk.EW)

outputLabelFrame = tk.LabelFrame(window, text="Current sens")
outputLabelFrame.grid(row=5, column=2, columnspan=2, rowspan=2, padx=2, pady=4, ipadx=40, sticky="NSEW")

outputSensLabel = tk.Label(window, text="Not running")
outputSensLabel.grid(row=5, column=2, columnspan=2, rowspan=2)

#authorLabel = tk.Label(window, text="Made by Torje")
#authorLabel.grid(row=6, column = 4)

window.mainloop()