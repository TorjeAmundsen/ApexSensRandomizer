import sys
import random
import os
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QFileDialog
from gui import Ui_MainWindow as QtGUI
import datetime
from config import Config
import vdf
import winreg

def main():

    def start_randomizer():
        print(ui.gameDirectoryField.text())

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

    FROZEN = hasattr(sys, "frozen")
    live_sens_txt = "/config/current_sensitivity.txt"
    sens_log_txt = "/config/sensitivity_log.txt"
    sens_randomizer_directory = os.path.dirname(sys.executable if FROZEN else os.path.abspath(__file__))
    apexID = "1172470"
    releaseTag = "v1.0.1"
    config = Config(sens_randomizer_directory)
    QApplication.setStyle("fusion")
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = QtGUI()
    ui.setupUi(MainWindow)

    ui.startRandomizerButton.clicked.connect(start_randomizer)
    ui.browseButton.clicked.connect(browse_directory)
    ui.autoDetectButton.clicked.connect(auto_detect_directory)
    ui.saveSettingsButton.clicked.connect(config.save())
    
    print(sens_randomizer_directory)
    MainWindow.show()
    
    sys.exit(app.exec())
    


if __name__ == "__main__":
    main()