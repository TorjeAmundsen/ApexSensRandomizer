import json
import os
import sys
from PyQt6.QtGui import QKeySequence

class Config():

    theme: bool = 0
    FROZEN = hasattr(sys, "frozen")
    sens_randomizer_directory = os.path.dirname(sys.executable if FROZEN else os.path.abspath(__file__))

    def __init__(self, directory):
        self.directory = f"{directory}/config/config.json"
        if not os.path.exists(f"{directory}/config"):
            os.makedirs(f"{directory}/config")
        
    """ def keysequence_to_string(self, sequence):
        key_sequence = sequence.keySequence()
        return key_sequence.toString()
    
    def string_to_keysequence(self, sequence_string):
        key_sequence = QKeySequence.fromString(sequence_string)
        return key_sequence """
    
    def save(self, ui):
        ui.dpiSelector.setCurrentText(ui.dpiSelector.currentText() or "800")
        if ui.randomizeBindButton.text() in ["Set a bind...", "Invalid key!", "..."]:
            ui.randomizeBindButton.setText("Alt+X")
        if ui.enableBindButton.text() in ["Set a bind...", "Invalid key!", "..."]:
            ui.enableBindButton.setText("F6")
        if ui.disableBindButton.text() in ["Set a bind...", "Invalid key!", "..."]:
            ui.disableBindButton.setText("F7")
        configuration = {
            "directory": ui.gameDirectoryField.text(),
            "dpi": ui.dpiSelector.currentText(),
            "min_sensitivity": ui.minSensSpinbox.value(),
            "max_sensitivity": ui.maxSensSpinbox.value(),
            "base_sensitivity": ui.defaultSensSpinbox.value(),
            "randomize_bind": ui.randomizeBindButton.text(),
            "timer": [ui.timerCheckbox.isChecked(), ui.timeSpinbox.value()],
            "enable_bind": ui.enableBindButton.text(),
            "disable_bind": ui.disableBindButton.text(),
            "theme": self.theme
        }

        with open(self.directory, "w") as config_file:
            json.dump(configuration, config_file, indent=4)

    def load(self, ui):
        try:
            with open(self.directory, "r") as config_file:
                configuration = json.load(config_file)
                
                ui.gameDirectoryField.setText(configuration.get("directory", ""))
                ui.dpiSelector.setCurrentText(configuration.get("dpi", 800))
                ui.minSensSpinbox.setValue(configuration.get("min_sensitivity", 0.7))
                ui.maxSensSpinbox.setValue(configuration.get("max_sensitivity", 3.8))
                ui.defaultSensSpinbox.setValue(configuration.get("base_sensitivity", 1.5))
                ui.randomizeBindButton.setText(configuration.get("randomize_bind", "Set a bind..."))
                ui.timerCheckbox.setChecked(configuration.get("timer")[0])
                ui.timeSpinbox.setValue(configuration.get("timer")[1])
                ui.enableBindButton.setText(configuration.get("enable_bind", "Set a bind..."))
                ui.disableBindButton.setText(configuration.get("disable_bind", "Set a bind..."))
                self.theme = (configuration.get("theme", 0))
            
            print("Configuration loaded successfully")
        except FileNotFoundError:
            print("No configuration file found")