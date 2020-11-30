import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import numpy

################### USAGE
# use TreeHive.createTrees to create a set of trees. It takes 6 optional arguments. 

#use TreeHive.setGroupOfTreesToInProgress to set the icons of 5 trees to the loading icon.
#use TreeHive.setGroupOfTreesToRemoved to set the icons of 5 trees to the loading icon.
#They both take two arguments, the first argument is Position (there are 4 gripper positions (1,2,3,4) since we grab 5 trees and have 20 trees in a row)
#and the second argument is Row (A row here is actually the column in the matrix of trees)

class TreeHive(QWidget):
    def __init__(self,*args,x=50,y=50,iconsize=25,CCx=30,CCy=30,rows=20,columns=35):
        super(QWidget,self).__init__(*args)
        #self.createTrees(x,y,iconsize,CC,rows,columns)
        self.iconArray = numpy.full((100,100),QLabel(self))
    def createTrees(self, x, y, iconsize, CCx,CCy, rows, columns):
        self.iconArray = numpy.full((rows,columns),QLabel(self))
        for i in range(self.iconArray.shape[1]):
            for j in range(self.iconArray.shape[0]):
                self.iconArray[j,i]=QLabel(self)
                self.iconArray[j,i].setPixmap(QPixmap("images/pine-tree.png"))
                self.iconArray[j,i].setGeometry(x + CCx*i, y + CCy*j, iconsize, iconsize)
                self.iconArray[j,i].setScaledContents(True)
        

    def setGroupOfTreesToInProgress(self, Pos, Row):
        x = self.translateGripperPosToCoordinates(Pos)
        y = self.InvertRowNumbers(Row)
        print("Going to Position {} in row {}".format(Pos, Row))
        self.iconArray[x, y].setPixmap(QPixmap("images/loading.png"))
        self.iconArray[x+2, y].setPixmap(QPixmap("images/loading.png"))
        self.iconArray[x+4, y].setPixmap(QPixmap("images/loading.png"))
        self.iconArray[x+6, y].setPixmap(QPixmap("images/loading.png"))
        self.iconArray[x+8, y].setPixmap(QPixmap("images/loading.png"))
    
    def setGroupOfTreesToRemoved(self, Pos, Row):
        x = self.translateGripperPosToCoordinates(Pos)
        y = self.InvertRowNumbers(Row)
        print("Going to Position {} in row {}".format(Pos, Row))
        self.iconArray[x, y].setPixmap(QPixmap("images/record.png"))
        self.iconArray[x+2, y].setPixmap(QPixmap("images/record.png"))
        self.iconArray[x+4, y].setPixmap(QPixmap("images/record.png"))
        self.iconArray[x+6, y].setPixmap(QPixmap("images/record.png"))
        self.iconArray[x+8, y].setPixmap(QPixmap("images/record.png"))

    def translateGripperPosToCoordinates(self,Pos):
        if Pos == 1:
            x = 0 
        elif Pos == 2:
            x = 1
        elif Pos == 3:
            x =10
        else:
            x = 11
        return x

    def InvertRowNumbers(self, Row):
        return 35 - Row

    

    

def main():
    App = QApplication(sys.argv)
    window = TreeHive(y=10,x=10)
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()
