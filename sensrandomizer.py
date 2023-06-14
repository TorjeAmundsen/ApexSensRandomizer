import tkinter as tk
from tkinter import ttk, filedialog
import re
import json
import random
import keyboard
import os
from os import path


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
    btnText = ["Start Randomizer", "Stop Randomizer"]
    btnColor = ["#b0ffb9", "#d48e8e"]
    btnActive = ["#b3e6b9", "#e09f9f"]
    global running
    global runButton
    running = not running
    runButton.configure(text=btnText[running], bg=btnColor[running], activebackground=btnActive[0])


def randomize():
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
    if len(k) > 1:
        k = str(k).upper()
        randomizeBindButton.configure(text=k)
    else:
        randomizeBindButton.configure(text=k)

def recordKey2(): #Function for clicking the bind button for "Enable in-game"
    k = keyboard.read_key()
    if len(k) > 1:
        k = str(k).upper()
        enableBindButton.configure(text=k)
    else:
        enableBindButton.configure(text=k)

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
    try:
        enableRando = open(directory + "/cfg/enablerando.cfg", "w")
        enableRando.write(enablerStr)
        runButton.configure(text="Start Randomizer")
    except FileNotFoundError:
        runButton.configure(text="Incorrect game path!")
    
    try:
        disableRando = open(directory + "/cfg/disablerando.cfg", "w")
        disableRando.write(disableStr)
    except:
        runButton.configure(text="Incorrect game path!")
    try:
        with open(directory + "/cfg/autoexec.cfg", 'r') as autoexec:
            lines = autoexec.readlines()
            for line in lines:
                if line.find("exec enablerando") != -1:
                    print("", 'string exists in file')
                    print('Line Number:', lines.index(line))
                    print('Line:', line)
    except FileNotFoundError:
        with open(directory + "/cfg/autoexec.cfg", 'x') as autoexec:
            lines = autoexec.readlines()


# INCOMPLETE ABOVE, FINISH KEY BIND FUNCTION FIRST

window = tk.Tk()

window.title("Apex Sens Randomizer")
window.iconbitmap("randoicon.ico")

gameDirLabel = tk.Label(window, text="Game directory:")
gameDirLabel.grid(row=0, column=0, sticky=tk.E, padx=4)

gameDir = tk.Entry(window)
gameDir.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

selectFolder = tk.Button(window, text="Select folder", command=select_folder)
selectFolder.grid(row=0, column=2, padx=5, pady=5)

dpiLabel = tk.Label(window, text="Mouse DPI:")
dpiLabel.grid(row=1, column=0, sticky=tk.E, padx=4)

dpiEntry = ttk.Combobox(window, values=["400", "800", "1600"])
dpiEntry.config(validatecommand=(window.register(validate_purenumber_input), "%P"))
dpiEntry.grid(row=1, column=1, padx=5, pady=5)


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
runButton.grid(row=5, column=1, columnspan=1, rowspan=2, padx=5, ipady=5, sticky=tk.EW, pady=15)

autoexecButton = tk.Button(window, text="Generate autoexec", command=generateAutoExec)
autoexecButton.grid(row=4, column=1, columnspan=1, padx=5, pady=10, sticky=tk.EW)

blankLabel = tk.Label(window, text="Keybinds")
blankLabel.grid(row=0, column=3, sticky=tk.EW, padx=8)

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
modifierBoxCtrl.grid(row=2, column=2, sticky=tk.W)

modifierBoxAlt = tk.Checkbutton(window, text="Alt", variable=altCheck)
modifierBoxAlt.grid(row=2, column=2, columnspan=2)

modifierBoxShift = tk.Checkbutton(window, text="Shift", variable=shiftCheck)
modifierBoxShift.grid(row=2, column=3, sticky=tk.E)

enableBindButton = tk.Button(window, text="Bind", command=recordKey2)
enableBindButton.grid(row=3, column=3, columnspan=1, sticky=tk.EW, padx=6)

enableBindLabel = tk.Label(window, text="Enable in-game:")
enableBindLabel.grid(row=3, column=2, sticky=tk.E, padx=4)

disableBindButton = tk.Button(window, text="Bind", command=recordKey3)
disableBindButton.grid(row=4, column=3, columnspan=1, sticky=tk.EW, padx=6)

disableBindLabel = tk.Label(window, text="Disable in-game:")
disableBindLabel.grid(row=4, column=2, sticky=tk.E, padx=4)

separator1 = ttk.Separator(window, orient="horizontal")
separator1.grid(row=1, column=2, columnspan=2, sticky="NEW")

separator2 = ttk.Separator(window, orient="horizontal")
separator2.grid(row=2, column=2, columnspan=2, sticky="SEW")

separator3 = ttk.Separator(window, orient="vertical")
separator3.grid(row=1, column=2, rowspan=2, sticky="NSW")

separator4 = ttk.Separator(window, orient="vertical")
separator4.grid(row=1, column=3, rowspan=2, sticky="NSE")

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

configData = [gameDir.get(), dpiEntry.get(), minSensEntry.get(), maxSensEntry.get(), updateBindModifiers(), enableBindButton.cget("text"), disableBindButton.cget("text")]

sensLogTxt = "sensitivity_log.txt"
liveSensTxt = "current_sensitivity.txt"

def save_configuration():
    reloadData()
    if float(max_sensitivity) > float(min_sensitivity):
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
        
        print("Configuration saved successfully!", directory, dpi, min_sensitivity, max_sensitivity)
    else:
        print("Max sensitivity needs to be greater than min sensitivity!")

saveButton = tk.Button(window, text="Save settings", command=save_configuration)
saveButton.grid(row=5, column=2, columnspan=1, pady=18, ipady=6, sticky=tk.EW)

window.mainloop()