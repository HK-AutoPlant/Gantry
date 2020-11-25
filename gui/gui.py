# window.progressbar.    = od.busvoltage()
# pyuic5 mainwindow.ui -o MainWindow.py
#while (1):
	#app.exec()
	

import sys
import os
sys.path.append("../zAxis/Python") # Adds higher directory to python modules path.

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
from PyQtGraphDataPlot import *
##----- Gamepad Controller library -----------------
try:
    from bl import xboxOne
    print("imported")
except Exception as e :
    print(e)

#---- Port recognition ------
from portRecognition import findArduinoPort

#---- Arduino Stepper Motor Control ------
from SC import usbCommunication
#----------------- MQTT--------------------
import paho.mqtt.client as paho
broker = "127.0.0.1"
broker_port = 1883

# from PyQt5 import QtWebEngineWidgets
# from PyQt5 import QtWebEngineCore
# from PyQt5.QtWebEngineWidgets import QWebEngineSettings

b = 0
window = 0
b1 = 0

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

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self,resWidth,resHeight, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        #Load the UI Page
        uic.loadUi('mainwindow2.ui', self)
        # Importing TreeHive into widget window        
        #x=50,y=50,iconsize=25,CC=30,rows=20,columns=35):
        ratio = resHeight/resWidth
        cc = 1.3*ratio*resHeight/(19+2*0.8)
        iconSize = ratio*cc
        # print(self.treeWidget))
        self.treeWidget.createTrees(0,0,iconSize,cc,20,35)
        # Create paho Mqtt object
        self.client = paho.Client("Autoplant1") #create client object
        # Arduino Stepper Motor 
        # files_and_directories = os.listdir("/dev/ttyUSB*")
        try:
            zAxisSerialNumber = "AB0K1I4L" #zAxis serial number. 
            zAxisUsbPort = findArduinoPort(zAxisSerialNumber)

            #Device_id = os.listdir("/dev/ttyUSB*")
            #zAxisUsbPort = Device_id
            BAUD_RATE = 115200
            # zAxisUsbPort = '/dev/ttyUSB0'
            self.zAxis = usbCommunication(zAxisUsbPort, BAUD_RATE)
        except Exception as e:
            print(e)        
        # For using an Xbox One Controller
        try:
            self.readXboxInput = xboxOne()
            print("xbox created")
        except :
            pass
        #Sets icon of the control buttons, can be made in QtCreator as well...
        self.pushButton_Home.setIcon(QIcon("icons/home.png"))
        self.pushButton_Left.setIcon(QIcon("icons/left.png"))
        self.pushButton_Right.setIcon(QIcon("icons/right.png"))
        self.pushButton_Up.setIcon(QIcon("icons/up.png"))
        self.pushButton_Down.setIcon(QIcon("icons/down.png"))
        self.pushButton_zUp.setIcon(QIcon("icons/up.png"))
        self.pushButton_zDown.setIcon(QIcon("icons/down.png"))
        self.pushButton_zHome.setIcon(QIcon("icons/home.png"))
        # Start worker threds
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.startWorkers()    
        # Start Odrive connectiong as a thred to not lock the GUI!
        self.odriveConnect.clicked.connect(self.workerConnectOdrive)
        # Set Axis motor intop close loop control
        self.closedLoopAxis0CheckBox.clicked.connect(lambda:self.closedLoop(0))
        self.closedLoopAxis1CheckBox.clicked.connect(lambda:self.closedLoop(1))       
        # Standrad ControlMode = Auto
        self.controllerMode = "Manual" 
        time.sleep(2)
        self.movezAxis("Home", 0)
        
        # Webcam video feed
        # QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.PluginsEnabled,True)        
        # self.webWidget.setUrl(QUrl("http://localhost:8081"))
        # self.webWidget.setUrl(QUrl("https://www.youtube.com/watch?v=Zje_ihjZdLM2"))
        # Open GUI window     
        self.show()
        self.showMaximized()
        
        
