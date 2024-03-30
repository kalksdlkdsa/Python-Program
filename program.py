from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWebEngineWidgets import QWebEngineView

class Ui_MainWindow(object):
    def __init__(self):
        self.tabCount = 1  # New variable to keep track of the number of tabs

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setWindowTitle("PyBrowser")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)  # New vertical layout

        # Create a horizontal layout for the label, lineEdit, and goButton
        self.hLayout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.goButton = QtWidgets.QPushButton(parent=self.centralwidget)  # New button
        self.goButton.setObjectName("goButton")
        self.newTabButton = QtWidgets.QPushButton(parent=self.centralwidget)  # New button for new tab
        self.newTabButton.setObjectName("newTabButton")

        # Add widgets to the horizontal layout
        self.hLayout.addWidget(self.label)
        self.hLayout.addWidget(self.lineEdit)
        self.hLayout.addWidget(self.goButton)
        self.hLayout.addWidget(self.newTabButton)

        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)  # New tab widget
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setTabsClosable(True)  # Enable close buttons on tabs
        self.tabWidget.tabCloseRequested.connect(self.closeTab)  # Connect the tabCloseRequested signal to our custom slot

        # Add the horizontal layout and the tabWidget to the vertical layout
        self.layout.addLayout(self.hLayout)
        self.layout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Connect the button click event to our custom slot
        self.goButton.clicked.connect(self.loadUrl)
        # Connect the returnPressed signal of lineEdit to our custom slot
        self.lineEdit.returnPressed.connect(self.loadUrl)
        # Connect the newTabButton click event to our custom slot
        self.newTabButton.clicked.connect(self.newTab)

        # Create an initial tab
        self.newTab()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow", "URL input"))
        self.goButton.setText(_translate("MainWindow", "Go"))  # New button text
        self.newTabButton.setText(_translate("MainWindow", "New Tab"))  # New button text

    # Custom slot to handle button click and returnPressed signal
    def loadUrl(self):
        url = self.lineEdit.text()
        currentTab = self.tabWidget.currentWidget()
        if currentTab is not None:
            currentTab.load(QtCore.QUrl(url))

    # Custom slot to handle newTabButton click
    def newTab(self):
        newTab = QWebEngineView()
        index = self.tabWidget.addTab(newTab, f"Tab {self.tabCount}")  # Use the tabCount variable for the tab name
        newTab.load(QtCore.QUrl('https://google.com'))  # Load the default page
        newTab.loadFinished.connect(lambda: self.updateUrl(newTab))
        self.tabWidget.setCurrentIndex(index)  # Switch to the new tab
        self.tabCount += 1  # Increment the tabCount variable

    # Custom slot to update the lineEdit text when a new page is loaded
    def updateUrl(self, tab):
        tab.page().runJavaScript("window.location.href", self.lineEdit.setText)

    # Custom slot to handle tabCloseRequested signal
    def closeTab(self, index):
        tab = self.tabWidget.widget(index)
        tab.deleteLater()
        self.tabWidget.removeTab(index)

    # Custom slot to handle F12 key press
    def viewSource(self):
        currentTab = self.tabWidget.currentWidget()
        if currentTab is not None:
            currentTab.page().toHtml(self.showSource)

    # Custom slot to show the source code
    def showSource(self, source):
        sourceDialog = QtWidgets.QDialog()
        layout = QtWidgets.QVBoxLayout(sourceDialog)
        textEdit = QtWidgets.QTextEdit(sourceDialog)
        textEdit.setPlainText(source)
        layout.addWidget(textEdit)
        sourceDialog.exec()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_F12:
            self.ui.viewSource()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec())