import os
from PyQt4 import QtCore, QtGui

from Extensions import StyleSheet


class Favourites(QtGui.QLabel):

    showMe = QtCore.pyqtSignal()

    openFile = QtCore.pyqtSignal(str)

    def __init__(self, favouritesList, messagesWidget, parent=None):
        super(Favourites, self).__init__(parent)

        self.setMinimumSize(600, 230)
        self.setObjectName("containerLabel")
        self.setStyleSheet(StyleSheet.toolWidgetStyle)

        self.setBackgroundRole(QtGui.QPalette.Background)
        self.setAutoFillBackground(True)

        self.messagesWidget = messagesWidget
        self.favouritesList = favouritesList

        self.manageFavAct = \
            QtGui.QAction(
                QtGui.QIcon(os.path.join("Resources", "images", "settings")),
                          "Manage Favourites", self, statusTip="Manage Favourites",
                          triggered=self.showMe.emit)

        mainLayout = QtGui.QVBoxLayout()

        hbox = QtGui.QHBoxLayout()
        mainLayout.addLayout(hbox)

        label = QtGui.QLabel("Manage Favourites")
        label.setObjectName("toolWidgetNameLabel")
        hbox.addWidget(label)

        hbox.addStretch(1)

        self.hideButton = QtGui.QToolButton()
        self.hideButton.setAutoRaise(True)
        self.hideButton.setIcon(
            QtGui.QIcon(os.path.join("Resources", "images", "cross_")))
        self.hideButton.clicked.connect(self.hide)
        hbox.addWidget(self.hideButton)

        self.favouritesListWidget = QtGui.QListWidget()
        mainLayout.addWidget(self.favouritesListWidget)

        hbox = QtGui.QHBoxLayout()

        self.removeButton = QtGui.QPushButton("Remove")
        self.removeButton.clicked.connect(self.removeFavourite)
        hbox.addWidget(self.removeButton)

        hbox.addStretch(1)

        mainLayout.addLayout(hbox)

        self.setLayout(mainLayout)

        self.favouritesMenu = QtGui.QMenu("Favourites")
        self.favouritesMenu.setIcon(QtGui.QIcon(
            os.path.join("Resources", "images", "bookmarked_url")))
        self.loadFavourites()

    def removeFavourite(self):
        row = self.favouritesListWidget.currentRow()
        del self.favouritesList[row]
        self.loadFavourites()

    def addToFavourites(self, path):
        if path in self.favouritesList:
            pass
        else:
            self.favouritesList.append(path)
            self.favouritesList.sort()
            self.loadFavourites()
            self.messagesWidget.addMessage(0, "Favourites",
                                           ["'{0}' added!".format(path)])

    def loadFavourites(self):
        self.favouritesMenu.clear()
        self.favouritesListWidget.clear()
        if len(self.favouritesList) > 0:
            self.favouritesActionGroup = QtGui.QActionGroup(self)
            self.favouritesActionGroup.triggered.connect(
                self.favouriteActivated)
            for i in self.favouritesList:
                action = QtGui.QAction(QtGui.QIcon(
                    os.path.join("Resources", "images", "star")), i, self)
                self.favouritesActionGroup.addAction(action)
                self.favouritesMenu.addAction(action)

                item = QtGui.QListWidgetItem(i.strip())
                item.setToolTip(i)
                item.setSizeHint(QtCore.QSize(20, 20))
                self.favouritesListWidget.addItem(item)

            self.favouritesMenu.addSeparator()
            self.favouritesMenu.addAction(self.manageFavAct)
            self.removeButton.setDisabled(False)
        else:
            action = QtGui.QAction("No Favourites", self)
            self.favouritesMenu.addAction(action)
            self.favouritesMenu.addAction(action)
            self.removeButton.setDisabled(True)

    def favouriteActivated(self, action):
        path = action.text()
        if os.path.exists(path):
            self.openFile.emit(path)
        else:
            message = QtGui.QMessageBox.warning(self, "Open",
                                                "File is no longer available.")
