# window.progressbar.    = od.busvoltage()
# pyuic5 mainwindow.ui -o MainWindow.py
#while (1):
	#app.exec()
	
from PyQt5 import QtWidgets, uic
#from pyqtgraph import PlotWidget
#import pyqtgraph as pg
import sys
b = 0
window = 0
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi('mainwindow.ui', self)

    def pressed(self, odrv):        
        self.progressBar.setProperty("value",self.progressBar.value()+1)
        #print("1")
        print(odrv)
        self.batteryVoltage.setText("hejhej")
        if(self.checkBox.isChecked()):
            print("hej")

    def batteryCheck(self):
        print("hej")
        if(self.checkBox.isChecked()):
            print("hej")
            self.progressBar.setProperty("value",self.progressBar.value()+1)

def main():
    global window
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    
    global b 
    b = MainWindow()
    window.pushButton.clicked.connect(window.pressed)   
   # window.batteryVoltage.setText('BatteryVoltage = 13V')
    window.lcdNumber.setProperty("value",5.4)

    #window.pressed("hej2")
    window.show()
    #window.pressed()    
    sys.exit(app.exec_())
       
    

if __name__ == '__main__':   
    #while(True):
     #   print("hej")     
    main()
