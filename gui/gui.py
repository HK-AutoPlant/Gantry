# window.progressbar.    = od.busvoltage()
# pyuic5 mainwindow.ui -o MainWindow.py
#while (1):
	#app.exec()
	
from PyQt5 import QtWidgets, uic , QtCore  
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
#from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
import time
import odrive
import math
import random
from TreeHive import TreeHive

b = 0
window = 0
b1 = 0
# #
# class WorkerThread(QtCore.QObject):
#     signalExample = QtCore.pyqtSignal(str, int)
 
#     def __init__(self):
#         super().__init__()
 
#     @QtCore.pyqtSlot()
#     def run(self):
#         while True:
#             # Long running task ...
#             self.signalExample.emit("leet", 1337)
#             time.sleep(5)

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
        #self.kwargs['progress_callback'] = self.signals.progress        

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
#----- old--------
# class Worker22(QRunnable):
#     '''
#     Worker thread
#     Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
#     :param callback: The function callback to run on this worker thread. Supplied args and 
#                      kwargs will be passed through to the runner.
#     :type callback: function
#     :param args: Arguments to pass to the callback function
#     :param kwargs: Keywords to pass to the callback function
#     '''
#         def __init__(self, fn, *args, **kwargs):
#         super(Worker, self).__init__()
#         # Store constructor arguments (re-used for processing)
#         self.fn = fn
#         self.args = args
#         self.kwargs = kwargs

#     @pyqtSlot()
#     def run(self):
#         '''
#         Initialise the runner function with passed args, kwargs.
#         '''
#         self.fn(*self.args, **self.kwargs)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        #Load the UI Page
        uic.loadUi('mainwindow2.ui', self)        
        #self.tab_4 = TreeHive(x=30,y=30,iconsize = 20, CC = 25)
        #self.tabWidget.addTab(self.tab_4, "Picking Status")
        self.tab_5 = TreeHive(self.tab_5,x=30,y=30,iconsize = 20, CC = 25)
        #self.widgetTest = QtWidgets.QWidget(self.tab_2)
        # self.tabWidget.addTab(self.tab_5, "NEW")
        # w = QWidget(self.tab_4)
        # ## Create some widgets to be placed inside
        # btn = QPushButton('press me')
        # text = QLineEdit('enter text')
        # listw = QListWidget()
        # plot = pg.PlotWidget()
        # self.plot([1,2,3,4,5,6,7,8,9,10], [30,32,34,32,33,31,29,32,35,45])

        # ## Create a grid layout to manage the widgets size and position
        # layout = QGridLayout()
        # w.setLayout(layout)

        # ## Add widgets to the layout in their proper positions
        # layout.addWidget(btn, 0, 0)   # button goes in upper-left
        # layout.addWidget(text, 1, 0)   # text edit goes in middle-left
        # layout.addWidget(listw, 2, 0)  # list widget goes in bottom-left
        # layout.addWidget(plot, 0, 1, 3, 1)  # plot goes on right side, spanning 3 rows

        self.pushButton_Home.setIcon(QIcon("icons/home.png"))
        self.pushButton_Left.setIcon(QIcon("icons/left.png"))
        self.pushButton_Right.setIcon(QIcon("icons/right.png"))
        self.pushButton_Up.setIcon(QIcon("icons/up.png"))
        self.pushButton_Down.setIcon(QIcon("icons/down.png"))

        # Standrad ControlMode = Auto
        self.controllerMode = "Auto"    
        
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.show()
        
        self.pushButton_Auto_Manual.clicked.connect(self.controlMode)

        self.pushButton.clicked.connect(self.pressed)
        #self.odrv0 = self.ConnectOdrive()
       
        self.startWorkers()
        #self.odriveConnect.clicked.connect(self.startWorkers)
        self.odriveConnect.clicked.connect(self.workerConnectOdrive)
        self.closedLoopAxis0CheckBox.clicked.connect(lambda:self.closedLoop(0))
        self.closedLoopAxis1CheckBox.clicked.connect(lambda:self.closedLoop(1))
        

