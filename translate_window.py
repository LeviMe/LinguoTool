#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 11 09:19:48 2022

@author: levi
"""

from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel,QTextEdit,\
    QVBoxLayout, QScrollArea,QHBoxLayout, QLineEdit,QDesktopWidget, QPushButton, QSizePolicy
from PyQt5.QtGui import QFont, QIcon, QTextOption, QPalette, QColor,QFontDatabase
from PyQt5.QtCore import QCoreApplication, Qt, QSize

import examples_loader

SIZE = 800



class ButtonSel(QPushButton):
    def __init__(self, icon, name):
        super().__init__()
        self.icon = icon
        self.name = name
        self.setIcon(QIcon(icon))
        self.setIconSize(QSize(30, 30))
        self.setMaximumWidth(110)


class LangSel_bar(QHBoxLayout):
    def __init__(self):
        super(LangSel_bar, self).__init__()
        
        b_dict = {"French" :"icons/france.png", "English":"icons/uk.png",\
         "German":"icons/germany.png", "reverse":"icons/reverse.png" }
        
        self.B_dict = {}
        for b in b_dict:
            self.B_dict[b] = ButtonSel(b_dict[b], b)       
        self.B_dict["reverse"].setMaximumWidth(35)
        
        self.source = "German"
        self.target = "English"
        self.source_label = QLabel(self.source)
        self.target_label = QLabel(self.target)
        
        for label in [self.source_label, self.target_label]:
            f0 = QFont("Segoe UI", 16) #, QFont.Bold, False)
            label.setFont(f0)
            label.setStyleSheet("QLabel { color : blue}")
            label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            
        for w in [self.source_label,self.B_dict["reverse"], self.target_label, \
                  self.B_dict["English"],self.B_dict["German"],self.B_dict["French"]]:
            self.addWidget(w)
            
    
    def update_lang(self, source, target):
        self.source, self.target = source, target
        self.source_label.setText(self.source)
        self.target_label.setText(self.target)
        self.source_label.update()
        self.target_label.update()
        
        

class TranslationField(QHBoxLayout):
        
    def __init__(self, tr_function, index=0, font_name="Arial", size=12, bold=False):
        super(TranslationField, self).__init__()
        col1 = "#B4ECF4"
        col2 = "#C1FADE"
        font_id_1 = QFontDatabase.addApplicationFont("./fonts/Roboto/Roboto-Medium.ttf")
        font_1 = QFontDatabase.applicationFontFamilies(font_id_1)[0]
        
        self.tr_function = tr_function
        
        self.inpText = QLineEdit()
        #inpText.setContentsMargins(20, 5, 20, 5)
        #inpText.setText(text1)
        self.inpText.setStyleSheet("QLineEdit { background:"+col1+"; selection-background-color: #000000; }")
        f0 = QFont(font_1, size) #, QFont.Bold, False)
        self.inpText.setFont(f0)
        #self.inpText.setText("")
        self.outpText = QLabel()
        self.outpText.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
      #  self.outpText.setMaximumHeight(5*size)
       # inpText.setContentsMargins(20, 5, 20, 5) #left, top, right, bottom
        self.outpText.setWordWrap(True)

      #  self.outpText.setMaximumHeight(60)
        #self.outpText.setText("")
       # outpText.setMinimumWidth(int(SIZE*.88))
       # outpText.setMaximumWidth(int(SIZE*.88))
        self.outpText.setContentsMargins(20, 5, 20, 5) #left, top, right, bottom
        self.outpText.setTextInteractionFlags(Qt.TextSelectableByMouse)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(col2))
        palette.setColor(QPalette.WindowText,  QColor("#000000"))
        self.outpText.setAutoFillBackground(True)
        self.outpText.setPalette(palette)
        f1 = QFont(font_1, size)
     #   if bold: f1.setBold(True)
        self.outpText.setFont(f1)
        
        TElement = QVBoxLayout()
        TElement.setSpacing(5)
        TElement.addWidget(self.inpText)
        TElement.addWidget(self.outpText)

#################################################################################        
        self.button = QPushButton()
        self.button.setMaximumHeight(45)
        self.button.setIcon(QIcon('icons/star.png'))
        self.button.setIconSize(QSize(35, 35))
        self.button.clicked.connect(self.change_status)
        self.button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)        
        self.status = False
          
        self.addLayout(TElement)
        self.addWidget(self.button)
        
        
    def translate(self):
        text = self.inpText.text()
        tr_text = self.tr_function(text)
        #print(tr_text)
        self.outpText.setText(tr_text)

        
        
    def change_status(self):
        self.status = not self.status
        if (self.status):
            self.button.setIcon(QIcon('icons/star2.png'))
        else:
            self.button.setIcon(QIcon('icons/star.png'))



class Window(QMainWindow):
    """
    __init__ : Initialize the window
    This function sets up the window's properties such as title, size, and it calls the initUI() function. 
    """ 
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Translate a list of items')
        
        self.width, self.height = SIZE, int(SIZE*.9)
        self.resize(self.width, self.height)
        #self.center_window()
        
        self.list_sentences = []
        self.list_labels = []
        self.list_TField = []
        
        self.source_lang = "German"
        self.target_lang = "English"
        self.loader = examples_loader.examples_loader(\
            source = self.source_lang , target =self.target_lang)
        self.tr_function = self.loader.translateG 
        
        self.indexCurrent = 0
        self.initUI()
        
        
    
    def updateSearch(self, index):
       # print("appel update search", index)
        self.indexCurrent = index
        currentField = self.list_TField[self.indexCurrent]
        currentField.translate()
        
        indexNext = self.indexCurrent + 1
        if self.indexCurrent == len(self.list_TField)-1:
         #   print("sur le dernier ", self.indexCurrent)
            nextField = TranslationField(self.tr_function,indexNext)
           # nextField.inpText.setText("champ #"+str(indexNext))
            nextField.inpText.returnPressed.connect(lambda: self.updateSearch(indexNext))            
            self.scroll_layout.addLayout(nextField)
            self.list_TField += [nextField]
            
        self.list_TField[indexNext].inpText.setFocus()
       # self.indexCurrent=indexNext
            
            
       
    def react_buttons(self):
        name = self.sender().name
        update_flag = False
        if name in ["English", "French", "German"] and name != self.source_lang:
            self.target_lang = name
            update_flag = True
        if name == "reverse":
            self.target_lang, self.source_lang = self.source_lang, self.target_lang
            update_flag = True
        if update_flag:
            self.loader.update_param(self.source_lang, self.target_lang)
            self.langSel_bar.update_lang(self.source_lang, self.target_lang)
      

    """
    initUI : initialize the user interface
    This function sets up all of the elements of the user interface such as the search bar, scroll area, etc.
    """
    def initUI(self):
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)


        ######################################################   
        self.langSel_bar = LangSel_bar()
        
        B_dict = self.langSel_bar.B_dict
        for b in B_dict:
            B_dict[b].clicked.connect(self.react_buttons)
                
        self.main_layout.addLayout(self.langSel_bar)
        ######################################################
        

        self.scroll_widget = QWidget(self)
        self.main_layout.addWidget(self.scroll_widget)
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setSpacing(10) 
        self.scroll_layout.setAlignment(Qt.AlignTop)

        field_0 = TranslationField(self.tr_function,0) 

        #field_0.setAlignment(Qt.AlignTop)           
        field_0.inpText.returnPressed.connect(lambda: self.updateSearch(0))
        self.list_TField = [field_0]
        self.scroll_layout.addLayout(field_0)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_layout_2 = QHBoxLayout(self.main_widget)
        self.scroll_layout_2.addWidget(self.scroll_area)
        self.main_layout.addLayout(self.scroll_layout_2)
        

    """
    quitApp : quit the application
    This function quits the application when called.
    """
    
    def quitApp(self):
        QCoreApplication.instance().quit()



##############################################################################

import sys
from PyQt5.QtWidgets import  QApplication
import translate_window


app=0 # necessaire crash
app = QApplication([])
app.setStyle('Fusion')
app.aboutToQuit.connect(app.deleteLater)
dow = translate_window.Window()
dow.show()


sys.exit(app.exec())
app.exit()


