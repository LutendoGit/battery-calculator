from PyQt5.QtCore import QRect, QPoint,QStandardPaths,Qt,QTimer,QSizeF,QUrl
from PyQt5.QtGui import QPixmap, QPen,QScreen,QPainter, QPdfWriter,QPagedPaintDevice

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog,QCheckBox,QLabel,QTabWidget
import sys
import os


# Main application class
class ScreenshotTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screenshot Tool")
        self.setGeometry(100, 100, 400, 250)

        # setting up the UI
        central_widget = QWidget()  # first create a central widget
        self.setCentralWidget(central_widget) # set it as the central widget
        layout = QVBoxLayout(central_widget)  # add a layout to the central widget

        
        self.screenshot_button = QPushButton("Take Screenshot")
        self.screenshot_button.setStyleSheet("font-size: 10px; padding: 12px; background-color: #1976d2; color: white; border-radius: 4px;")
        self.screenshot_button.setFixedWidth(95)
        self.screenshot_button.clicked.connect(self.take_screenshot)
        layout.addWidget(self.screenshot_button, alignment=Qt.AlignLeft)

        
       
        
 

    
            
      
   
  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScreenshotTool()
    window.show()
    sys.exit(app.exec_())