#---------------------------------------------------------------------------------------------
#-------------------Push Buttons And Sliders--------------------------------------------------
#---------------------------------------------------------------------------------------------
        # Change control mode between Auto and Manuals       
        self.pushButton_Auto_Manual.clicked.connect(self.controlMode)
        # pushButtons for navigation
        self.pushButton_Up.clicked.connect(self.moveUp)
        self.pushButton_Down.clicked.connect(self.moveDown)
        self.pushButton_Right.clicked.connect(self.moveRight)
        self.pushButton_Left.clicked.connect(self.moveLeft)
        self.pushButton_Home.clicked.connect(self.moveHome)
        # Slider for navigation
        self.posXSlider.valueChanged.connect(self.movePosX)
        # Sliders for maximum speed
        self.velocityLimitX.valueChanged.connect(lambda:self.odriveVelocityLimit(1))
        self.velocityLimitY.valueChanged.connect(lambda:self.odriveVelocityLimit(0))
        # pushButton for Calibration
        self.pushButton_CalibrateAxis0.clicked.connect(lambda:self.calibrateAxis(0))
        self.pushButton_CalibrateAxis1.clicked.connect(lambda:self.calibrateAxis(1))
        # pushButton for odrive
        self.settingsButtons.accepted.connect(self.saveOdriveSettings)
        self.settingsButtons.button(QDialogButtonBox.Reset).clicked.connect(self.resetErrorOdrive)
        self.pushButton_Reboot.clicked.connect(self.rebootOdrive)
        self.pushButton_calibrateEncodeOffsetAxis0.clicked.connect(lambda:self.calibrateEncoder(0))
        self.pushButton_calibrateEncodeOffsetAxis1.clicked.connect(lambda:self.calibrateEncoder(1))
        self.comboBox_CheckParameter.currentIndexChanged.connect(lambda: self.checkParameter(self.comboBox_CheckParameter.currentText())) # checking various parameters in the oDrive
        # pushButton for zAxis movement
        self.pushButton_zDown.clicked.connect(lambda: self.movezAxis("Down",self.zAxisStepInmm.value()))
        self.pushButton_zUp.clicked.connect(lambda: self.movezAxis("Up",self.zAxisStepInmm.value()))
        self.pushButton_zHome.clicked.connect(lambda: self.movezAxis("Home",0))
        # pushButton for buffer
        self.pushButton_BufferEmptied.clicked.connect(self.emptyBuffer)        
        # pushButton for collecting trees
        self.pushButton_GoToPosition.clicked.connect(lambda: self.goToPosition(int(self.comboBox_TreePos.currentText()),int(self.comboBox_TreeRow.currentText())))

        self.comboBox_CheckParameter.currentIndexChanged.connect(lambda: self.checkParameter(self.comboBox_CheckParameter.currentText()))
        self.pushButton_calibrateEncodeOffsetAxis0.clicked.connect(lambda:self.calibrateEncoder(0))
        self.pushButton_calibrateEncodeOffsetAxis1.clicked.connect(lambda:self.calibrateEncoder(1))

        #self.actionquit.triggered.connect(sys.exit(self) )
#---------------------------------------------------------------------------------------------    

#---------------------------------------------------------------------------------------------
#-------------------TIMERS--------------------------------------------------------------------
        # timer for handling slider to set Velocity Limits
        self.timer = QTimer()
        self.timer.setInterval(100)
        #self.timer.timeout.connect(self.limitVelocity_in_X)
        # self.timer.start()
        # timer for updating battery voltage
        self.batteryUpdateTimer = QTimer()
        self.batteryUpdateTimer.setInterval(5000)
        self.batteryUpdateTimer.timeout.connect(self.batteryUpdatevalue)
        self.batteryUpdateTimer.start()
        # Timer for Error check
        self.errorCheckTimer = QTimer()
        self.errorCheckTimer.setInterval(500)
        self.errorCheckTimer.timeout.connect(self.errorCheck)
        self.errorCheckTimer.start()
        # Timer for Plotting Odrive data
        self.plotOdriveTimer = QTimer()
        self.plotOdriveTimer.setInterval(200)
        self.plotOdriveTimer.timeout.connect(self.plotOdriveData)
        self.plotOdriveTimer.start()
        #self.collectData()
#---------------- End Timers -----------------------------------------------------------------

