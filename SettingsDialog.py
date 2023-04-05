import json
import os
from PyQt5 import QtWidgets, uic, QtGui, QtCore


class SettingsDialog(QtWidgets.QDialog):
    def __init__(self):
        super(SettingsDialog, self).__init__()

        # Set window flags to exclude the help button
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        try:
            uic.loadUi('options.ui', self)
        except Exception as e:
            print(f"An error occurred while loading the options UI file: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", "An error occurred while loading the options UI file.")
        self.setWindowTitle("Settings")

        # Find and setup list view for displaying QSS file names
        self.qss_list_view = self.findChild(QtWidgets.QListView, 'listView_qss')
        self.qss_list_view.clicked.connect(self.on_qss_selected)

        # Find and setup "Apply" button
        self.apply_button = self.findChild(QtWidgets.QPushButton, 'applyTheme')
        self.apply_button.clicked.connect(self.on_apply_button_clicked)

        # Load QSS file names and populate the list view
        self.load_qss_files()
        self.setFixedSize(self.size())

    def on_apply_button_clicked(self):
        try:
            # Get the selected QSS file name from the list view
            index = self.qss_list_view.currentIndex()
            if index.isValid():
                qss_file_name = self.qss_list_view.model().data(index)

                # Update the current theme in config.json
                with open('config.json', 'r+') as config_file:
                    config_data = json.load(config_file)
                    config_data['theme'] = qss_file_name + ".qss"  # Add .qss extension
                    config_file.seek(0)
                    json.dump(config_data, config_file, indent=4)
                    config_file.truncate()

                # Close the settings window
                self.close()
        except Exception as e:
            print(f"An error occurred while applying settings: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", "An error occurred while applying settings.")

    def load_qss_files(self):
        # Load QSS file names from "themes" folder
        qss_files = os.listdir("themes")

        # Set up model to populate the list view
        model = QtGui.QStandardItemModel()
        for qss_file in qss_files:
            item = QtGui.QStandardItem(qss_file[:-4])  # Remove .qss extension
            model.appendRow(item)

        # Set the model on the list view
        self.qss_list_view.setModel(model)

    def on_qss_selected(self, index):
        # Handle QSS file selected
        selected_qss_file = self.qss_list_view.model().itemData(index)[0]
        print(f"Selected QSS file: {selected_qss_file}")
        # Apply selected QSS file for the whole program
        qss_file_path = os.path.join("themes", selected_qss_file + ".qss")  # Add .qss extension
        self.apply_qss(qss_file_path)

    def apply_qss(self, qss_file):
        # Apply QSS file for the whole program
        with open(qss_file, 'r') as f:
            qss_data = f.read()
            self.setStyleSheet(qss_data)
