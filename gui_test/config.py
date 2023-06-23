import json
import os
import sys
import PySide6
from PyQt6.QtGui import QKeySequence

class Config():
    theme: bool = 0
    FROZEN = hasattr(sys, "frozen")
    sens_randomizer_directory = os.path.dirname(sys.executable if FROZEN else os.path.abspath(__file__))
    def __init__(self, directory):
        self.directory = f"{directory}/config/config.json"
        if not os.path.exists(f"{directory}/config"):
            os.makedirs(f"{directory}/config")
        
    def keysequence_to_string(self, sequence):
        key_sequence = sequence.keySequence()
        return key_sequence.toString()
    
    def save(self, ui):
        """ try:
            if ui.timeSpinbox.value() < 1:
                ui.timeSpinbox.setValue(1)
        except:
            ui.timeSpinbox.setValue(10)

        ui.dpiSelector.setCurrentText(ui.dpiSelector.currentText() or "800")
        ui.minSensSpinbox.setValue(ui.minSensSpinbox.value())
        ui.maxSensSpinbox.setValue(ui.maxSensSpinbox.value())
        ui.defaultSensSpinbox.set(ui.defaultSensSpinbox.value())
        if ui.randomizeBindField. == "Bind" or randomizeBind.get() == "Invalid" or randomizeBind.get() == "...":
            randomizeBind.set("x")
            if not any([ctrlCheck.get(), altCheck.get(), shiftCheck.get()]):
                altCheck.set(True)
        if enableBind.get() == "Bind" or enableBind.get() == "Invalid":
            enableBind.set("F6")
        if disableBind.get() == "Bind" or disableBind.get() == "Invalid":
            disableBind.set("F7")
        if float(maxSens.get()) < float(minSens.get()):
            maxSens.set(str(float(minSens.get()) + 1)) """

        configuration = {
            "directory": ui.gameDirectoryField.text(),
            "dpi": ui.dpiSelector.currentText(),
            "min_sensitivity": ui.minSensSpinbox.value(),
            "max_sensitivity": ui.maxSensSpinbox.value(),
            "base_sensitivity": ui.defaultSensSpinbox.value(),
            "randomize_bind": self.keysequence_to_string(ui.randomizeBindField),
            "timer": [ui.timerCheckbox.isChecked(), ui.timeSpinbox.value()],
            "enable_bind": self.keysequence_to_string(ui.enableBindField),
            "disable_bind": self.keysequence_to_string(ui.disableBindField),
            "theme": self.theme
        }

        with open(self.directory, "w") as config_file:
            json.dump(configuration, config_file, indent=4)