#-------------------Plotting------------------------------------------------------------------
        # Plot data for Axis0
        self.axis0_encoder_pos_estimate     = [0]        
        self.axis0_controller_pos_setpoint  = [0]        
        self.axis0_controller_vel_setpoint  = [0]
        self.axis0_encoder_vel_estimate     = [0]            
        # Plot data for Axis1  
        self.axis1_encoder_pos_estimate     = [0]
        self.axis1_controller_pos_setpoint  = [0]
        self.axis1_controller_vel_setpoint  = [0]
        self.axis1_encoder_vel_estimate     = [0]  
        # Common data
        self.plotAxisX = [0]  # X-axis => samples
        # Plot Styling
        # self.graphWidget.setBackground('w')
        pen1 = pg.mkPen(color=(255, 0, 0), width=1)
        pen2 = pg.mkPen(color=(0, 255, 0), width=3)
        pen3 = pg.mkPen(color=(255, 0, 0), width=1)
        pen4 = pg.mkPen(color=(0, 255, 0), width=1)
        # self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
        self.graphWidget.addLegend()
        self.graphWidget_2.addLegend()
        self.data_line  =  self.graphWidget.plot(self.plotAxisX, self.axis0_encoder_pos_estimate     , name="Estimated",pen=pen1)
        self.data_line2 =  self.graphWidget.plot(self.plotAxisX, self.axis0_controller_pos_setpoint  , name="Setpoint",pen=pen2)
        self.data_line3 =  self.graphWidget_2.plot(self.plotAxisX, self.axis0_encoder_vel_estimate   , name="velocity estimate",pen=pen3)
        self.data_line4 =  self.graphWidget_2.plot(self.plotAxisX, self.axis0_controller_vel_setpoint, name="velocity setpoint",pen=pen4)
        # self.plot(self.plotAxisX , self.odrv0.axis0.encoder.pos_estimate     , "Sensor1" , 'r')
        self.pushButton_clearPlot.clicked.connect(self.clearPlot)
        self.checkBox_axis0Setpoint.clicked.connect(lambda:self.showDataOnPlot(0))
        self.checkBox_axis0Estimated.clicked.connect(lambda:self.showDataOnPlot(1))
#------------ Functions for plotting ---------------------------------------------------------
    def showDataOnPlot(self,id):
        #for id in range(0 ,len(self.graphWidget.getPlotItem().items)):
        if (self.checkBox_axis0Estimated.isChecked()):  
            print("Axis "+str(id) +"Checked")          
            self.graphWidget.getPlotItem().items[0].setVisible(True)

        if (self.checkBox_axis0Estimated.isChecked()) == False:        
            print("Axis"+str(id) +"NOT Checked")  
            self.graphWidget.getPlotItem().items[0].setVisible(False)

        if self.checkBox_axis0Setpoint.isChecked() :
            print("Axis 1 Checked")  
            self.graphWidget.getPlotItem().items[1].setVisible(True)

        if self.checkBox_axis0Setpoint.isChecked()  == False:
            print("Axis 1 NOT Checked")  
            self.graphWidget.getPlotItem().items[1].setVisible(False)

    def clearPlot(self):
        self.graphWidget.getPlotItem().items[0].setVisible(False)
        # self.graphWidget.clear()

    def plotOdriveData(self): #update_plot_data
        if hasattr(self, 'odrv0' ) == True:
            try:
                # self.plotAxisX = self.plotAxisX[1:]  # Remove the first y element.
                self.plotAxisX.append(self.plotAxisX[-1] + 1)  # Add a new value 1 higher than the last.       
                # self.y = self.y[1:]  # Remove the first 
                # self.axis0_encoder_pos_estimate.append( random.uniform(0,100))  # Add a new random value.
                #self.axis0_encoder_pos_estimate.append(self.axis0_encoder_pos_estimate[-1])  # Add a new random value.
                #self.axis0_encoder_pos_estimate.append(self.odrv0.axis0.encoder.pos_estimate)
                pos = self.odrv0.axis1.encoder.pos_estimate
                pos2 = self.odrv0.axis1.controller.pos_setpoint
                vel = self.odrv0.axis1.encoder.vel_estimate
                vel2 = self.odrv0.axis1.controller.vel_setpoint
                self.axis0_encoder_pos_estimate.append(pos)
                self.axis0_controller_pos_setpoint.append(pos2)
                self.axis0_encoder_vel_estimate.append(vel)
                #print(self.odrv0.axis0.controller.vel_setpoint)
                self.axis0_controller_vel_setpoint.append(vel2)
                #self.odrv0.axis0.controller.pos_setpoint(pos2)
                #print(self.axis0_encoder_pos_estimate)
                self.data_line.setData(self.plotAxisX , self.axis0_encoder_pos_estimate)  # Update the data.
                self.data_line2.setData(self.plotAxisX, self.axis0_controller_pos_setpoint)  # Update the data.
                self.data_line3.setData(self.plotAxisX, self.axis0_encoder_vel_estimate)
                self.data_line4.setData(self.plotAxisX, self.axis0_controller_vel_setpoint)
            except:
                pass
    
    def plot(self, X, Y):
        # self.graphWidget.plot(X ,Y)
        self.data_line.setData(X, Y)  # Update the data.