#---------------------------------------------------------------------------------------------
#-------------------Push Buttons And Sliders--------------------------------------------------
#---------------------------------------------------------------------------------------------
        # pushButtons for navigation
        self.pushButton_Up.clicked.connect(self.moveUp)
        self.pushButton_Down.clicked.connect(self.moveDown)
        self.pushButton_Right.clicked.connect(self.moveRight)
        self.pushButton_Left.clicked.connect(self.moveLeft)
        self.pushButton_Home.clicked.connect(self.moveHome)

        # Slider for navigation
        self.posXSlider.valueChanged.connect(self.movePosX)
        # pushButton for Calibration
        self.pushButton_CalibrateAxis0.clicked.connect(lambda:self.calibrateAxis(0))
        self.pushButton_CalibrateAxis1.clicked.connect(lambda:self.calibrateAxis(1))

        # pushButton for odrive
        self.settingsButtons.accepted.connect(self.saveOdriveSettings)
        self.settingsButtons.button(QDialogButtonBox.Reset).clicked.connect(self.resetErrorOdrive)
        self.pushButton_Reboot.clicked.connect(self.rebootOdrive)

        # pushButton for buffer
        self.pushButton_BufferEmptied.clicked.connect(self.emptyBuffer)
        
        # pushButton for collecting trees
        self.pushButton_collectTree.clicked.connect(self.collectingTrees)

#---------------------------------------------------------------------------------------------    
#---------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------
#-------------------TIMERS--------------------------------------------------------------------
        # timer for handling slider to set Velocity Limits
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.limitVelocity_in_X)
        self.timer.start()

        # timer for updating battery voltage
        self.batteryUpdateTimer = QTimer()
        self.batteryUpdateTimer.setInterval(5000)
        self.batteryUpdateTimer.timeout.connect(self.batteryUpdatevalue)
        self.batteryUpdateTimer.start()

        # Timer for Error check
        self.errorCheckTimer = QTimer()
        self.errorCheckTimer.setInterval(1500)
        self.errorCheckTimer.timeout.connect(self.errorCheck)
        self.errorCheckTimer.start()
        # Timer for Plotting Odrive data
        self.plotOdriveTimer = QTimer()
        self.plotOdriveTimer.setInterval(300)
        self.plotOdriveTimer.timeout.connect(self.plotOdriveData)
        self.plotOdriveTimer.start()
        #self.collectData()
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
        self.axis0_encoder_pos_estimate     = [0]
        # self.axis1.encoder.pos_estimate     = []
        self.axis0_controller_pos_setpoint  = [0]
        # self.axis1.controller.pos_setpoint  = []
        self.plotAxisX = [0]        
        # self.x = list(range(100))  # 100 time points
        # self.y = [random.uniform(0,100) for _ in range(100)]  # 100 data points
        # self.graphWidget.setBackground('w')
        pen1 = pg.mkPen(color=(255, 0, 0))
        pen2 = pg.mkPen(color=(0, 255, 0))
        # self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
        self.graphWidget.addLegend()
        self.data_line  =  self.graphWidget.plot(self.plotAxisX, self.axis0_encoder_pos_estimate     , name="Estimated",pen=pen1)
        self.data_line2 =  self.graphWidget.plot(self.plotAxisX, self.axis0_controller_pos_setpoint  , name="Setpoint",pen=pen2)
        # self.plot(self.plotAxisX , self.odrv0.axis0.encoder.pos_estimate     , "Sensor1" , 'r')

