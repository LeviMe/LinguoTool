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

SIZE = 960



def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        if item.widget() is not None:
            item.widget().deleteLater()
            
        if item.layout() is not None:
            clear_layout(item)
           #item.layout().deleteLater()
            #item.setParent(None)


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
            font_id_1 = QFontDatabase.addApplicationFont("./fonts/Roboto/Roboto-Medium.ttf")
            font_1 = QFontDatabase.applicationFontFamilies(font_id_1)[0]
            f0 = QFont(font_1, 16) #, QFont.Bold, False) # auparavant "Segoe UI"
            label.setFont(f0)
            label.setStyleSheet("QLabel { color : #111111}")
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


class CustomTextEdit(QTextEdit):
    def __init__(self, col1, col2, font_name="Arial", size=12):
        super(QTextEdit, self).__init__()  
        
        self.setFixedWidth(int(SIZE*.9))
        self.setMaximumHeight(60)
        self.setWordWrapMode(QTextOption.WordWrap)   
        self.textChanged.connect(self.updateText)
        
        self.text1.setStyleSheet("QTextEdit { background: {0}; selection-background-color: {1}; }".format(col1, col2))
        f0 = QFont(font_name, size, QFont.Bold, False)
        self.text1.setFont(f0)
        
        #self.setFixedSize(SIZE, 40)
        #self.setText(text1)
        #self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
    def updateText1(self):
          self.setFixedHeight(int(1.2*self.document().size().height()))
        

class LabelResult(QLabel):
    def __init__(self, col1, col2, font_name="Arial", size=12, bold=False):
        super(LabelResult, self).__init__()  
        self.setWordWrap(True)
        self.setMinimumWidth(int(SIZE*.88))
        self.setMaximumWidth(int(SIZE*.88))
        self.setContentsMargins(20, 5, 20, 5) #left, top, right, bottom
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(col1))
        palette.setColor(QPalette.WindowText,  QColor(col2))
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        f1 = QFont(font_name, size)
        if bold: f1.setBold(True)
        self.setFont(f1)
        


    
class Result_bar(QHBoxLayout):    
    def __init__(self, text1, text2):
        super(Result_bar, self).__init__()
        font_id_1 = QFontDatabase.addApplicationFont("./fonts/Roboto/Roboto-Medium.ttf")
        font_1 = QFontDatabase.applicationFontFamilies(font_id_1)[0]
        
        self.text1 = LabelResult("#B4ECF4","#000000", font_name=font_1, size=12, bold=False)
        self.text1.setText(text1)
        
        self.text2 = LabelResult("#D2FCFE","#000000",font_name= "Helvetica",size=11)
        self.text2.setText(text2)
 
        self.button = QPushButton()
        self.button.setFixedSize(QSize(35, 35))
        self.button.setIcon(QIcon('icons/star.png'))
        self.button.setIconSize(QSize(30, 30))
        self.button.clicked.connect(self.change_status)
        
        self.status = False
        
        # Add Widgets to Layout        
        v_layout = QVBoxLayout()
        v_layout.setSpacing(0) 
        v_layout.addWidget(self.text1)
        v_layout.addWidget(self.text2)
        v_layout.addSpacing(8)

        self.addLayout(v_layout)
        self.addWidget(self.button, alignment= Qt.AlignTop | Qt.AlignLeft)

        self.button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        
        
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
        self.setWindowTitle('My Reverso App with Python/PyQT5')
        
        self.width, self.height = SIZE, int(SIZE*.9)
        self.resize(self.width, self.height)
        self.center_window()
        
        self.list_sentences = []
        self.list_labels = []
        
        self.initUI()
        
        
        self.source_lang = "German"
        self.target_lang = "English"
        self.loader = examples_loader.examples_loader(\
            source = self.source_lang , target =self.target_lang)
        
    
    """
    center_window : center the window on the screen
    This function centers the window on the user's screen by calculating the coordinates 
    of the center of the screen and then placing the window there.    
    """

    def center_window(self):   
        # gros probl??me apr??s maj de Gnome sur Wayland. Ne fonctionne pas

        desktop = QDesktopWidget()
        geometry = desktop.screenGeometry()
       # print(geometry.width(), geometry.height())
        x0 = geometry.width() // 2 - self.width // 2
        y0 = geometry.height() // 2 - self.height // 2
        
        self.setGeometry(x0, y0, self.width, self.height) 
       # print(self.x(), self.y())
      #  self.setFixedSize(self.width, self.height)
      
    """
    launch_search : launch the search
    This function retrieves the text from the search bar, calls the retrieve function from the examples_loader 
    class to get a list of sentences and then passes that list to the load_sentences function.
    """
 
    def launch_search(self):
        text = self.search_bar.text()
        if (text): # eviter barre vide
            list_sentences = self.loader.retrieve(text)
            self.load_sentences(list_sentences)
        

    """
    load_sentences : load the sentences
     This function takes a list of sentences and adds labels to the scroll layout for each sentence. 
     It also sets the font of the labels to either bold or regular based on the language. 
    """
    
    def load_sentences(self, list_sentences):
        self.list_sentences = []
        self.list_sentences = list_sentences 
        
        clear_layout(self.scroll_layout)         

        assert(len(self.list_sentences)%2 == 0)
        for i in range(0, len(self.list_sentences), 2):
            hl = Result_bar(self.list_sentences[i], \
                          self.list_sentences[i+1])
    
            self.scroll_layout.addLayout(hl)

    
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
            self.launch_search()
      

    """
    initUI : initialize the user interface
    This function sets up all of the elements of the user interface such as the search bar, scroll area, etc.
    """
    def initUI(self):
      #  self.setStyleSheet("QMainWindow {background-color: #AAAAAA;}")
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)

        ######################################################
        
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText('Search')
        self.search_bar.setMinimumHeight(40)
        self.search_button = QPushButton("")
        self.search_button.setMinimumSize(40,40)
        self.search_button.setIcon(QIcon('icons/search.png'))
        self.search_button.setIconSize(QSize(35, 35))
        self.search_button.clicked.connect(self.launch_search)
        self.search_bar.returnPressed.connect(self.launch_search)
        h_box = QHBoxLayout()
        h_box.addWidget(self.search_bar)
        h_box.addWidget(self.search_button)
        self.main_layout.addLayout(h_box)
        
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

        self.load_sentences(self.list_sentences)

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
#import translate_window

# ATTENTION LORS D'UN COPIE COLLE LA WINDOW N'est plus la m??me si importation


app=0 # necessaire crash
app = QApplication([])
app.setStyle('Fusion')
app.aboutToQuit.connect(app.deleteLater)
dow = Window()


dow.show()


sys.exit(app.exec())
app.exit()


