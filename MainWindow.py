import json

from PyQt5 import QtWidgets, QtGui, uic, QtCore
from random import randint, choice

from PyQt5.QtGui import QIcon

from SettingsDialog import SettingsDialog


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Load the UI file
        uic.loadUi('main.ui', self)
        self.setWindowTitle("COOLor Picker")

        # Set the window icon
        try:
            icon = QIcon('assets/icon.png')
        except Exception as e:
            print(f"An error occurred while loading the icon: {e}")
        self.setWindowIcon(icon)

        # Find the widgets
        try:
            self.listView = self.findChild(QtWidgets.QListView, 'listView')
            self.generateButton = self.findChild(QtWidgets.QPushButton, 'generateButton')
            self.copyButton = self.findChild(QtWidgets.QPushButton, 'copyButton')
            self.comboBox = self.findChild(QtWidgets.QComboBox, 'comboBox')
            self.checkBox = self.findChild(QtWidgets.QCheckBox, 'checkBox')
        except AttributeError as e:
            raise AttributeError(f"Error finding one or more UI elements: {e}")

        # Connect the signals to the slots
        self.generateButton.clicked.connect(self.generate_palette)
        self.copyButton.clicked.connect(self.copy_palette_to_clipboard)
        self.listView.clicked.connect(self.copy_color_to_clipboard)

        # Set the listView to be non-editable
        self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # Connect the actionSettings to the settings_dialog function
        self.actionSettings.triggered.connect(self.settings_dialog)

        # apply the theme to the main window
        self.setFixedSize(self.size())
        self.load_theme()

    def settings_dialog(self):
        try:
            settings_window = SettingsDialog()
            settings_window.exec_()
            self.update_theme()
        except Exception as e:
            print(f"An error occurred while opening the settings window: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", "An error occurred while opening the settings window.")

    def generate_palette(self):
        try:
            palette_size = int(self.comboBox.currentText())
            monochromatic_mode = self.checkBox.isChecked()

            if monochromatic_mode:
                hue = randint(0, 359)
                brightness_step = 80 // palette_size
                saturation_step = 60 // palette_size
                colors = []
                for i in range(palette_size):
                    saturation = 50 + i * saturation_step
                    brightness = 10 + i * brightness_step
                    color = QtGui.QColor.fromHsv(hue, saturation, brightness)
                    colors.append(color)
            else:
                # Generate color wheel
                hue = randint(0, 359)
                colors = []
                for i in range(palette_size):
                    color_hue = (hue + i * 360 / palette_size) % 360
                    color_saturation = 50 + randint(0, 100)  # Increase saturation range to 0-100
                    color_value = 50 + randint(0, 50)

                    # Use color theory principles to adjust saturation and brightness
                    color_saturation = self.adjust_saturation(color_saturation)
                    color_value = self.adjust_brightness(color_value)

                    color = QtGui.QColor.fromHsv(color_hue, color_saturation, color_value)
                    colors.append(color)

            # Update the list view
            model = QtGui.QStandardItemModel()
            for color in colors:
                item = QtGui.QStandardItem()
                item.setBackground(QtGui.QBrush(color))
                item.setText(color.name())
                model.appendRow(item)
            self.listView.setModel(model)
        except Exception as e:
            print(f"An error occurred while generating the palette: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", "An error occurred while generating the palette.")

    def adjust_saturation(self, saturation):
        # Adjust saturation based on color theory principles
        if saturation < 50:
            saturation = saturation + 20
        else:
            saturation = saturation - 20
        return saturation

    def adjust_brightness(self, brightness):
        # Adjust brightness based on color theory principles
        if brightness < 50:
            brightness = brightness + 20
        else:
            brightness = brightness - 20
        return brightness

    def copy_palette_to_clipboard(self):
        try:
            clipboard = QtWidgets.QApplication.clipboard()
            model = self.listView.model()
            text = '\n'.join([model.item(i).text() for i in range(model.rowCount())])
            clipboard.setText(text)
            self.copyButton.setText("Copied to clipboard")
            QtCore.QTimer.singleShot(3000, lambda: self.copyButton.setText("Copy to clipboard"))
        except Exception as e:
            print(f"An error occurred while copying the palette to the clipboard: {e}")
            QtWidgets.QMessageBox.warning(self, "Error",
                                          "An error occurred while copying the palette to the clipboard.")

    def copy_color_to_clipboard(self, index):
        try:
            clipboard = QtWidgets.QApplication.clipboard()
            model = self.listView.model()
            item = model.itemFromIndex(index)
            color = item.background().color()
            clipboard.setText(color.name())

            # Change the item text to "Copied to clipboard" for 3 seconds
            original_text = item.text()
            item.setText("Copied")
            self.listView.update(index)
            QtCore.QTimer.singleShot(3000, lambda: item.setText(original_text))
        except Exception as e:
            print(f"An error occurred while copying the color to the clipboard: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", "An error occurred while copying the color to the clipboard.")

    # theme handling

    def load_theme(self):
        # Load theme name from config.json
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                theme_name = config.get('theme', 'default.qss')  # Default theme name if not specified
        except FileNotFoundError:
            theme_name = 'default.qss'  # Default theme name if config.json not found
        except json.JSONDecodeError as e:
            print(f"Error loading config.json: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", "Failed to load config.json")
            theme_name = 'default.qss'  # Default theme name if config.json is malformed or invalid

        # Load and apply the theme
        self.apply_theme(theme_name)

    def apply_theme(self, theme_name):
        # Build path to theme QSS file
        theme_path = 'themes/' + theme_name

        # Load and apply QSS file
        try:
            with open(theme_path, 'r') as f:
                style_data = f.read()
                self.setStyleSheet(style_data)
        except FileNotFoundError:
            print(f"Error loading theme {theme_name}: File not found")
            QtWidgets.QMessageBox.warning(self, "Error", f"Failed to load theme {theme_name}")
        except Exception as e:
            print(f"Error loading theme {theme_name}: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", f"Failed to load theme {theme_name}")

    def update_theme(self):
        # Get theme name from config.json
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                theme_name = config.get('theme', 'default.qss')  # Default theme name if not specified
        except FileNotFoundError:
            theme_name = 'default.qss'  # Default theme name if config.json not found
        except json.JSONDecodeError as e:
            print(f"Error loading config.json: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", "Failed to load config.json")
            theme_name = 'default.qss'  # Default theme name if config.json is malformed or invalid

        # Apply the updated theme
        self.apply_theme(theme_name)
