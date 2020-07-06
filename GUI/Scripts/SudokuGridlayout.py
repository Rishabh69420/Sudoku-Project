import SudokuClass
from PyQt5 import QtCore, QtGui, QtWidgets
from collections import namedtuple
from random import randint, choice        #only for testing, remove later

'''
Work remaining -
  -> Make custom QLineInput class without background and a fixed size - ✔
  ->Grid Lines around numbers  - ✔
  ->Text Formatting (font, font size etc) and repositioning to the exact center - ✔
  ->'Submit Answer' button 
  ->Timer?? 
  ->Link mainmenu Play button to this file
and probably some more stuff
'''

'''Custom Text Label class for all the numbers which will be fixed in a place'''
class FixedDisplayNumbers(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.resize(45,45)
        self.setMaximumHeight(45)
        self.setMaximumWidth(45)

        font = QtGui.QFont("Futurist Fixed-width", 17)
        self.setFont(font)
        self.setAlignment(QtCore.Qt.AlignCenter)

        self.setStyleSheet("* { border: 1px solid black; }")

'''Custom Line Edit class for all the blanks user will have to input into'''
class UserInputBox(QtWidgets.QLineEdit):
    def __init__(self):
        super().__init__()                                 #resized
        self.resize(45,45)
        self.setMaximumHeight(45)
        self.setMaximumWidth(45)

        font = QtGui.QFont("Futurist Fixed-width", 17)      #font, size, alignment
        self.setFont(font)
        self.setAlignment(QtCore.Qt.AlignCenter)

        self.setValidator(QtGui.QIntValidator())             #only integers allowed in textbox
        self.setMaxLength(1)          #will not allow multiple numbers

        self.setStyleSheet("* { background-color: rgba(0, 0, 0, 0); }* { border: 1px solid black; }* { color: rgb(255, 255, 255); }QLineEdit::hover\n"
"{\n"
"border : 3px solid white;\n"
"}")

    
'''
Class for Sudoku window.
REMEMBER TO GIVE A SUDOKU BOARD PARAMETER WHILE CREATING Sudoku object!!
'''
class SudokuMainWindow(object):
    def __init__(self, board):
        super().__init__()
        self.board = board
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(448, 532)
        MainWindow.setFixedSize(448, 532)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.sudoku_background_label = QtWidgets.QLabel(self.centralwidget)   #
        self.sudoku_background_label.setGeometry(QtCore.QRect(-10, 0, 461, 521))
        self.sudoku_background_label.setText("")
        self.sudoku_background_label.setPixmap(QtGui.QPixmap("GUI/Resources/sudoku-grid.png"))
        self.sudoku_background_label.setScaledContents(True)
        self.sudoku_background_label.setObjectName("sudoku_background_label")

        #displaying the numbers using a grid layout
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 20, 400, 400))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setSpacing(0)

        """namedtuple 'coordinate' which stores x and y coordinates to where the labels or textboxes are filled in.
        x coordinate -> column number
        y coordinate -> row number"""

        coordinate = namedtuple("coordinate", "x y")               
        current_coords = coordinate(0, 0)
        while current_coords.y <= 8:    #iterating row-wise
            row = self.board[current_coords.y]
            for i in row:          #iterating through each row, column-wise
                if i is not None:       #Nones represent values that user will have to fill in
                    label = FixedDisplayNumbers()
                    label.setNum(i)
                    self.gridLayout.addWidget(label, current_coords.y, current_coords.x)
                    current_coords = coordinate(current_coords.x + 1, current_coords.y)     #increasing column number so that next val goes into the next column
                else:
                    textInput = UserInputBox()
                    self.gridLayout.addWidget(textInput,current_coords.y, current_coords.x)
                    current_coords = coordinate(current_coords.x + 1, current_coords.y)
            current_coords = coordinate(x = 0, y = current_coords.y + 1)

    
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 448, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sudoku!"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    BOARD = []
    #testing
    Test_Sudoku_Object = SudokuClass.Sudoku()
    for i in Test_Sudoku_Object:
        for j in i:
            j.set_value(choice([randint(1,9),None]))
    
    for i in Test_Sudoku_Object.get_all_rows():
        BOARD.append(list(map(SudokuClass._Element.get_value, i)))
    
    ui = SudokuMainWindow(BOARD)           #Always pass a board parameter!

    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
