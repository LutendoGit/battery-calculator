from PyQt5.QtCore import QRect, QPoint,QStandardPaths,Qt,QTimer,QSizeF,QUrl, QPoint,QTimer 
from PyQt5.QtGui import QPixmap, QPen,QScreen,QPainter, QPdfWriter,QPagedPaintDevice,QKeySequence

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog,QCheckBox,QLabel,QTabWidget,QHBoxLayout,QSizePolicy,QShortcut
import sys
import os


from matplotlib import scale

class FramelessWindow(QMainWindow): # Create a custom frameless window-
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint) # Remove window borders
        self.setAttribute(Qt.WA_TranslucentBackground) # makes the background transparent
        self.setGeometry(50, 50, 50, 50) # Set initial size and position
        self.setStyleSheet("background: transparent; border:none; border-radius: 4px;") # Add a border and rounded corners
        self.oldPos = self.pos() # Store the initial position of the window

        # setting up the UI
        central_widget = QWidget()  # first create a central widget
        self.setCentralWidget(central_widget) # set it as the central widget
        layout = QVBoxLayout(central_widget)  # add a layout to the central widget

        # Add custom title bar
        self.title_bar = QWidget(self)
        self.title_bar.setStyleSheet("background-color: #1976d2; color: white; border-top-left-radius: 4px; border-top-right-radius: 4px;")
        self.title_bar.setFixedHeight(25)  # Set a fixed height for the title bar


        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_label = QLabel("Screenshot Tool")
        title_label.setStyleSheet("font-size: 10px; padding: 2px; color: white;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()

        # Minimize button
        self.mini_button = QPushButton("–")
        self.mini_button.setStyleSheet("font-size: 10px; padding: 2px; color: white; border: none;")
        self.mini_button.setFixedSize(25, 25 )
        self.mini_button.clicked.connect(self.showMinimized)
        title_layout.addWidget(self.mini_button)

        # Maximize/Restore button
        self.maxi_button = QPushButton("🗖" )
        self.maxi_button.setStyleSheet("font-size: 10px; padding: 2px; color: white; border: none;")
        self.maxi_button.setFixedSize(25, 25 )
        self.maxi_button.clicked.connect(self.toggle_maximize)
        title_layout.addWidget(self.maxi_button)

        self.is_maximized = False  # Track maximized state

        # Close button
        self.exit_button = QPushButton("✕")
        self.exit_button.setStyleSheet("font-size: 10px; padding: 2px; color: white; border: none;")
        self.exit_button.setFixedSize(25, 25 )
        self.exit_button.clicked.connect(self.close)
        title_layout.addWidget(self.exit_button)

        

        # Add the title bar to the main layout
        layout.addWidget(self.title_bar)

        # Embed ScreenshotTool
        self.screenshot_ui = ScreenshotTool()
        layout.addWidget(self.screenshot_ui)


        

           # Maximize/Restore button functionality
    def toggle_maximize(self):
        if self.is_maximized:
           self.showNormal()
           self.is_maximized = False
        else:
           self.showMaximized()
           self.is_maximized = True




       


          # Add custom title bar
        #self.title_bar = customTitleBar(self)
        #layout.addWidget(self.title_bar)


         

      

    def mousePressEvent(self, event): # Capture the position when mouse is pressed
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()  # Store the position where the mouse is pressed
            event.accept()
    
    def mouseMoveEvent(self, event): # Move the window when dragging
        if self.oldPos:
            delta = QPoint(event.globalPos() - self.oldPos)  # Calculate the difference
            self.move(self.x() + delta.x(),self.y()+ delta.y()) # Move the window
            self.oldPos = event.globalPos() # Update the old position
    
    def mouseReleaseEvent(self, event): # Reset the old position when the mouse is released
        self.oldPos  = None

"""#adding tittle bar customization here
class customTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        # customizing the title bar
        #self.title_bar = QWidget(self)
        #self.title_bar.setStyleSheet("background-color: grey; color: white;")
        #self.title_bar.setFixedHeight(25)  # Set a fixed height for the title bar

        #layout for the title bar
        #self.setStyleSheet("background-color: grey; color: white;")
        #self.setFixedHeight(25)  # Set a fixed height for the title bar

        layout = QHBoxLayout(self.title_bar)
        layout.setContentsMargins(0, 0, 0, 0)

        #layout.addStretch()

          # creating a custom title bar
        title_bar_label = QLabel("Screenshot Tool")
        title_bar_label.setStyleSheet("font-size: 10px; padding: 2px; color: black; border-top-left-radius: 4px; border-top-right-radius: 4px;")
        layout.addWidget(title_bar_label)
        #layout.addStretch()

        # Minimize button
        self.mini_button = QPushButton("–")
        self.mini_button.setStyleSheet("font-size: 10px; padding: 2px; background-color: grey; color: black; border: none;")
        self.mini_button.setFixedSize(25, 25 )
        self.mini_button.clicked.connect(self.parent.showMinimized)
        layout.addWidget(self.mini_button)

        # Maximize/Restore button
        self.maxi_button = QPushButton("🗖" )
        self.maxi_button.setStyleSheet("font-size: 10px; padding: 2px; background-color: grey; color: black; border: none;")
        self.maxi_button.setFixedSize(25, 25 )
        self.maxi_button.clicked.connect(self.toggle_maximize)
        layout.addWidget(self.maxi_button)

        # Close button
        self.exit_button = QPushButton("✕")
        self.exit_button.setStyleSheet("font-size: 10px; padding: 2px; background-color: grey; color: black; border: none;")
        self.exit_button.setFixedSize(25, 25 )
        self.exit_button.clicked.connect(self.parent.close)
        layout.addWidget(self.exit_button)

        self.is_maximized = False"""

     

# Main application class
class ScreenshotTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screenshot Tool")
        self.setStyleSheet("background-color: white;")
        self.setGeometry(100, 100, 450, 250)
        self.main_layout = QVBoxLayout(self)  # add a layout to the central widget
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        #self.setLayout(self.main_layout)

        # Keyboard shortcuts
        self.screenshot_shortcut = QShortcut(QKeySequence("Ctrl+shift+S"),self)  # define the shortcut sequence for taking screenshot
        self.screenshot_shortcut.setContext(Qt.ApplicationShortcut) # make it work even when the app is not focused
        self.screenshot_shortcut.activated.connect(self.take_screenshot) # connect the shortcut to the take_screenshot method

        # creating the screenshot button
        self.screenshot_button = QPushButton("📸+add")
        self.screenshot_button.setStyleSheet("font-size: 12px; padding: 2px; color: black; border-radius: 4px;")
        self.screenshot_button.setFixedWidth(50)
        self.screenshot_button.clicked.connect(self.take_screenshot)
        self.main_layout.addWidget(self.screenshot_button, alignment=Qt.AlignLeft)

        """"# Preview label
        self.preview_label = QLabel("")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.main_layout.addWidget(self.preview_label)

        # bottom row layout for save button and Discard button
        bottom_row  = QHBoxLayout()
        bottom_row.setContentsMargins(0, 0, 0, 0)

        # Discard button
        self.discard_button = QPushButton("Discard")
        self.discard_button.setStyleSheet("font-size: 10px; padding: 12px; color: white; border-radius: 4px;")
        self.discard_button.clicked.connect(self.discard_screenshot)
        self.discard_button.hide()
        self.discard_button.move(100,0)
        bottom_row.addWidget(self.discard_button,alignment=Qt.AlignBottom|Qt.AlignLeft)


        # save button
        self.save_button  = QPushButton("Save")
        self.save_button.setStyleSheet("font-size: 10px; padding: 12px; color: white; border-radius: 4px;")
        self.save_button.setFixedWidth(50)
        self.save_button.clicked.connect(self.save_screenshot)
        bottom_row.addWidget(self.save_button, alignment=Qt.AlignBottom|Qt.AlignRight)
        self.save_button.setEnabled(False)  # Disable save button initially
        self.save_button.hide() # Hide save button initially
        self.save_button.move(100, 80)"""




    # screenshot functionality
    def take_screenshot(self):
        top_level = self.window()
        if top_level is not None:
            top_level.hide()  # hide the top level  screenshot window not just the embed widget
            print("top_level window is hidden now")
        else:
            self.hide()
        QApplication.processEvents()  # ensuring screenshot window is hidden during capture
        QTimer.singleShot(200, self.capture_screen)  # allowing window to hide for set timer before capture


        #QTimer.singleShot(300, self.show)  # Show the window again after taking the screenshot
        #self.discard_button.setEnabled(True) # Enable discard button after taking screenshot
    def capture_screen(self):
        screen = QApplication.primaryScreen()
        if screen:
            print("screen detected")
            #desktop_id = QApplication.desktop().winId()
            self.screenshot = screen.grabWindow(0)
            print("screenshot taken")

            top_level = self.window()
            if top_level is not None:
                top_level.show()
                print("top level window is restored")
            else:
                self.show()  # Show the window again after taking the screenshot
            #self.resize(1080, 1080)  # Resize window to fit the screenshot
            self.preview_window = screenshot_preview(self.screenshot)
            self.preview_window.show()
            self.preview_window.preview_label.setPixmap(self.screenshot.scaled(self.preview_window.preview_label.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation))
            #self.preview_window.save_button = self.save_button
            #self.save_button.setEnabled(True) # Enable save button after taking screenshot
            #self.save_button.show() # Show save button after taking screenshot
            
            #self.discard_button.show() # Show discard button after taking screenshot 


        else:
            print("No screen detected")

    # save functionality

    ''''def save_screenshot(self):
        options = QFileDialog.Options()
        file_path, _  = QFileDialog.getSaveFileName(self,"save screenshot","","PDF Files (*.pdf);;JPEG Files (*.jpg);;All Files (*)", options=options)
        if file_path:
            if file_path.endswith(".pdf"):
                self.save_as_pdf(file_path)

            elif file_path.endswith(".jpg"):
                    self.save_as_jpeg(file_path)
            else:
                self.screenshot.save(file_path)  # Save in default format if no extension is provided

    def save_as_pdf(self, file_path):
        pdf_writer = QPdfWriter(file_path)
        pdf_writer.setPageSize(QPagedPaintDevice.A4)
        pdf_writer.setResolution(96)

        painter = QPainter(pdf_writer)

        # Get page dimensions
        page_width = pdf_writer.width()
        page_height = pdf_writer.height()

        img_size = self.screenshot.size()
        scale_w = page_width / img_size.width()
        scale_h = page_height / img_size.height()
        scale = min(scale_w, scale_h)

        new_width = img_size.width() * scale
        new_height = img_size.height() * scale
        x = (page_width - new_width) / 2
        y = (page_height - new_height) / 2

        painter.drawPixmap(QRect(int(x), int(y), int(new_width), int(new_height)), self.screenshot)
        painter.end()
        print(f"Screenshot saved as PDF at {file_path}")

    def save_as_jpeg(self, file_path):
            self.screenshot.save(file_path, "JPEG")
            print(f"Screenshot saved as JPEG at {file_path}")

    def discard_screenshot(self):
        self.screenshot = None
        self.preview_label.clear()
        self.preview_label.setText("Screenshot preview will appear here")
        self.save_button.setEnabled(False)
        self.discard_button.setEnabled(False)'''

# screenshot preview window class        
class screenshot_preview(QWidget):
    def __init__(self, screenshot_pixmap):
        super().__init__()
        self.setWindowTitle("Screenshot Preview")
        self.setStyleSheet("background-color: white;")
        self.screenshot = screenshot_pixmap

        # Compute a reasonable initial window size (cap to available screen)
        screen_geom = QApplication.primaryScreen().availableGeometry()
        max_w = int(screen_geom.width() * 0.8)
        max_h = int(screen_geom.height() * 0.8)

        img_w = self.screenshot.width()
        img_h = self.screenshot.height()

        # reserve space for the buttons (bottom bar)
        self.bottom_bar_height = 64
        win_w = min(img_w, max_w)
        win_h = min(img_h, max_h - self.bottom_bar_height) + self.bottom_bar_height
        self.resize(win_w, win_h)

        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(8)

        # Preview label - it will expand and we will keep the pixmap scaled in resizeEvent
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet("background: transparent;")
        self.preview_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.preview_label, stretch=1)

        # set initial pixmap scaled to current label size
        self._update_preview_pixmap()

        # bottom row layout for save and discard buttons inside a fixed-height container
        bottom_widget = QWidget()
        bottom_widget.setFixedHeight(self.bottom_bar_height)
        bottom_row = QHBoxLayout(bottom_widget)
        bottom_row.setContentsMargins(6, 6, 6, 6)
        bottom_row.setSpacing(8)

        # Discard button
        self.discard_button = QPushButton("Discard")
        self.discard_button.setStyleSheet("font-size: 10px; padding: 8px; color: brown; border-radius: 4px;")
        self.discard_button.clicked.connect(self.discard_screenshot)
        bottom_row.addWidget(self.discard_button, alignment=Qt.AlignLeft | Qt.AlignVCenter)

        bottom_row.addStretch()

        # Save button
        self.save_button = QPushButton("Save")
        self.save_button.setStyleSheet("font-size: 10px; padding: 8px; color: green; border-radius: 4px;")
        self.save_button.setFixedWidth(72)
        self.save_button.clicked.connect(self.save_screenshot)
        bottom_row.addWidget(self.save_button, alignment=Qt.AlignRight | Qt.AlignVCenter)

        self.layout.addWidget(bottom_widget)

    def _update_preview_pixmap(self):
        if self.screenshot and not self.preview_label.size().isEmpty():
            scaled = self.screenshot.scaled(self.preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.preview_label.setPixmap(scaled)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Update pixmap to fit the new preview_label size while preserving bottom bar area
        self._update_preview_pixmap()
       
    def save_screenshot(self):
        options = QFileDialog.Options()
        file_path, _  = QFileDialog.getSaveFileName(self,"save screenshot","","PDF Files (*.pdf);;JPEG Files (*.jpg);;All Files (*)", options=options)
        if file_path:
            if file_path.endswith(".pdf"):
                self.save_as_pdf(file_path)

            elif file_path.endswith(".jpg"):
                    self.save_as_jpeg(file_path)
            else:
                self.screenshot.save(file_path)  # Save in default format if no extension is provided
    
    
    def save_as_pdf(self, file_path):
        pdf_writer = QPdfWriter(file_path)
        pdf_writer.setPageSize(QPagedPaintDevice.A4)
        pdf_writer.setResolution(96)

        painter = QPainter(pdf_writer)

        # Get page dimensions
        page_width = pdf_writer.width()
        page_height = pdf_writer.height()

        img_size = self.screenshot.size()
        scale_w = page_width / img_size.width()
        scale_h = page_height / img_size.height()
        scale = min(scale_w, scale_h)

        new_width = img_size.width() * scale
        new_height = img_size.height() * scale
        x = (page_width - new_width) / 2
        y = (page_height - new_height) / 2

        painter.drawPixmap(QRect(int(x), int(y), int(new_width), int(new_height)), self.screenshot)
        painter.end()
        print(f"Screenshot saved as PDF at {file_path}")
        self.close()
        print("Preview window terminated successfully")

    def save_as_jpeg(self, file_path):
            self.screenshot.save(file_path, "JPEG")
            print(f"Screenshot saved as JPEG at {file_path}")
            self.close()
            print("Preview window terminated successfully")
    
    def discard_screenshot(self):
        self.screenshot = None
        self.preview_label.clear()
        self.preview_label.setText("")
        self.save_button.setEnabled(False)
        self.discard_button.setEnabled(False)
        self.close()
        print("Preview window terminated successfully")

    
            
      
   
  
# running the application.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FramelessWindow()
    window.resize(250,50)
    window.show()
    sys.exit(app.exec_())