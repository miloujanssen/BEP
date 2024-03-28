"""Main method for starting the application"""

import sys

from PySide6.QtWidgets import QApplication

from application import Application


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myApp = Application()
    myApp.show()
    app.exec()
