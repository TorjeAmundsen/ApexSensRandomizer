# ApexSensRandomizer
A non intrusive, customizable, autoexec/config based sensitivity randomizer for Apex Legends.


![ApexSensRandomizer GUI with the configuration filled out.](https://github.com/TorjeAmundsen/ApexSensRandomizer/assets/14235956/351956d4-a5d4-4c33-ba45-7dd2d98d157a)![ApexSensRandomizer GUI while randomizing your sensitivity.](https://github.com/TorjeAmundsen/ApexSensRandomizer/assets/14235956/6b5fc6f9-c2a6-4ece-8d8a-dbda1d80b492)


# Instructions
Find your Apex Legends game directory through Steam by right clicking Apex Legends, going to Properties..., Local Files, Browse.

Example path from my system: `E:\SteamLibrary\steamapps\common\Apex Legends`

While you're here in properties, also add `+ exec autoexec` to your launch options in the General tab, like this:

![Steam General properties with "+exec autoexec" typed into the launch options field.](https://github.com/TorjeAmundsen/ApexSensRandomizer/assets/14235956/d2632617-941c-4464-91a4-e3e9fe2a72b7)

You'll need this command in your launch options for the program to work.

Copy your game path (the base game directory, not any deeper folder) into the `Game directory` field (or browse to it with the `Browse...` button).

`Mouse DPI` is only used for calculating the formatted sensitivity output for displaying in programs like OBS, or the sensitivity log file. I have 3 preset values of `400`, `800`, and `1600` DPI, but you can also type in any DPI value you want here.

`Min sensitivity` and `Max sensitivity`  changes your sensitivity range by setting your preferred minimum and maximum in-game sensitivities that the program will randomize between. Something like 0.35 minimum and 2.00 maximum seems to work well for me at 1600 DPI, but tweak this to whatever you want.

`Randomize sens` is the global hotkey for randomizing your sensitivty. This is the "main" purpose of the program, so make this one accessible. Bind it by clicking the `Bind` button, and then pressing any alphanumeric key on your keyboard. The key you pressed should appear inside the button you pressed if you pressed a valid key.

Checking any combination the three `Ctrl`, `Alt` or `Shift` checkboxes will require those modifiers to be held at the same time as your `Randomize sens` hotkey

`Enable in-game` and `Disable in-game` are autoexec commands bound in-game by Apex Legends using your autoexec.cfg file. Bind it the same way as `Randomize sens`. Pressing the `Enable in-game` keys effectively re-bind your WADS keys to execute `randomsens.cfg` whenever they are pressed, and my program updates `randomsens.cfg` with a `mouse_sensitivity x.xx` command to change your sensitivity every time you press your `Randomize sens` hotkey.

Press the `Disable in-game` bind to unbind `randomsens.cfg` from your WADS keys, returning them to normal and stoppig them from updating your sensitivity. Do note that you need to be fully in-game (as in, you have control of your character) for these two binds to work. They will only work once you are in the dropship, mid-game, or in firing range (preferably for making sure it's working lol).

`Save settings` saves all the configurable fields above to `config.json`, which is generated in the same directory you are running `ApexSensRandomize.exe` from. This file is also automatically saved when you press `Generate autoexec` or `Start Randomizer`.

`Generate autoexec` is important. This will automatically generate (or append/edit the files if they already exist) the files `autoexec.cfg`, `enablerando.cfg`, and `disablerando.cfg` files in your `\Apex Legends\cfg\` folder. Always press this after changing your binds/hotkeys, as this is necessary update the corresponding binds and commands in these files.

`Start Randomizer` starts the loop that listens for your `Randomize sens` bind. Once this is running, the program is fully functioning, and editing your config file containign the senstivity command every time you press `Randomize sens`. This will also output a log file `sensitivity_log.txt` containing every sensitivity the program has generated so far, as well as a formatted live view file `current_sensitivity.txt` that you can use in say a Text GDI+ source in OBS to show your current randomized sensitivity live in OBS. These files are generated in the same folder you are running `ApexSensRandomizer.exe` from.
