from PyQt5 import QtWidgets, uic , QtCore  
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#from pyqtgraph import PlotWidget
#import pyqtgraph as pg
import time
import odrive
import traceback, sys


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data
    
    error
        `tuple` (exctype, value, traceback.format_exc() )
    
    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress 

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and 
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()    

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress        

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        
        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done
        


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi('mainwindow.ui', self)
        #self.show()
        self.threadpool = QThreadPool()
        self.show()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.pushButton.clicked.connect(self.pressed)
        self.odrv0 = self.ConnectOdrive()
       
        # self.startWorkers()
        #self.odriveConnect.clicked.connect(self.startWorkers)
        #self.showVolt()
        #self.velocity_in_X()
       # self.batteryCheck() 

        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.limitVelocity_in_X)
        self.timer.start()

    def showVolt(self):
        print(self.odrv0.vbus_voltage)
        vbusVoltage = self.odrv0.vbus_voltage
        self.batteryVoltage.setText(str(vbusVoltage))
        self.lcdNumber.setProperty("value",vbusVoltage)

    def limitVelocity_in_X(self):
        max_vel = self.velocityLimitX.value()  
        self.lcd_vel.setProperty("value",max_vel) 
            
    def startWorkers(self):        
        # Pass the function to execute
        worker   = Worker(self.batteryUpdatevalue)
        
       # worker3  = Worker(self.movePosX)
        if self.odriveConnect.isChecked():
            worker2  = Worker(self.ConnectOdrive)
            #worker2.signals.finished.connect(self.batteryUpdatevalue)
            self.threadpool.start(worker2)
        # Execute
        self.threadpool.start(worker)
        # self.threadpool.start(worker3)

    def ConnectOdrive(self):
        print("connecting odrive")
        # connect odrive and return object for all other funciton.
        # This must be proteced by a Mutex!!!! or Signals!!
        odrv0 = odrive.find_any()
        print("odrive connected")
        return odrv0

    def pressed(self):        
        self.progressBar.setProperty("value",self.progressBar.value()+1)
        #print("1")
        self.batteryVoltage.setText("hejhej")
        if(self.checkBox.isChecked()):
            #print("hej")
            self.batteryCheck()

    def batteryUpdatevalue(self):
        #print(self.odrv0)
        #while self.odrv0 == None:
         #   time.sleep(1)
        #self.odrv0 = odrive.find_any() # Finds the Odrive
        time.sleep(1)
        #print(odrv0)
        for n in range(0,1):
            #while(0):            
            vbusVoltage = self.odrv0.vbus_voltage
            #vbusVoltage = 5
            self.batteryVoltage.setText(str(vbusVoltage))
            self.lcdNumber.setProperty("value",vbusVoltage)
            #print("hej")            
            time.sleep(1)
        
            #QApplication.processEvents() 

    def batteryCheck(self):
    # Pass the function to execute
        worker  = Worker(self.batteryUpdatevalue)
    # Execute
        self.threadpool.start(worker)
   
    def movePosX(self):
        posX = self.posInX.value()
        self.lcd_vel.setProperty("value",posX) 
        try:
            self.odrv0.axis1.controller.move_incremental(posX,1)
        except:
            pass
        
    

def main():
    global window
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    
    #global b 
    #b = MainWindow()
    #b= QtWidgets.QApplication.processEvents()
    #window.show()       
    sys.exit(app.exec_())    
    
if __name__ == '__main__':   
    #while(True):
     #   print("hej")     
    main()

