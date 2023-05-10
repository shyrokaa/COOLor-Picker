from PyQt5 import QtGui, QtWidgets


def resize_button(button: QtWidgets.QPushButton, scale: float):
    font = button.font()
    font.setPointSize(int(font.pointSize() * scale))
    button.setFont(font)

    size = button.size()
    button.resize(size.width() * scale, size.height() * scale)
