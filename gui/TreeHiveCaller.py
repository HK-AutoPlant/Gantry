import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import numpy
from TreeHive import *

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TreeHiveTester')
        self.setGeometry(0,0,1300,800)
        self.show()
        self.trees = TreeHive()


def main():
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()
else:
    print('imported ' + __name__)
