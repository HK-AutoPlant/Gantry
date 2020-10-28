#!/usr/bin/env python3
# -*- conding: utf-8 -*-

import os, sys, urllib.request, json
import PyQt5.QtQml
from PyQt5.QtQuick import QQuickView
from PyQt5.QtCore import QStringListModel, Qt, QUrl
from PyQt5.QtGui import QGuiApplication

if __name__ == '__main__':

    #get our data
    url = "http://country.io/names.json"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))

    #Format and sort the data
    data_list = list(data.values())
    data_list.sort()

    #Set up the application window
    app = QGuiApplication(sys.argv)
    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)

    #Expose the list to the Qml code
    my_model = QStringListModel()
    my_model.setStringList(data_list)
    view.rootContext().setContextProperty("myModel",my_model)

    #Load the QML file
    qml_file = os.path.join(os.path.dirname(__file__),"test.ui.qml")
    view.setSource(QUrl.fromLocalFile(os.path.abspath(qml_file)))

    #Show the window
    if view.status() == QQuickView.Error:
        sys.exit(-1)
    view.show()