#---------------- END Plotting ---------------------------------------------------------------

#-------------------- Other Functions --------------------------------------------------------

    def mapFromPosAndRowToSetPoints(self,pos,row): 
        xOffset_mm = 0
        yOffset_mm = 100
        plantXCC_mm = 35.1
        plantYCC_mm = 30
        trayWidth_mm = 352
        xOffsetBetweenRows_mm = 17.55
        if pos == 1:
            x_mm=xOffset_mm
        elif pos == 2:
            x_mm = xOffset_mm + plantXCC_mm
        elif pos == 3:
            x_mm = xOffset_mm + trayWidth_mm
        else: # 4
            x_mm = xOffset_mm + trayWidth_mm + plantXCC_mm
        if not row % 2:# For even row number. Jackpot has an zigg zagg pattern
            x_mm = x_mm + xOffsetBetweenRows_mm
        
        y_mm = yOffset_mm + row*plantYCC_mm - plantYCC_mm + math.floor(row/8)*6
        mmToRevolutions = 1/(25*math.pi)
        x_revolutions = x_mm * mmToRevolutions
        y_revolutions = y_mm * mmToRevolutions
        return x_revolutions, y_revolutions

    def goToPosition(self,pos,row):
        self.treeWidget.setGroupOfTreesToInProgress(pos,row)
        x,y = self.mapFromPosAndRowToSetPoints(pos,row)
        string = "X coordinate: {}, Y coordinate: {}".format(x,y)
        
        self.odrv0.axis0.controller.input_pos = x
        self.odrv0.axis1.controller.input_pos = y
        print(string)

    def collectingTrees(self):
        for n in range(1,5):
            for i in range(1,5):
                self.tab_5.setGroupOfTreesToInProgress(n,i)
                time.sleep(0.1)
                self.tab_5.update()
            
    def startWorkers(self):
        try:
            worker_mqtt = Worker(self.mqttInitiate)
            self.threadpool.start(worker_mqtt)
            worker = Worker(self.readXboxInput.readXboxInput)
            worker.signals.result.connect(self.xboxMove)
            worker.signals.finished.connect(self.startWorkers)
            # worker.signals.progress.connect(self.progress_fn)
            self.threadpool.start(worker)
        except Exception as exp:
            print(exp) 
        # pass

    def progress_fn(self,n):
        print(n)

    def xboxMove(self,key):
        # print("hhejeje")
        print(key)
        if key[0] == "Down":
            self.moveDown()
        elif key[0] == "Up":
            self.moveUp()
        elif key[0] == "Right":
            self.moveRight()
        elif key[0] == "Left":
            self.moveLeft()
        elif key[0] == "A":
            self.moveHome()
        # self.startWorkers()

    def mqttInitiate(self):
        try:
            self.client.connect(broker,broker_port)#connect
            self.client.loop_start() #start loop to process received messages
        except Exception as exp:
            print(exp)


