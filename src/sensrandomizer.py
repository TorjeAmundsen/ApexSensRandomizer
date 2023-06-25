# Made by Torje Amundsen
import sys
import random
import os
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox
from gui import Ui_MainWindow as QtGUI
import datetime
import base64
from config import Config
import vdf
import winreg
import threading
import time
import keyboard
import requests
import webbrowser

def main():
    def check_for_updates(release, ui, window):
        owner = "TorjeAmundsen"
        repo = "ApexSensRandomizer"
        response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/releases/latest")
        response_json = response.json()
        tag = response_json.get("tag_name", "")
        assets = response_json.get("assets")
        download = assets[0]["browser_download_url"]
        if response.status_code == 200:
            if tag not in [release, config.skipped_update_tag]:
                # [f"Download {release_tag}", "Show Changelog", "Remind Me Later", "Don't Ask Again"]
                print("placeholder for showing a new update is available")
                update = QMessageBox(window)
                update.setWindowTitle("Update")
                update.setText("A new update is available for ApexSensRandomizer!")
                update.setInformativeText(f"Your current version: {release_tag}\nLatest release: {tag}\n")
                update.setPalette(ui.palette)
                update_button = update.addButton("Download", QMessageBox.ButtonRole.YesRole)
                update_button.clicked.connect(lambda: open_site(download))
                changelog_button = update.addButton("Show Changelog", QMessageBox.ButtonRole.YesRole)
                changelog_button.clicked.disconnect()
                changelog_button.clicked.connect(lambda: open_site(f"https://www.github.com/{owner}/{repo}/releases/latest"))
                skip_update_button = update.addButton("Skip Version", QMessageBox.ButtonRole.YesRole)
                skip_update_button.clicked.connect(lambda: skip_update(tag))
                update.addButton("Update Later", QMessageBox.ButtonRole.NoRole)
                update.exec()
    def open_site(url):
        webbrowser.open_new_tab(url)
    
    def skip_update(tag):
        config.skipped_update_tag = tag
        config.save(ui)

    def toggle():
        ui.running = not ui.running
        ui.startRandomizerButton.setText(running_text[ui.running])
        for i in disabled_while_running:
            if i != ui.outputLabel and i != ui.startRandomizerButton:
                i.setEnabled(not ui.running)
        now = datetime.datetime.now()
        sensLog = open(sens_log_txt, "a")
        sensLog.write(f"\n[{now.strftime('%Y-%m-%d %H:%M:%S] ')}{start_stop_log[ui.running]}")
    def start_randomizer():
        generate_autoexec()
        if os.path.isfile(ui.gameDirectoryField.text() + "/cfg/enablerando.cfg"):
            toggle()
            if ui.running:
                    keyboard.add_hotkey(config.update_bind_modifiers(ui.randomizeBindButton.text(), ui), randomize)
                    ui.outputLabel.setText(f"Press {config.update_bind_modifiers(ui.randomizeBindButton.text(), ui)}")
                    if ui.timerCheckbox.isChecked():
                        startThreadedFunction(timerLoop, ui.timeSpinbox.value())
            else:
                ui.outputLabel.setText(f"Not running")
                reset_sensitivity()
                keyboard.remove_all_hotkeys()
                event.clear()

    def browse_directory():
        browse = QFileDialog.getExistingDirectory(
            None,
            "Select Apex Legends Directory",
            sens_randomizer_directory,
        )
        
        if browse:
            ui.gameDirectoryField.setText(f"{browse}/")

    def findSteamDirectory():
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, R"SOFTWARE\WOW6432Node\Valve\Steam")
        path = winreg.QueryValueEx(key, "InstallPath")
        return path[0]

    def apexLibraryPath(id):
        folders = vdf.load(open(rf"{findSteamDirectory()}\steamapps\libraryfolders.vdf"))
        vdfstring = folders.get("libraryfolders")

        for i in vdfstring.values():
            current_path = i.get("path")
            for j in i.get("apps").keys():
                if j == id:
                    return current_path

    def auto_detect_directory():
        appmanifestpath = rf"{apexLibraryPath(apexID)}\steamapps\appmanifest_{apexID}.acf"
        appmanifest = vdf.load(open(appmanifestpath))
        for i in appmanifest.values():
            print("Path detected: ", rf"{apexLibraryPath(apexID)}\steamapps\common\{i.get('installdir')}")
            ui.gameDirectoryField.setText(rf"{apexLibraryPath(apexID)}\steamapps\common\{i.get('installdir')}")
    
    def startThreadedFunction(function, args, button=False):
        if button:
            for i in disabled_while_running:
                if i != args:
                    i.setEnabled(False)
            args.setText("Press a key...")
        newThread = threading.Thread(target=function, args=(args,))
        newThread.daemon = True
        newThread.start()

    def timerLoop(delay):
        event.set()
        timer = 0
        randomize()
        while event.is_set():
            timer += 1
            if timer == delay*10:
                randomize()
                timer = 0
            time.sleep(0.1)

    def recordKey(bind):
        k = keyboard.read_key()
        if (k.isalnum() and not len(k) > 1 or k.startswith("f")):
                k = str(k).upper()
                bind.setText(k)
        else:
            bind.setText("Invalid key!")
        bind.setChecked(False)
        for i in disabled_while_running:
            i.setEnabled(True)
    def randomize():
        min_float = float(ui.minSensSpinbox.value())
        max_float = float(ui.maxSensSpinbox.value())
        init_RNG = random.uniform(min_float, max_float)
        sens_num_actual = round(init_RNG, 2)
        floatSens = float(sens_num_actual)

        cmRev = str(round((360 / (0.022 * int(ui.dpiSelector.currentText()) * floatSens)) * 2.54, 1))

        formattedSens = cmRev + "cm/360 (" + f"{floatSens:.2f}" + " @ " + str(ui.dpiSelector.currentText()) + " DPI)"

        now = datetime.datetime.now()
        sensLog = open(sens_log_txt, "a")
        sensLog.write("\n[" + now.strftime("%Y-%m-%d %H:%M:%S] ") + formattedSens)

        liveSens = open(live_sens_txt, "w")
        liveSens.write(formattedSens)

        randomsens = open(ui.gameDirectoryField.text() + "/cfg/randomsens.cfg", "w")
        randomsens.write("mouse_sensitivity " + f"{floatSens:.2f}")

        ui.outputLabel.setText(formattedSens)

    def generate_autoexec():
        config.save(ui)
        enableStr = f"""#Automatically generated by Apex Sens Randomizer

bind \"w\" \"+forward; exec randomsens\"
bind \"s\" \"+backward; exec randomsens\"
bind \"a\" \"+moveleft; exec randomsens\"
bind \"d\" \"+moveright; exec randomsens\"
bind \"{ui.disableBindButton.text()}\" \"exec disablerando; exec autoexec\""""
        disableStr = f"""#Automatically generated by Apex Sens Randomizer

unbind \"w\"
unbind \"s\"
unbind \"a\"
unbind \"d\"
bind \"w\" \"+forward\"
bind \"s\" \"+backward\"
bind \"a\" \"+moveleft\"
bind \"d\" \"+moveright\"
bind \"{ui.enableBindButton.text()}\" \"exec enablerando\"
mouse_sensitivity {ui.defaultSensSpinbox.value()}"""

        autoexecStr = f"#Automatically generated by Apex Sens Randomizer\n\nbind \"{ui.enableBindButton.text()}\" \"exec enablerando\""
        try:
            enableRando = open(ui.gameDirectoryField.text() + "/cfg/enablerando.cfg", "w")
            enableRando.write(enableStr)
        except FileNotFoundError:
            ui.startRandomizerButton.setText("Incorrect game path!")
            ui.startRandomizerButton.setEnabled(False)
            return
        
        try:
            disableRando = open(ui.gameDirectoryField.text() + "/cfg/disablerando.cfg", "w")
            disableRando.write(disableStr)
        except FileNotFoundError:
            pass

        try:
            with open(ui.gameDirectoryField.text() + "/cfg/autoexec.cfg", 'r+') as autoexec:
                lines = autoexec.readlines()
                line_number = None
                for i, line in enumerate(lines):
                    if "enablerando" in line:
                        line_number = i
                        break
                if line_number is not None:
                    lines[line_number] = f"bind \"{ui.enableBindButton.text()}\" \"exec enablerando\"\n"
                with open(ui.gameDirectoryField.text() + "/cfg/autoexec.cfg", 'w') as autoexec:
                    autoexec.writelines(lines)
        except FileNotFoundError:
            with open(rf"{ui.gameDirectoryField.text()}/cfg/autoexec.cfg", 'x') as autoexec:
                autoexec.write(autoexecStr)
        finally:
            ui.startRandomizerButton.setText("Start Randomizer")
            ui.startRandomizerButton.setEnabled(True)
    
    def reset_sensitivity():
        randomsens = open(ui.gameDirectoryField.text() + "/cfg/randomsens.cfg", "w")
        randomsens.write(f"mouse_sensitivity {ui.defaultSensSpinbox.value()}")

    
    FROZEN = hasattr(sys, "frozen")
    sens_randomizer_directory = os.path.dirname(sys.executable if FROZEN else os.path.abspath(__file__))

    live_sens_txt = f"{sens_randomizer_directory}/config/current_sensitivity.txt"
    sens_log_txt = f"{sens_randomizer_directory}/config/sensitivity_log.txt"

    ui = QtGUI()
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui.setupUi(MainWindow)

    iconString = """AAABAAMAEBAAAAEABAAoAQAANgAAABgYAAABAAQA6AEAAF4BAAAgIAAAAQAEAOgCAABGAwAAKAAA
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
    icondata = base64.b64decode(iconString)
    temp_file = "icon.ico"
    icon_file = open(temp_file, "wb")
    icon_file.write(icondata)
    icon_file.close()

    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(temp_file), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
    MainWindow.setWindowIcon(icon)
    os.remove(temp_file)

    apexID = "1172470"
    release_tag = "v1.1.0"
    event = threading.Event()
    running_text = ["Start Randomizer", "Stop Randomizer"]
    start_stop_log = ["Randomizer stopped!\n", "Randomizer started!"]
    
    disabled_while_running = [ui.gameDirectoryField,  ui.dpiSelector,        ui.autoDetectButton,
                              ui.browseButton,        ui.defaultSensSpinbox, ui.minSensSpinbox,
                              ui.maxSensSpinbox,      ui.saveSettingsButton, ui.enableBindButton,
                              ui.disableBindButton,   ui.timerCheckbox,      ui.timeSpinbox,
                              ui.randomizeBindButton, ui.outputLabel,        ui.ctrlCheck,
                              ui.altCheck,            ui.shiftCheck,         ui.startRandomizerButton]
    
    ui.dpiSelector.setCurrentIndex(1)
    config = Config(sens_randomizer_directory)
    config.load(ui)
    QApplication.setStyle("fusion")
    ui.running = False
    ui.startRandomizerButton.clicked.connect(start_randomizer)
    ui.browseButton.clicked.connect(browse_directory)
    ui.autoDetectButton.clicked.connect(auto_detect_directory)
    ui.saveSettingsButton.clicked.connect(generate_autoexec)
    ui.randomizeBindButton.clicked.connect(lambda: startThreadedFunction(recordKey, ui.randomizeBindButton, True))
    ui.enableBindButton.clicked.connect(lambda: startThreadedFunction(recordKey, ui.enableBindButton, True))
    ui.disableBindButton.clicked.connect(lambda: startThreadedFunction(recordKey, ui.disableBindButton, True))
    MainWindow.setWindowTitle(f"Apex Sensitivity Randomizer {release_tag}")
    print(sens_randomizer_directory)
    MainWindow.show()
    if not config.update_checked:
        check_for_updates(release_tag, ui, MainWindow)
    
    sys.exit(app.exec())
    


if __name__ == "__main__":
    main()