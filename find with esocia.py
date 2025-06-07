import requests
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import os
import sys
url = "http://www.sabhiwaraich.c1.biz"
timeout = 5

def main():

    class AboutDialog(QDialog):
        def __init__(self, *args, **kwargs):
            super(AboutDialog, self).__init__(*args, **kwargs)
            

            QBtn = QDialogButtonBox.Ok  # No cancel
            self.buttonBox = QDialogButtonBox(QBtn)
            self.buttonBox.accepted.connect(self.accept)
            self.buttonBox.rejected.connect(self.reject)

            layout = QVBoxLayout()



            logo = QLabel()
            logo.setPixmap(QPixmap(os.path.join("icon")))
            layout.addWidget(logo)
            title = QLabel("find -The private browser")
            font = title.font()
            font.setPointSize(20)
            title.setFont(font)
        

            layout.addWidget(title)
            layout.addWidget(QLabel("Version 0.1 beta"))
            layout.addWidget(QLabel("by Sabhi Warich"))

            for i in range(0, layout.count()):
                layout.itemAt(i).setAlignment(Qt.AlignHCenter)

            layout.addWidget(self.buttonBox)

            self.setLayout(layout)


    class MainWindow(QMainWindow):
        def __init__(self, *args, **kwargs):
            super(MainWindow, self).__init__(*args, **kwargs)
            backicon="back.png"
            forwardicon="forward.png"
            homeicon="home.png"
            reloadicon="reload.png"
            cancelicon="cancel.png"
            tabicon = "add tab.png"
            icon = "icon.ico"
            abouticon= "aboutus.jpg"
            openicon="open.jpg"
            saveicon="save.png"
            printicon="print.png"
            self.tabs = QTabWidget()
            self.tabs.setDocumentMode(True)
            self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
            self.tabs.currentChanged.connect(self.current_tab_changed)
            self.tabs.setTabsClosable(True)
            self.tabs.tabCloseRequested.connect(self.close_current_tab)

            self.setCentralWidget(self.tabs)

            self.status = QStatusBar()
            self.setStatusBar(self.status)

            navtb = QToolBar("Navigation")
            navtb.setIconSize(QSize(16, 16))
            self.addToolBar(navtb)

            back_btn = QAction((QIcon(backicon)),"back", self)
            back_btn.setStatusTip("Back to previous page")
            back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
            navtb.addAction(back_btn)

            next_btn = QAction((QIcon(forwardicon)), "forward", self)
            next_btn.setStatusTip("Forward to next page")
            next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
            navtb.addAction(next_btn)

            reload_btn = QAction((QIcon(reloadicon)), "refresh", self)
            reload_btn.setStatusTip("Reload page")
            reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
            navtb.addAction(reload_btn)

            home_btn = QAction((QIcon(homeicon)), "home", self)
            home_btn.setStatusTip("Go home")
            home_btn.triggered.connect(self.navigate_home)
            navtb.addAction(home_btn)
            

            self.httpsicon = QLabel()  # Yes, really!
            self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))
            navtb.addWidget(self.httpsicon)
    
            self.urlbar = QLineEdit()
            self.urlbar.returnPressed.connect(self.navigate_to_url)
            self.urlbar.setStyleSheet("QLineEdit {  border: 2px solid green;"
                                             "border-radius: 8px;}");
            navtb.addWidget(self.urlbar)

            
            
            stop_btn = QAction((QIcon(cancelicon)),"stop", self)
            stop_btn.setStatusTip("Stop loading current page")
            stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
            navtb.addAction(stop_btn)

            # Uncomment to disable native menubar on Mac
            # self.menuBar().setNativeMenuBar(False)

            file_menu = self.menuBar().addMenu("&File")

            new_tab_action = QAction((QIcon(tabicon)),"add new tab", self)
            new_tab_action.setStatusTip("Open a new tab")
            new_tab_action.triggered.connect(lambda _: self.add_new_tab())
            file_menu.addAction(new_tab_action)

            open_file_action = QAction((QIcon(openicon)),"Open file...", self)
            open_file_action.setStatusTip("Open from file")
            open_file_action.triggered.connect(self.open_file)
            file_menu.addAction(open_file_action)

            save_file_action = QAction((QIcon(saveicon)), "Save Page As...", self)
            save_file_action.setStatusTip("Save current page to file")
            save_file_action.triggered.connect(self.save_file)
            file_menu.addAction(save_file_action)

            print_action = QAction((QIcon(printicon)),"Print...", self)
            print_action.setStatusTip("Print current page")
            print_action.triggered.connect(self.print_page)
            file_menu.addAction(print_action)

            help_menu = self.menuBar().addMenu("&Help")

            about_action = QAction((QIcon(icon)),"About find ", self)
            about_action.setStatusTip("Find out more about find ")  # Hungry!
            about_action.triggered.connect(self.about)
            help_menu.addAction(about_action)

            navigate_find_action = QAction((QIcon(abouticon)),"About us", self)
            navigate_find_action.setStatusTip("know about us")
            navigate_find_action.triggered.connect(self.navigate_find)
            help_menu.addAction(navigate_find_action)

            self.add_new_tab(QUrl('https://www.ecosia.org'), 'Homepage')

            self.show()

            self.setWindowTitle("find")
            self.setWindowIcon(QIcon(icon))
            
            
            new_tab_action = QAction((QIcon(tabicon)),"add new tab", self)
            new_tab_action.setStatusTip("Open a new tab")
            new_tab_action.triggered.connect(lambda _: self.add_new_tab())
            navtb.addAction(new_tab_action)

        def add_new_tab(self, qurl=None, label="Blank"):

            if qurl is None:
                qurl = QUrl('')

            browser = QWebEngineView()
            browser.setUrl(qurl)
            i = self.tabs.addTab(browser, label)

            self.tabs.setCurrentIndex(i)

            # More difficult! We only want to update the url when it's from the
            # correct tab
            browser.urlChanged.connect(lambda qurl, browser=browser:
                                    self.update_urlbar(qurl, browser))

            browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                        self.tabs.setTabText(i, browser.page().title()))

        def tab_open_doubleclick(self, i):
            if i == -1:  # No tab under the click
                self.add_new_tab()

        def current_tab_changed(self, i):
            qurl = self.tabs.currentWidget().url()
            self.update_urlbar(qurl, self.tabs.currentWidget())
            self.update_title(self.tabs.currentWidget())

        def close_current_tab(self, i):
            if self.tabs.count() < 2:
                return

            self.tabs.removeTab(i)

        def update_title(self, browser):
            if browser != self.tabs.currentWidget():
                # If this signal is not from the current tab, ignore
                return

            title = self.tabs.currentWidget().page().title()
            self.setWindowTitle("%s - Find" % title)

        def navigate_find(self):
            self.tabs.currentWidget().setUrl(QUrl("https://www.instagram.com/sabhi_waraich06"))

        def about(self):
            dlg = AboutDialog()
            dlg.exec_()

        def open_file(self):
            filename, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                    "Hypertext Markup Language (*.htm *.html);;"
                                                    "All files (*.*)")

            if filename:
                with open(filename, 'r') as f:
                    html = f.read()

                self.tabs.currentWidget().setHtml(html)
                self.urlbar.setText(filename)

        def save_file(self):
            filename, _ = QFileDialog.getSaveFileName(self, "Save Page As", "",
                                                    "Hypertext Markup Language (*.htm *html);;"
                                                    "All files (*.*)")

            if filename:
                html = self.tabs.currentWidget().page().toHtml()
                with open(filename, 'w') as f:
                    f.write(html.encode('utf8'))

        def print_page(self):
            dlg = QPrintPreviewDialog()
            dlg.paintRequested.connect(self.browser.print_)
            dlg.exec_()

        def navigate_home(self):
            self.tabs.currentWidget().setUrl(QUrl("https://www.ecosia.org"))

        def navigate_to_url(self):  # Does not receive the Url
            q = QUrl(self.urlbar.text())
            if q.scheme() == "":
                q.setScheme("http")

            self.tabs.currentWidget().setUrl(q)

        def update_urlbar(self, q, browser=None):

            if browser != self.tabs.currentWidget():
                # If this signal is not from the current tab, ignore
                return

            if q.scheme() == 'https':
                # Secure padlock icon
                self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-ssl.png')))

            else:
                # Insecure padlock icon
                self.httpsicon.setPixmap(QPixmap(os.path.join('images', 'lock-nossl.png')))

            self.urlbar.setText(q.toString())
            self.urlbar.setCursorPosition(0)


    app = QApplication(sys.argv)
    app.setApplicationName("find")


    window = MainWindow()

    app.exec_()

def nointernet():
    import tkinter
    root = tkinter.Tk()
    photo = tkinter.PhotoImage(file = "nointernet.gif")
    label = tkinter.Label(image = photo)
    label.pack()
    root.mainloop()
main()
# try:
# 	request = requests.get(url, timeout=timeout)
# 	main()
# except (requests.ConnectionError, requests.Timeout) as exception:
#     nointernet()
