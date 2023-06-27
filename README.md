# ApexSensRandomizer v1.1.0 - [Download here!](https://github.com/TorjeAmundsen/ApexSensRandomizer/releases/latest)
A non-intrusive, customizable, autoexec/config based sensitivity randomizer for Apex Legends.


![ApexSensRandomizer GUI with the configuration filled out.](https://github.com/TorjeAmundsen/ApexSensRandomizer/assets/14235956/970bdf13-129b-455d-b70a-0036e12eef67)


## Display live-updating sensitivity in OBS!

The program will also output a log file `sensitivity_log.txt` containing every sensitivity the program has generated so far, as well as a formatted live view file `current_sensitivity.txt` that you can use in say a Text GDI+ source in OBS to show your current randomized sensitivity live in OBS. These files are generated in a `\config\` folder in the directory you are running `ApexSensRandomizer.exe` from.

![OBS screenshot showing how to add a Text source](https://github.com/TorjeAmundsen/ApexSensRandomizer/assets/14235956/174d3d0a-4c5b-4944-970d-2920158ebd08)

![Screenshot of the Text properties window showing how to set it to read from a file](https://github.com/TorjeAmundsen/ApexSensRandomizer/assets/14235956/37f97a94-452f-4196-93b9-5e02fc19f801)
![Explorer screenshot showing which file to set the Text source to read from in OBS](https://github.com/TorjeAmundsen/ApexSensRandomizer/assets/14235956/84db3527-7462-4484-a978-8426f5d9b71f)

# Support

If you're having any issues with the program, feel free to join my **[Discord server](https://discord.gg/doomjump)** and ask in the #support channel! You can also report bugs/request features here if you don't have a GitHub account. You can also reach out to me on **[Twitter @Txrje.](https://twitter.com/Txrje)**

To report a bug/issue, or to request a feature, open a new issue here: **[ApexSensRandomizer issues](https://github.com/TorjeAmundsen/ApexSensRandomizer/issues)**

# Instructions

Download `ApexSensRandomizer.exe` from Releases, and preferably put this program in its own folder, as the program will generate some config files/logs in the folder it gets ran from.


### Game directory & launch options

Press the `Auto-detect` button in the top right to attempt to automatically find your Apex Legends directory, or manually find your Apex Legends game directory through Steam by right clicking Apex Legends, going to Properties..., Local Files, Browse, and copy your game path (the base game directory, not any deeper folder) into the `Game directory` field (or browse to it with the `Browse...` button).

Example path from my system: `E:\SteamLibrary\steamapps\common\Apex Legends`

Add `+exec autoexec` to your launch options in the General tab of your properties, like this:

![Steam General properties with "+exec autoexec" typed into the launch options field.](https://github.com/TorjeAmundsen/ApexSensRandomizer/assets/14235956/d2632617-941c-4464-91a4-e3e9fe2a72b7)

You'll need this command in your launch options for the program to work.

### Mouse DPI

`Mouse DPI` is only used for calculating the formatted sensitivity output for displaying in programs like OBS, or the sensitivity log file. I have 4 preset values of 400, 800, 1600 and 3200 DPI, but you can also type in any DPI value you want here.

### Min/Max sensitivity

`Minimum sensitivity` and `Maximum sensitivity`  changes your sensitivity range by setting your preferred minimum and maximum in-game sensitivities that the program will randomize between. Something like 0.35 minimum and 2.00 maximum seems to work well for me at 1600 DPI, but tweak this to whatever you want.

### Default Sensitivity

`Default sensitivity` is just the sensitivity value your sensitivity will be set to when you disable the randomizer. Set this to whatever sensitivity  you normally play on for the program to return you to your original sensitivity when you disable the randomizer in-game. This value has no effect on the randomization itself.

### Randomize sens

`Randomize sensitivity` is the global hotkey for randomizing your sensitivty. This is the "main" purpose of the program, so make this one accessible. Bind it by clicking the `Set a bind...` button, and then pressing any alphanumeric key on your keyboard. The key you pressed should appear inside the button you pressed if you pressed a valid key.

Checking any combination the three `Ctrl`, `Alt` or `Shift` checkboxes will require those modifiers to be held at the same time as your `Randomize sensitivity` hotkey

### Timer

`Enable timer` lets you enable a timer for the program to automatically randomize your sensitivity every x seconds. This process is threaded, which means you can still use your `Randomize sens` hotkey on top of this, to manually randomize it whenever you want while the timer is running. Set the timer interval with the value to the right of the checkbox.

### Enable/Disable in-game

Do note that you need to be fully in-game (as in, you have control of your character) for these two binds to work. They will only work once you are in the dropship, mid-game, or in firing range (preferably for making sure it's working lol).

`Enable in-game` and `Disable in-game` are autoexec commands bound in-game by Apex Legends using your autoexec.cfg file. These can be set to the same key to effectively make the button a toggle. Bind it in the same way you bound `Randomize sens`. Pressing the `Enable in-game` keys effectively re-bind your WADS keys to execute `randomsens.cfg` whenever they are pressed, and my program updates `randomsens.cfg` with a `mouse_sensitivity x.xx` command to change your sensitivity every time you press your `Randomize sens` hotkey.

Press the `Disable in-game` bind to unbind `randomsens.cfg` from your WADS keys, returning them to normal and stoppig them from updating your sensitivity. You technically don't have to press this ever, as stopping the randomizer will set your sensitivity back to your default sensitivity. This will just completely unbind WASD from executing `randomsens.cfg`, which is needed if you want to change your sens away from your set default sens.

### Save settings & Start Randomizer

`Save settings` saves all the configurable fields above to `config.json`, which is generated in the same directory you are running `ApexSensRandomize.exe` from. This will also automatically generate (or append/edit the files if they already exist) the files `autoexec.cfg`, `enablerando.cfg`, and `disablerando.cfg` files in your `\Apex Legends\cfg\` folder. This is also automatically done when you press `Start Randomizer`, this just allows you to save your settings/generate the necessary config files without starting the randomizer.

`Start Randomizer` starts the loop that listens for your `Randomize sensitivity` bind, and also the timer if applicable. Once this is running, the program is fully functioning, and it is editing your config file `randomsens.cfg` containing the senstivity command every time you press `Randomize sensitivity`, and however often the timer is set to automatically randomize on top of that if enabled.