# ------------------- Functions for autonomous mode ------------------------------------------
    def checkIfInPos(self):
        setpointX = self.odrv0.axis0.controller.pos_setpoint
        positionX = self.odrv0.axis0.encoder.pos_estimate
        errorX = abs(setpointX - positionX)
        tolerance = 0.1
        if errorX < tolerance:
            xInPos = True
        else:
            xInPos = False
        setpointY = self.odrv0.axis1.controller.pos_setpoint
        positionY = self.odrv0.axis1.encoder.pos_estimate
        errorY = abs(setpointY - positionY)
        if errorY < tolerance:
            yInPos = True
        else: 
            yInPos = False
        return (xInPos and yInPos)

    def goToStart(self):
        mmToRevolutions = 1/(25*math.pi)
        self.odrv0.axis1.controller.input_pos = 50*mmToRevolutions
        print("going to start of column")
        while not self.checkIfInPos():
            pass

    def goToBuffer(self):
        mmToRevolutions = 1/(25*math.pi)
        self.odrv0.axis1.controller.input_pos = 0.7
        self.odrv0.axis0.controller.input_pos = 5.8
        while not self.checkIfInPos():
            pass

    def auto(self):    
        pos = 1
        row = 1
        sleepTime = 1.0
        self.zAxis.sendMessage("r")  
        time.sleep(2*sleepTime)  
        self.goToBuffer()
        self.movezAxis("Home", 0)
        time.sleep(10*sleepTime)
        self.movezAxis("Down",100)
        time.sleep(6*sleepTime)
        while self.controllerMode == "Auto":
            
            self.goToPosition(pos,row)# go to desired position
            while not self.checkIfInPos():
                pass

            print("moving Z down...")
            self.movezAxis("Down",10) # Move down
            time.sleep(0.5*sleepTime)

            print("Gripping plants...")
            self.zAxis.sendMessage("g7")#closing gripper
            time.sleep(4*sleepTime)

            print("Moving Z up...")
            self.movezAxis("Up",110) # Move up
            time.sleep(6*sleepTime)

            print("Trees are correctly gripped")

            self.goToStart()
            time.sleep(1*sleepTime)
            
            self.goToBuffer()
            print("dropping plants into buffer")
            self.movezAxis("Down",110) # Move down
            time.sleep(6*sleepTime)
            self.zAxis.sendMessage("g-7")
            time.sleep(4*sleepTime)
            self.odrv0.axis1.controller.input_pos = -0.5
            time.sleep(1*sleepTime)
            self.movezAxis("Up",10) # Move up
            time.sleep(0.5*sleepTime)

            # self.odrv0.axis0.controller.input_pos = 5.8
            if pos == 4:
                pos = 1
                if row == 35:
                    print("Done picking all plants")
                    pos = 1
                    row = 1
                    self.controllerMode == "Manual"
                    break
                else:
                    row = row + 1                  
            else:
                pos = pos + 1
               
    def startAuto(self):
        worker = Worker(self.auto)
        self.threadpool.start(worker)
        # worker.signals.result.connect(self.xboxMove)

# ------------------- Functions for Connecting Odrive ----------------------------------------
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
        try:
            odrv0 = odrive.find_any()
        except Exception as ex:
            print(ex)
        #print("odrive connected")
        self.odriveConnect.setText("odrive connected")
        self.odriveConnect.adjustSize()        
        return odrv0

# ------------------- Functions for Odrive such as Error and settings ------------------------
    def calibrateEncoder(self, axis):
        if hasattr(self, 'odrv0' ) == True:
            if axis == 0:
                self.odrv0.axis0.requested_state = 7 # encoder offset 
            elif axis == 1:
                self.odrv0.axis1.requested_state = 7 # encoder offset 

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
             # calling to check endstopps, 200ms Timer is ok
            self.checkEndstops()          
        except:
            pass

    def checkEndstops(self):
        try:            
            if self.odrv0.axis0.min_endstop.endstop_state == True:                
                self.endStop_Axis0_Min.setStyleSheet('background-color:red')
            else:
                self.endStop_Axis0_Min.setStyleSheet('background-color:rgb(0, 255, 0)')

            if self.odrv0.axis1.min_endstop.endstop_state == True:
                self.endStop_Axis1_Min.setStyleSheet('background-color:red')
            else:
                self.endStop_Axis1_Min.setStyleSheet('background-color:rgb(0, 255, 0)')
            
            if self.odrv0.axis0.max_endstop.endstop_state == True:                
                self.endStop_Axis0_Max.setStyleSheet('background-color:red')
            else:
                self.endStop_Axis0_Max.setStyleSheet('background-color:rgb(0, 255, 0)')

            if self.odrv0.axis1.max_endstop.endstop_state == True:
                self.endStop_Axis1_Max.setStyleSheet('background-color:red')
            else:
                self.endStop_Axis1_Max.setStyleSheet('background-color:rgb(0, 255, 0)')

        except Exception as ex:
            pass

    def rebootOdrive(self):
        try:
            self.odrv0.reboot()
            self.closedLoopAxis0CheckBox.stateChanged(1)
        except:
            pass
        
    def resetErrorOdrive(self):
        print("Resetting Odrive")
        try:
            #self.odrv0.reboot()
            self.odrv0.axis0.clear_errors()
            self.odrv0.axis1.clear_errors()
            self.closedLoopAxis0CheckBox.stateChanged(1)
        except:
            pass

    def saveOdriveSettings(self):
        print("saving odrive settings")
        try:
            self.odrv0.save_configuration()
        except:
            pass
        
        #self.settingsButtons

    def controlMode(self):
        if self.pushButton_Auto_Manual.text() == "Auto":
            self.controllerMode = "Manual"
            self.pushButton_Auto_Manual.setText("Manual")
        else:
            if hasattr(self, 'odrv0' ) == True:
                self.startAuto()
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
            # publish to mqtt
            if hasattr(self, 'client' ) == True:
                self.client.publish("oDrive/batteryVoltage",chargeLevel)#publish
        except:
            pass

