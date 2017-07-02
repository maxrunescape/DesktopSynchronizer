import sys
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, qApp, QAction

from game import Board

class Client(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):   

        menu = self.menuBar()
        file = menu.addMenu('File')
        
        new_game = QAction('New Game', menu)
        new_game.setShortcut('N')
        file.addAction(new_game)

        quit = QAction('Quit', menu)
        quit.setShortcut('B')
        quit.triggered.connect(qApp.quit)
        file.addAction(quit)

        file.triggered[QAction].connect(self.processtrigger)

        self.tboard = Board(self)
        self.setCentralWidget(self.tboard)

        self.statusbar = self.statusBar()        
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)

        self.resize(360, 760)
        self.center()
        self.setWindowTitle('Tetris')        
        self.show()

    def processtrigger(self, action):
        print(action.text()+" is triggered")
        if action.text() == 'New Game':
            self.tboard.start()

    def center(self):
        
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, 
            (screen.height()-size.height())/2)


class Shape(object):
    
    coordsTable = (
        ((0, 0),     (0, 0),     (0, 0),     (0, 0)),
        ((0, -1),    (0, 0),     (-1, 0),    (-1, 1)),
        ((0, -1),    (0, 0),     (1, 0),     (1, 1)),
        ((0, -1),    (0, 0),     (0, 1),     (0, 2)),
        ((-1, 0),    (0, 0),     (1, 0),     (0, 1)),
        ((0, 0),     (1, 0),     (0, 1),     (1, 1)),
        ((-1, -1),   (0, -1),    (0, 0),     (0, 1)),
        ((1, -1),    (0, -1),    (0, 0),     (0, 1))
    )

    def __init__(self):
        
        self.coords = [[0,0] for i in range(4)]
        self.pieceShape = Tetrominoe.NoShape

        self.setShape(Tetrominoe.NoShape)
        

    def shape(self):
        return self.pieceShape
        

    def setShape(self, shape):
        
        table = Shape.coordsTable[shape]
        
        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]

        self.pieceShape = shape
        

    def setRandomShape(self):
        self.setShape(random.randint(1, 7))

        
    def x(self, index):
        return self.coords[index][0]

        
    def y(self, index):
        return self.coords[index][1]

        
    def setX(self, index, x):
        self.coords[index][0] = x

        
    def setY(self, index, y):
        self.coords[index][1] = y

        
    def minX(self):
        
        m = self.coords[0][0]
        for i in range(4):
            m = min(m, self.coords[i][0])

        return m

        
    def maxX(self):
        
        m = self.coords[0][0]
        for i in range(4):
            m = max(m, self.coords[i][0])

        return m

        
    def minY(self):
        
        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1])

        return m

        
    def maxY(self):
        
        m = self.coords[0][1]
        for i in range(4):
            m = max(m, self.coords[i][1])

        return m

        
    def rotateLeft(self):
        
        if self.pieceShape == Tetrominoe.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape
        
        for i in range(4):
            
            result.setX(i, self.y(i))
            result.setY(i, -self.x(i))

        return result

        
    def rotateRight(self):
        
        if self.pieceShape == Tetrominoe.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape
        
        for i in range(4):
            
            result.setX(i, -self.y(i))
            result.setY(i, self.x(i))

        return result




if __name__ == '__main__':
    
    app = QApplication([])
    client = Client()    
    sys.exit(app.exec_())