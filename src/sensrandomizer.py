"""
Apex Sensitivity Randomizer v1.1.0
Torje K. Amundsen 2023
Main module
"""

import sys
from random import uniform as uniform_random
from os import path
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox
from gui import Ui_MainWindow as QtGUI
from datetime import datetime
from config import Config
from vdf import load as vdfload
from winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE
from threading import Event, Thread
from time import sleep
from keyboard import add_hotkey, read_key, remove_all_hotkeys
from requests import get as request
from webbrowser import open_new_tab
from ctypes import windll

def main():
    """ Main function. """

    def check_for_updates(release, ui, window):
        """
        Checks for updates, pops up a window with relevant links if a
        newer update than the current tag is found.
        """
        owner = "TorjeAmundsen"
        repo = "ApexSensRandomizer"
        response = request(f"https://api.github.com/repos/{owner}/{repo}/releases/latest",
                           timeout=10)
        response_json = response.json()
        tag = response_json.get("tag_name", "")
        assets = response_json.get("assets")
        download = assets[0]["browser_download_url"]
        if response.status_code == 200:
            if tag not in [release, config.skipped_update_tag]:
                update = QMessageBox(window)
                update.setWindowTitle("Update")
                update.setText("A new update is available for ApexSensRandomizer!")
                update.setInformativeText(
                    f"Your current version: {release_tag}\nLatest release: {tag}\n")
                update.setPalette(ui.palette)
                update_button = update.addButton("Download", QMessageBox.ButtonRole.YesRole)
                update_button.clicked.connect(lambda: open_site(download))
                changelog_button = update.addButton("Changelog", QMessageBox.ButtonRole.YesRole)
                changelog_button.clicked.disconnect()
                changelog_button.clicked.connect(
                    lambda: open_site(f"https://www.github.com/{owner}/{repo}/releases/latest"))
                skip_update_button = update.addButton(
                    "Skip Version", QMessageBox.ButtonRole.YesRole)
                skip_update_button.clicked.connect(
                    lambda: skip_update(tag))
                update.addButton("Not Now", QMessageBox.ButtonRole.NoRole)
                update.exec()


    def open_site(url):
        open_new_tab(url)


    def skip_update(tag):
        """
        Sets a flag in your config file to not pop up the update window
        on launch until next release if the user choose so.
        """
        config.skipped_update_tag = tag
        config.save(ui)


    def toggle():
        """
        Toggles the main "running" bool, as well as
        disabling/re-enabling the GUI, using the running bool as an
        index for lists containing the relevant text to update.
        """
        ui.running = not ui.running
        ui.startRandomizerButton.setText(running_text[ui.running])
        for i in disabled_while_running:
            if i not in (ui.outputLabel, ui.startRandomizerButton):
                i.setEnabled(not ui.running)
        now = datetime.now()
        sens_log = open(sens_log_txt, "a", encoding="UTF-8")
        sens_log.write(f"\n[{now.strftime('%Y-%m-%d %H:%M:%S] ')}{start_stop_log[ui.running]}")
        if not ui.running:
            try: # Resets your randomsens.cfg to your default sensitivity
                randomsens = open(ui.gameDirectoryField.text() + "/cfg/randomsens.cfg", "w")
                randomsens.write(f"mouse_sensitivity {ui.defaultSensSpinbox.value()}")
            except FileNotFoundError:
                pass


    def start_randomizer():
        """ Main "Start Randomizer" function. The big button. """
        generate_autoexec()
        if path.isfile(ui.gameDirectoryField.text() + "/cfg/enablerando.cfg"):
            toggle()
            if ui.running:
                add_hotkey(config.update_bind_modifiers(ui.randomizeBindButton.text(), ui),
                           randomize)
                ui.outputLabel.setText(
                    f"Press {config.update_bind_modifiers(ui.randomizeBindButton.text(), ui)}")
                if ui.timerCheckbox.isChecked():
                    startThreadedFunction(timerLoop, ui.timeSpinbox.value())
            else:
                ui.outputLabel.setText(f"Not running")
                remove_all_hotkeys()
                event.clear()


    def browse_directory():
        browse = QFileDialog.getExistingDirectory(
            None,
            "Select Apex Legends Directory",
            sens_randomizer_directory,)
        if browse:
            ui.gameDirectoryField.setText(f"{browse}/")


    def find_steam_directory():
        """
        Returns your main Steam installation folder by looking through
        the user's Windows Registry.
        """
        key = OpenKey(HKEY_LOCAL_MACHINE, R"SOFTWARE\WOW6432Node\Valve\Steam")
        path = QueryValueEx(key, "InstallPath")
        return path[0]


    def apex_library_path(id):
        """
        Parses libraryfolders.vdf from your Steam directory in order to
        find out which Steam library contains Apex Legends. Required in
        case the user has multiple game libraries.
        """
        folders = vdfload(open(rf"{find_steam_directory()}\steamapps\libraryfolders.vdf"))
        vdfstring = folders.get("libraryfolders")


        for i in vdfstring.values():
            current_path = i.get("path")
            for j in i.get("apps").keys():
                if j == id:
                    return current_path


    def auto_detect_directory():
        """
        Parses the appmanifest file for Apex Legends, in case the user
        for some strange reason has installed Apex Legends in a folder
        that is renamed to something other than the default.
        """
        appmanifestpath = rf"{apex_library_path(apexID)}\steamapps\appmanifest_{apexID}.acf"
        appmanifest = vdfload(open(appmanifestpath))
        for i in appmanifest.values():
            print("Path detected: ",
                  rf"{apex_library_path(apexID)}\steamapps\common\{i.get('installdir')}")
            ui.gameDirectoryField.setText(
                rf"{apex_library_path(apexID)}\steamapps\common\{i.get('installdir')}")


    def startThreadedFunction(function, args, button=False):
        """
        Starts a threaded function. Used to run the timer if the user
        has it enabled, and also runs the key listeners on a separate
        thread in order to not freeze the program until a key is
        pressed.
        Has specific functionality for the bind buttons to disable the
        rest of the GUI while the program is listening for a keypress.
        Not doing this threaded cases a crash if the user tries to do
        anything other than press a key after starting the listener.
        """
        if button:
            for i in disabled_while_running:
                if i != args:
                    i.setEnabled(False)
            args.setText("Press a key...")
        newThread = Thread(target=function, args=(args,))
        newThread.daemon = True
        newThread.start()


    def timerLoop(delay):
        """
        Timer loop for the main randomizer functionality.
        I had to set the sleep amount to a very low amount in order to
        prevent the user from starting multiple timer threads by
        spamming the "Start Randomizer" button. You can technically
        still do this, but you need to spam the button at > 10Hz.
        """
        event.set()
        timer = 0
        randomize()
        while event.is_set():
            timer += 1
            if timer == delay*10:
                randomize()
                timer = 0
            sleep(0.1)


    def recordKey(bind):
        """ Listens for a keypress, and filters out invalid keys. """
        k = read_key()
        if (k.isalnum() and not len(k) > 1 or k.startswith("f")):
            k = str(k).upper()
            bind.setText(k)
        else:
            bind.setText("Invalid key!")
        bind.setChecked(False)
        for i in disabled_while_running:
            i.setEnabled(True)


    def randomize():
        """
        Main randomization function. Also handles writing to the
        relevant log files and randomsens.cfg.
        Converts your sensitivity to cm/360 for logging/output.
        """
        min_float = float(ui.minSensSpinbox.value())
        max_float = float(ui.maxSensSpinbox.value())
        init_RNG = uniform_random(min_float, max_float)
        sens_num_actual = round(init_RNG, 2)
        floatSens = float(sens_num_actual)

        cmRev = str(round((360/(0.022*int(ui.dpiSelector.currentText())*floatSens))*2.54, 1))

        formattedSens = f"{cmRev}cm/360 ({floatSens:.2f} @ {ui.dpiSelector.currentText()} DPI)"

        now = datetime.now()
        sensLog = open(sens_log_txt, "a")
        sensLog.write("\n[" + now.strftime("%Y-%m-%d %H:%M:%S] ") + formattedSens)

        liveSens = open(live_sens_txt, "w")
        liveSens.write(formattedSens)

        randomsens = open(ui.gameDirectoryField.text() + "/cfg/randomsens.cfg", "w")
        randomsens.write("mouse_sensitivity " + f"{floatSens:.2f}")

        ui.outputLabel.setText(formattedSens)


    """
    The "Save Settings" button. Calls the function to save config.json.
    Generates autoexec.cfg, enablerando.cfg, and disablerando.cfg if your game
    directory is valid.
    Will parse your autoexec.cfg file if it already exists, and either edit
    the existing line containing the "exec enablerando" bind to update it, or
    simply append the file if it exists but doesn't contain that command.
    """
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

        autoexecStr = "#Automatically generated by Apex Sens Randomizer\n\n"+\
            f"bind \"{ui.enableBindButton.text()}\" \"exec enablerando\""
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
                index = None
                for i, line in enumerate(lines):
                    if "enablerando" in line:
                        index = i
                        break
                if index is not None:
                    lines[index] = f"bind \"{ui.enableBindButton.text()}\" \"exec enablerando\"\n"
                with open(ui.gameDirectoryField.text() + "/cfg/autoexec.cfg", 'w') as autoexec:
                    autoexec.writelines(lines)
        except FileNotFoundError:
            with open(rf"{ui.gameDirectoryField.text()}/cfg/autoexec.cfg", 'x') as autoexec:
                autoexec.write(autoexecStr)
        finally:
            ui.startRandomizerButton.setText("Start Randomizer")
            ui.startRandomizerButton.setEnabled(True)


    FROZEN = hasattr(sys, "frozen")
    sens_randomizer_directory = path.dirname(sys.executable if FROZEN else path.abspath(__file__))

    live_sens_txt = f"{sens_randomizer_directory}/config/current_sensitivity.txt"
    sens_log_txt = f"{sens_randomizer_directory}/config/sensitivity_log.txt"

    ui = QtGUI()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui.setupUi(MainWindow)

    base_dir = path.dirname(__file__)
    icon_file = path.join(base_dir, "randoicon.ico")
    icon = QtGui.QIcon(icon_file)
    MainWindow.setWindowIcon(icon)
    apexID = "1172470"
    release_tag = "v1.1.0"
    event = Event()
    running_text = ["Start Randomizer", "Stop Randomizer"]
    start_stop_log = ["Randomizer stopped!\n", "Randomizer started!"]

    disabled_while_running = [
        ui.gameDirectoryField,  ui.dpiSelector,        ui.autoDetectButton,
        ui.browseButton,        ui.defaultSensSpinbox, ui.minSensSpinbox,
        ui.maxSensSpinbox,      ui.saveSettingsButton, ui.enableBindButton,
        ui.disableBindButton,   ui.timerCheckbox,      ui.timeSpinbox,
        ui.randomizeBindButton, ui.outputLabel,        ui.ctrlCheck,
        ui.altCheck,            ui.shiftCheck,         ui.startRandomizerButton,
        ui.labelDirectory,      ui.labelDPI,           ui.labelDefault,
        ui.labelMin,            ui.labelMax,           ui.labelRandomize,
        ui.labelEnable,         ui.labelDisable]

    myappid = "ApexSensRandomizer.{release_tag}"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    ui.dpiSelector.setCurrentIndex(1)
    config = Config(sens_randomizer_directory)
    config.load(ui)
    QApplication.setStyle("fusion")
    ui.running = False
    ui.startRandomizerButton.clicked.connect(start_randomizer)
    ui.browseButton.clicked.connect(browse_directory)
    ui.autoDetectButton.clicked.connect(auto_detect_directory)
    ui.saveSettingsButton.clicked.connect(generate_autoexec)
    ui.randomizeBindButton.clicked.connect(
        lambda: startThreadedFunction(recordKey, ui.randomizeBindButton, True))
    ui.enableBindButton.clicked.connect(
        lambda: startThreadedFunction(recordKey, ui.enableBindButton, True))
    ui.disableBindButton.clicked.connect(
        lambda: startThreadedFunction(recordKey, ui.disableBindButton, True))
    MainWindow.setWindowTitle(f"Apex Sensitivity Randomizer {release_tag}")
    print(sens_randomizer_directory)
    MainWindow.show()
    if not config.update_checked:
        check_for_updates(release_tag, ui, MainWindow)

    sys.exit(app.exec())



if __name__ == "__main__":
    main()