# ------------------- Functions for Odrive control parameters --------------------------------
    # Should Probalby be event base, such as "upon change value"
    def checkParameter(self, input):
       if hasattr(self, 'odrv0' ) == True:
           #----------- Axis0 --------------
            if input == "Check current limit Axis0":
                showValue = self.odrv0.axis0.motor.config.current_lim
            elif input == "Check velocity limit Axis0":
                showValue = self.odrv0.axis0.controller.config.vel_limit
            #----------- Axis1 --------------
            elif input == "Check velocity limit Axis1":
                showValue = self.odrv0.axis1.controller.config.vel_limit

            self.lcd_checkParameter.setProperty("value",showValue)
            self.comboBox_CheckParameter.adjustSize()    

    def odriveVelocityLimit(self,axis):
        max_velX = self.velocityLimitX.value()
        max_velY = self.velocityLimitY.value()
        vel_gain = self.gainVelController.value() 
        self.lcd_velX.setProperty("value",max_velX)
        try:
            pass
            # self.odrv0.axis0.controller.config.pos_gain = self.gainPosController.value()
            if axis == 1:
                self.odrv0.axis1.controller.config.vel_limit = max_velX 
                self.lcd_velX.setProperty("value",self.odrv0.axis1.controller.config.vel_limit)
            elif axis == 0:
                self.odrv0.axis0.controller.config.vel_limit = max_velY 
                self.lcd_velY.setProperty("value",self.odrv0.axis0.controller.config.vel_limit)
            # self.odrv0.axis0.controller.config.vel_gain  = vel_gain
        except:
            pass
            # print("set limits not completed")
     
#-------------------- Functions For Moving The Axis ------------------------------------------
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
            self.odrv0.axis0.controller.input_pos = 0
            self.odrv0.axis1.controller.input_pos = 0
        except:
            pass
 
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

#-------------------- Functions For Moving The Z-Axis ------------------------------
    def movezAxis(self, direction, length):
        try:
            if hasattr(self, 'zAxis' ) == True:
                if direction == "Down":
                    self.zAxis.sendMessage("z"+str(length))
                    # self.zAxis.sendMessage("g"+str(length))
                    self.lcd_zAxis.setProperty("value",(self.lcd_zAxis.value() - length))              
                    #print(direction + (str(length)))
                elif direction == "Up":
                    self.zAxis.sendMessage("z-"+str(length))
                    # self.zAxis.sendMessage("g-"+str(length))
                    self.lcd_zAxis.setProperty("value",(self.lcd_zAxis.value() + length))  
                    #print(direction + (str(length)))
                elif direction == "Home":                
                    self.zAxis.sendMessage(direction)
                    # self.zAxis.sendMessage("r")
                    self.lcd_zAxis.setProperty("value",-10)
                    print("Homeing Z")
        except Exception as ex:
            print(ex)
            # print("Arduino for zAxis not regonized, check connection, port and baud rate!")

        # except:
        #     print("Arduino for zAxis not regonized, check connection, port and baud rate!")




def main():
    global window
    app = QtWidgets.QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    print(width)
    print(height)
    window = MainWindow(width,height)
    # window.setMaximumWidth(width)
    # window.setMaximumHeight(height)
    # window.setMinimumWidth(width)
    # window.setMinimumHeight(height)
    
    #global b 
    #b = MainWindow()
    #b= QtWidgets.QApplication.processEvents()
    #window.show()       
    sys.exit(app.exec_())    
    
if __name__ == '__main__':   
    #while(True):
     #   print("hej")     
    main()



# ---------------------------------------------------------------------------
# --------------- Different Approach to Threads, more RTOS based! ----------
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
# ---------------------------------------------------------------------------
