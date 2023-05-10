from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QToolTip


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.label = QtWidgets.QLabel("Hover over me")
        self.label.setObjectName("my_label")
        self.label.setToolTip("This is my label tooltip")
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.label)

    def event(self, event):
        try:
            if event.type() == QtCore.QEvent.ToolTip:
                sender_obj = self.sender()
                if sender_obj is not None:
                    object_name = sender_obj.objectName()
                    if object_name:
                        self.show_tooltip(sender_obj)
                    else:
                        self.tts.say("Unable to determine object name.")
                else:
                    self.tts.say("No sender object found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        return super().event(event)

    def show_tooltip(self, label):
        QToolTip.showText(self.mapToGlobal(label.pos()), label.objectName())

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    widget = MyWidget()

    # create a QHoverEvent and send it to the label
    hover_event = QtWidgets.QHoverEvent(QtCore.QEvent.HoverEnter, QtCore.QPointF(0,0), QtCore.QPointF(0,0))
    QtWidgets.QApplication.sendEvent(widget.label, hover_event)

    widget.show()
    sys.exit(app.exec_())