#---------------------------------------------------------------------------------------------
#-------------------Functions--------------------------------------------------------------------
    
    def plotOdriveData(self): #update_plot_data
        if hasattr(self, 'odrv0' ) == True:
            # self.plotAxisX = self.plotAxisX[1:]  # Remove the first y element.
            self.plotAxisX.append(self.plotAxisX[-1] + 1)  # Add a new value 1 higher than the last.       
            # self.y = self.y[1:]  # Remove the first 
            # self.axis0_encoder_pos_estimate.append( random.uniform(0,100))  # Add a new random value.
            #self.axis0_encoder_pos_estimate.append(self.axis0_encoder_pos_estimate[-1])  # Add a new random value.
            #self.axis0_encoder_pos_estimate.append(self.odrv0.axis0.encoder.pos_estimate)
            pos = self.odrv0.axis0.encoder.pos_estimate
            # pos = 1.2
            pos2 = self.odrv0.axis0.controller.pos_setpoint
            self.axis0_encoder_pos_estimate.append(pos)
            self.axis0_controller_pos_setpoint.append(pos2)
            #self.odrv0.axis0.controller.pos_setpoint(pos2)
            print(self.axis0_encoder_pos_estimate)
            self.data_line.setData(self.plotAxisX, self.axis0_encoder_pos_estimate)  # Update the data.
            self.data_line2.setData(self.plotAxisX, self.axis0_controller_pos_setpoint)  # Update the data.
    

    def plot(self, X, Y):
        # self.graphWidget.plot(X ,Y)
        self.data_line.setData(X, Y)  # Update the data.

    def collectingTrees(self):
        for n in range(1,5):
            for i in range(1,5):
                self.tab_5.setGroupOfTreesToInProgress(n,i)
                time.sleep(0.1)
                self.tab_5.update()
        
    def calibrateAxis(self, axis):
        try:
            if axis == 0:
                self.odrv0.axis0.requested_state = 3
            if axis == 1:
                self.odrv0.axis1.requested_state = 3
        except:
            pass

    def errorCheck(self):
        try:
            error_Axis0 = self.odrv0.axis0.error
            error_Axis1 = self.odrv0.axis1.error
            self.errorAxis0.setText(str(error_Axis0))
            self.errorAxis1.setText(str(error_Axis1))
            self.errorAxis0.adjustSize()
            self.errorAxis1.adjustSize()
        except:
            pass

    def rebootOdrive(self):
        try:
            self.odrv0.reboot()
        except:
            pass
        
    def resetErrorOdrive(self):
        print("Rebooting Odrive")
        try:
            #self.odrv0.reboot()
            self.odrv0.axis0.clear_errors()
            self.odrv0.axis1.clear_errors()
        except:
            pass

    def saveOdriveSettings(self):
        print("saving odrive settings")
        try:
            self.odrv0.save_configuration()
        except:
            pass
        
        #self.settingsButtons

    def keyPressEvent(self, event):
        #https://doc.qt.io/qtforpython/PySide2/QtCore/Qt.html
        if event.key() == Qt.Key_W:            
            self.moveUp()
        elif event.key() == Qt.Key_A:
            self.moveLeft()
        elif event.key() == Qt.Key_S:
            self.moveDown()
        elif event.key() == Qt.Key_D:
            self.moveRight()
        #elif event.key() == Qt.Key_Space:
         #   self.moveHome()

    def controlMode(self):
        if self.pushButton_Auto_Manual.text() == "Auto":
            self.controllerMode = "Manual"
            self.pushButton_Auto_Manual.setText("Manual")
        else:
            self.controllerMode = "Auto"
            self.pushButton_Auto_Manual.setText("Auto")

    def closedLoop(self, axis):
        try:  
            if axis == 0:
                if self.closedLoopAxis0CheckBox.isChecked():
                    #print("trying to enter closed loop Axis0")                        
                    self.odrv0.axis0.requested_state = 8
                    print("closedLoop set AXIS 0")

                elif not(self.closedLoopAxis0CheckBox.isChecked()):
                    print("closedLoop UNset Axis 0")
                    self.odrv0.axis0.requested_state = 1

            if axis == 1:

                if self.closedLoopAxis1CheckBox.isChecked():
                # print("trying to enter closed loop Axis1")                        
                    self.odrv0.axis1.requested_state = 8
                    print("closedLoop set AXIS 1")

                elif not (self.closedLoopAxis1CheckBox.isChecked()):
                    print("closedLoop UNset Axis 1")                   
                    self.odrv0.axis1.requested_state = 1
                    
        except:
            pass

    def batteryUpdatevalue(self):
        #print("trying")
        try:
            #print(self.odrv0.vbus_voltage)
            # Estimated State Of Chare(SOC) 
            # taken from https://www.energymatters.com.au/components/battery-voltage-discharge/
            # Linear regressen y = k*x + m was made
            # vbusVoltage = random.uniform(11.5, 13) 
            vbusVoltage = self.odrv0.vbus_voltage
            self.batteryVoltage.setText(str(vbusVoltage))
            self.lcdNumber.setProperty("value",vbusVoltage)
            chargeLevel = round(92.98507 * vbusVoltage - 1095.39005, 1) 
            if chargeLevel > 100:
                chargeLevel = 100
            if chargeLevel < 0:
                chargeLevel = 0
            #print(chargeLevel)
            self.batteryChargeLevel.setProperty("value",chargeLevel)
        except:
            pass

    def limitVelocity_in_X(self):
        max_vel = self.velocityLimitX.value()  
        #self.lcd_vel.setProperty("value",max_vel)
        try:
            self.odrv0.axis1.controller.config.vel_limit = max_vel 
            self.lcd_vel.setProperty("value",self.odrv0.axis1.controller.config.vel_limit)
        except:
            pass
        
    def startWorkers(self): 
        pass
        # Pass the function to execute
        #worker   = Worker(self.batteryUpdatevalue)        
        #worker3  = Worker(self.movePosX)
        # Execute
        #self.threadpool.start(worker)
        #self.threadpool.start(worker3)

    def progress_fn(self,n):
        print(n)

    # Functions For Connecting Odrive
    def odrv0_object(self, s):
        #print(s)
        self.odrv0 = s
        return s

    def workerConnectOdrive(self):
        worker = Worker(self.ConnectOdrive)
        worker.signals.result.connect(self.odrv0_object)
        #self.odrv0 = worker.signals.result
        #worker.signals.finished.connect(self.thread_complete)
        #worker.signals.progress.connect(self.progress_fn)
        #worker.setAutoDelete(True)
        #worker.autoDelete()
        self.threadpool.start(worker)

    def ConnectOdrive(self):
        #print("connecting odrive")
        self.odriveConnect.setText("connecting odrive")
        self.odriveConnect.adjustSize()
        # connect odrive and return object for all other funciton.
        # This must be proteced by a Mutex!!!! or Signals!!
        odrv0 = odrive.find_any()
        #print("odrive connected")
        self.odriveConnect.setText("odrive connected")
        self.odriveConnect.adjustSize()
        return odrv0

    def pressed(self):        
        self.progressBar.setProperty("value",self.progressBar.value()+1)
        #print("1")
        self.batteryVoltage.setText("hejhej")
   
   # Functions For Moving The Axis
    def movePosX(self):
        posX = 2*self.posXSlider.value() /100.0
        # use lambda function to accept second input
        print(posX)
        self.lcd_vel.setProperty("value",posX) 
        try:
            print("trying to move")
            self.odrv0.axis1.controller.input_pos = posX
        except:
            pass
   
    def emptyBuffer(self):
        #for n in range(1,5):
            #str("self" +"." + frame_ + "n" + ".setStyleSheet('background-color:black')")
        self.frame_1.setStyleSheet('background-color:black')
        #time.sleep(1)
        self.frame_2.setStyleSheet('background-color:black')
        #time.sleep(1)
        #self.frame_1.setStyleSheet('background-color:rgb(0, 255, 0)')
        self.frame_3.setStyleSheet('background-color:black')
        #time.sleep(1)
        self.frame_1.setStyleSheet('background-color:rgb(0, 255, 0)')
   
    def moveUp(self):
        StepSize = self.stepInTurns.value()        
        self.lcdPos_Up.setProperty("value", round(self.lcdPos_Up.value() + StepSize , 2))        
        try:
            self.odrv0.axis1.controller.move_incremental(StepSize , 1)
        except:
            pass
        
    def moveDown(self): 
        StepSize = self.stepInTurns.value()       
        self.lcdPos_Up.setProperty("value", round(self.lcdPos_Up.value() - StepSize , 2))
        try:
            self.odrv0.axis1.controller.move_incremental(-StepSize , 1)
        except:
            pass

    def moveLeft(self):   
        StepSize = self.stepInTurns.value()     
        self.lcdPos_Left.setProperty("value", round(self.lcdPos_Left.value() - StepSize , 2))
        try:
            self.odrv0.axis0.controller.move_incremental(-StepSize , 1)
        except:
            pass
        
    def moveRight(self):    
        StepSize = self.stepInTurns.value()
        self.lcdPos_Left.setProperty("value", round(self.lcdPos_Left.value() + StepSize , 2))
        try:
            self.odrv0.axis0.controller.move_incremental(StepSize , 1)
        except:
            pass
    
    def moveHome(self):
        self.lcdPos_Up.setProperty("value", 0)
        self.lcdPos_Left.setProperty("value", 0)
        try:
            self.odrv0.axis0.controller.input_pos(0) 
            self.odrv0.axis1.controller.input_pos(0)
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
