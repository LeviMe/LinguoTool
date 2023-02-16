#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 16:26:52 2022

@author: levi
"""

import sys
from PyQt5.QtWidgets import  QApplication
import reverso_window


app=0 # necessaire crash
app = QApplication([])
app.setStyle('Fusion')
app.aboutToQuit.connect(app.deleteLater)
dow = reverso_window.Window()
dow.show()


sys.exit(app.exec())
app.exit()



"""
A relire
https://stackoverflow.com/questions/19459299/running-a-pyqt-application-twice-from-one-prompt-in-spyder
sur les problèmes pour lancer l'appli plusieurs fois depuis Spyder'

"""