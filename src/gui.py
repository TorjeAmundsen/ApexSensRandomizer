# Form implementation generated from reading ui file 'randomizer_gui.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(524, 322)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(524, 322))
        MainWindow.setMaximumSize(QtCore.QSize(524, 346))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(35, 35, 35))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(52, 52, 52))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(43, 43, 43))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(12, 12, 12))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(33, 33, 33))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(18, 18, 18))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(35, 35, 35))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(16, 16, 16))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(20, 20, 20))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 127))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(35, 35, 35))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(52, 52, 52))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(43, 43, 43))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(12, 12, 12))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(33, 33, 33))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(18, 18, 18))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(35, 35, 35))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(16, 16, 16))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(20, 20, 20))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 127))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(194, 194, 194))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(44, 44, 44))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(52, 52, 52))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(43, 43, 43))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(12, 12, 12))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(33, 33, 33))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(194, 194, 194))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(194, 194, 194))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(35, 35, 35))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(35, 35, 35))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(16, 16, 16))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(20, 20, 20))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(17, 17, 17, 127))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.PlaceholderText, brush)
        MainWindow.setPalette(palette)
        MainWindow.setAcceptDrops(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../randoicon.ico"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.Language.English, QtCore.QLocale.Country.UnitedStates))
        MainWindow.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setLocale(QtCore.QLocale(QtCore.QLocale.Language.English, QtCore.QLocale.Country.UnitedStates))
        self.centralwidget.setObjectName("centralwidget")
        self.gameDirectoryField = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.gameDirectoryField.setGeometry(QtCore.QRect(140, 10, 211, 22))
        self.gameDirectoryField.setObjectName("gameDirectoryField")
        self.dpiSelector = QtWidgets.QComboBox(parent=self.centralwidget)
        self.dpiSelector.setGeometry(QtCore.QRect(140, 50, 111, 22))
        self.dpiSelector.setAcceptDrops(False)
        self.dpiSelector.setAutoFillBackground(False)
        self.dpiSelector.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhDigitsOnly)
        self.dpiSelector.setEditable(True)
        self.dpiSelector.setMaxCount(32000)
        self.dpiSelector.setPlaceholderText("")
        self.dpiSelector.setFrame(True)
        self.dpiSelector.setObjectName("dpiSelector")
        self.dpiSelector.addItem("")
        self.dpiSelector.addItem("")
        self.dpiSelector.addItem("")
        self.dpiSelector.addItem("")
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 10, 91, 21))
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label.setObjectName("label")
        self.defaultSensSpinbox = QtWidgets.QDoubleSpinBox(parent=self.centralwidget)
        self.defaultSensSpinbox.setGeometry(QtCore.QRect(140, 90, 111, 22))
        self.defaultSensSpinbox.setSingleStep(0.05)
        self.defaultSensSpinbox.setProperty("value", 1.5)
        self.defaultSensSpinbox.setObjectName("defaultSensSpinbox")
        self.minSensSpinbox = QtWidgets.QDoubleSpinBox(parent=self.centralwidget)
        self.minSensSpinbox.setGeometry(QtCore.QRect(140, 130, 111, 22))
        self.minSensSpinbox.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.minSensSpinbox.setMinimum(0.01)
        self.minSensSpinbox.setSingleStep(0.05)
        self.minSensSpinbox.setProperty("value", 0.7)
        self.minSensSpinbox.setObjectName("minSensSpinbox")
        self.maxSensSpinbox = QtWidgets.QDoubleSpinBox(parent=self.centralwidget)
        self.maxSensSpinbox.setGeometry(QtCore.QRect(140, 170, 111, 22))
        self.maxSensSpinbox.setMinimum(0.02)
        self.maxSensSpinbox.setSingleStep(0.05)
        self.maxSensSpinbox.setProperty("value", 3.8)
        self.maxSensSpinbox.setObjectName("maxSensSpinbox")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 50, 91, 21))
        font = QtGui.QFont()
        font.setBold(False)
        self.label_2.setFont(font)
        self.label_2.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_2.setLocale(QtCore.QLocale(QtCore.QLocale.Language.English, QtCore.QLocale.Country.UnitedStates))
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 90, 101, 21))
        font = QtGui.QFont()
        font.setBold(False)
        self.label_3.setFont(font)
        self.label_3.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_3.setLocale(QtCore.QLocale(QtCore.QLocale.Language.English, QtCore.QLocale.Country.UnitedStates))
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 130, 111, 21))
        font = QtGui.QFont()
        font.setBold(False)
        self.label_4.setFont(font)
        self.label_4.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_4.setLocale(QtCore.QLocale(QtCore.QLocale.Language.English, QtCore.QLocale.Country.UnitedStates))
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 170, 111, 21))
        font = QtGui.QFont()
        font.setBold(False)
        self.label_5.setFont(font)
        self.label_5.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_5.setLocale(QtCore.QLocale(QtCore.QLocale.Language.English, QtCore.QLocale.Country.UnitedStates))
        self.label_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.startRandomizerButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.startRandomizerButton.setGeometry(QtCore.QRect(10, 255, 241, 51))
        self.startRandomizerButton.setAcceptDrops(False)
        self.startRandomizerButton.setStyleSheet("")
        self.startRandomizerButton.setAutoDefault(False)
        self.startRandomizerButton.setDefault(False)
        self.startRandomizerButton.setFlat(False)
        self.startRandomizerButton.setObjectName("startRandomizerButton")
        self.saveSettingsButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.saveSettingsButton.setGeometry(QtCore.QRect(10, 215, 241, 31))
        self.saveSettingsButton.setObjectName("saveSettingsButton")
        self.autoDetectButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.autoDetectButton.setGeometry(QtCore.QRect(360, 9, 75, 24))
        self.autoDetectButton.setObjectName("autoDetectButton")
        self.browseButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.browseButton.setGeometry(QtCore.QRect(440, 9, 75, 24))
        self.browseButton.setObjectName("browseButton")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setEnabled(True)
        self.frame.setGeometry(QtCore.QRect(263, 41, 251, 81))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frame.setObjectName("frame")
        self.timeSpinbox = QtWidgets.QSpinBox(parent=self.frame)
        self.timeSpinbox.setGeometry(QtCore.QRect(140, 49, 101, 22))
        self.timeSpinbox.setMinimum(1)
        self.timeSpinbox.setMaximum(9999)
        self.timeSpinbox.setObjectName("timeSpinbox")
        self.timerCheckbox = QtWidgets.QCheckBox(parent=self.frame)
        self.timerCheckbox.setGeometry(QtCore.QRect(14, 49, 101, 21))
        font = QtGui.QFont()
        font.setKerning(True)
        self.timerCheckbox.setFont(font)
        self.timerCheckbox.setTristate(False)
        self.timerCheckbox.setObjectName("timerCheckbox")
        self.label_6 = QtWidgets.QLabel(parent=self.frame)
        self.label_6.setGeometry(QtCore.QRect(14, 0, 131, 41))
        self.label_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.randomizeBindButton = QtWidgets.QPushButton(parent=self.frame)
        self.randomizeBindButton.setEnabled(True)
        self.randomizeBindButton.setGeometry(QtCore.QRect(140, 9, 101, 24))
        self.randomizeBindButton.setObjectName("randomizeBindButton")
        self.frame_2 = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_2.setEnabled(True)
        self.frame_2.setGeometry(QtCore.QRect(263, 121, 251, 81))
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frame_2.setObjectName("frame_2")
        self.label_8 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_8.setGeometry(QtCore.QRect(14, 0, 131, 41))
        self.label_8.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_9.setGeometry(QtCore.QRect(14, 39, 131, 41))
        self.label_9.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.enableBindButton = QtWidgets.QPushButton(parent=self.frame_2)
        self.enableBindButton.setEnabled(True)
        self.enableBindButton.setGeometry(QtCore.QRect(140, 9, 101, 24))
        self.enableBindButton.setObjectName("enableBindButton")
        self.disableBindButton = QtWidgets.QPushButton(parent=self.frame_2)
        self.disableBindButton.setEnabled(True)
        self.disableBindButton.setGeometry(QtCore.QRect(140, 49, 101, 24))
        self.disableBindButton.setObjectName("disableBindButton")
        self.frame_3 = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame_3.setEnabled(True)
        self.frame_3.setGeometry(QtCore.QRect(263, 211, 251, 99))
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frame_3.setObjectName("frame_3")
        self.outputLabel = QtWidgets.QLabel(parent=self.frame_3)
        self.outputLabel.setEnabled(True)
        self.outputLabel.setGeometry(QtCore.QRect(0, 0, 251, 99))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        self.outputLabel.setFont(font)
        self.outputLabel.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.outputLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.outputLabel.setObjectName("outputLabel")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Apex Sensitivity Randomizer"))
        self.dpiSelector.setCurrentText(_translate("MainWindow", "400"))
        self.dpiSelector.setItemText(0, _translate("MainWindow", "400"))
        self.dpiSelector.setItemText(1, _translate("MainWindow", "800"))
        self.dpiSelector.setItemText(2, _translate("MainWindow", "1600"))
        self.dpiSelector.setItemText(3, _translate("MainWindow", "3200"))
        self.label.setText(_translate("MainWindow", "Game directory"))
        self.label_2.setText(_translate("MainWindow", "Mouse DPI"))
        self.label_3.setText(_translate("MainWindow", "Default sensitivity"))
        self.label_4.setText(_translate("MainWindow", "Minimum sensitivity"))
        self.label_5.setText(_translate("MainWindow", "Maximum sensitivity"))
        self.startRandomizerButton.setText(_translate("MainWindow", "Start Randomizer"))
        self.saveSettingsButton.setText(_translate("MainWindow", "Save settings"))
        self.autoDetectButton.setText(_translate("MainWindow", "Auto-detect"))
        self.browseButton.setText(_translate("MainWindow", "Browse..."))
        self.timeSpinbox.setSuffix(_translate("MainWindow", "s"))
        self.timerCheckbox.setText(_translate("MainWindow", "Enable Timer"))
        self.label_6.setText(_translate("MainWindow", "Randomize sensitivity"))
        self.randomizeBindButton.setText(_translate("MainWindow", "Set a bind..."))
        self.label_8.setText(_translate("MainWindow", "Enable in-game"))
        self.label_9.setText(_translate("MainWindow", "Disable in-game"))
        self.enableBindButton.setText(_translate("MainWindow", "Set a bind..."))
        self.disableBindButton.setText(_translate("MainWindow", "Set a bind..."))
        self.outputLabel.setText(_translate("MainWindow", "Not running"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())