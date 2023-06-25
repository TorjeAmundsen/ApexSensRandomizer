import json
import os
import sys

class Config():
    update_checked: bool = False
    skipped_update_tag: str = ""
    theme: bool = 0
    invalid_binds = ["Set a bind...", "Invalid key!", "..."]
    FROZEN = hasattr(sys, "frozen")
    sens_randomizer_directory = os.path.dirname(sys.executable if FROZEN else os.path.abspath(__file__))

    def __init__(self, directory):
        self.directory = f"{directory}/config/config.json"
        if not os.path.exists(f"{directory}/config"):
            os.makedirs(f"{directory}/config")
        
    def update_bind_modifiers(self, string, ui):
        combinedBind = string
        if ui.shiftCheck.isChecked():
            combinedBind = "Shift + " + combinedBind
        if ui.altCheck.isChecked():
            combinedBind = "Alt + " + combinedBind
        if ui.ctrlCheck.isChecked():
            combinedBind = "Ctrl + " + combinedBind
        return combinedBind
    
    def save(self, ui):
        ui.dpiSelector.setCurrentText(ui.dpiSelector.currentText() or "800")
        if ui.randomizeBindButton.text() in self.invalid_binds:
            ui.randomizeBindButton.setText("X")
        if ui.enableBindButton.text() in self.invalid_binds:
            ui.enableBindButton.setText("F6")
        if ui.disableBindButton.text() in self.invalid_binds:
            ui.disableBindButton.setText("F7")
        configuration = {
            "directory": ui.gameDirectoryField.text(),
            "dpi": ui.dpiSelector.currentText(),
            "min_sensitivity": ui.minSensSpinbox.value(),
            "max_sensitivity": ui.maxSensSpinbox.value(),
            "base_sensitivity": ui.defaultSensSpinbox.value(),
            "randomize_bind": ui.randomizeBindButton.text(),
            "randomize_bind_modifiers": [ui.ctrlCheck.isChecked(), ui.altCheck.isChecked(), ui.shiftCheck.isChecked()],
            "timer": [ui.timerCheckbox.isChecked(), ui.timeSpinbox.value()],
            "enable_bind": ui.enableBindButton.text(),
            "disable_bind": ui.disableBindButton.text(),
            "theme": self.theme,
            "update_checked": self.update_checked,
            "skipped_update_tag": self.skipped_update_tag
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
                ui.ctrlCheck.setChecked(configuration.get("randomize_bind_modifiers")[0])
                ui.altCheck.setChecked(configuration.get("randomize_bind_modifiers")[1])
                ui.shiftCheck.setChecked(configuration.get("randomize_bind_modifiers")[2])
                ui.timerCheckbox.setChecked(configuration.get("timer")[0])
                ui.timeSpinbox.setValue(configuration.get("timer")[1])
                ui.enableBindButton.setText(configuration.get("enable_bind", "Set a bind..."))
                ui.disableBindButton.setText(configuration.get("disable_bind", "Set a bind..."))
                self.theme = configuration.get("theme", 0)
                self.update_checked = configuration.get("update_checked", False)
                self.skipped_update_tag = configuration.get("skipped_update_tag", "")
            
            print("Configuration loaded successfully")
        except FileNotFoundError:
            print("No configuration file found")