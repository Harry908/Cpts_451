import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "MileStone1app\Qt5MW.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class myApp(QMainWindow):
    def __init__(self):
        super(myApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentIndexChanged.connect(self.stateChanged)
    
    def execQuery(self, sqlStr):
        try:
            conn=psycopg2.connect("dbname='milestone1' user='postgres' host='localhost' password='0'")
        except Exception as e:
            print("Unable to connect to the database.")
            print(e)
        cur=conn.cursor()
        cur.execute(sqlStr)
        cur.commit()
        result = cur.fetchall()
        cur.close()
        return result
    
    # Load the state list
    def loadStateList(self):
        # Clear the state list
        self.ui.stateList.clearEditText()
        
        # Query the database
        sqlStr = "SELECT * FROM business ORDER BY state;"
        try:
            result = self.execQuery(sqlStr)
            
            # Populating the state list
            for row in result:
                self.ui.stateList.addItem(row[0])
        
        except Exception as e:
            print("Unable to execute query.")
            print(e)
        
        # Set the state list to empty
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()

    # State changed event
    def stateChanged(self):
        # Get the selected state
        if self.ui.stateList.currentIndex() < 0:
            return
        state=self.ui.stateList.currentText()
        
        # Load the city list
        sqlStr = "SELECT distinct city FROM business WHERE state = '" + state + "' ORDER BY city;"
        print('Load city:')
        print(sqlStr)
        self.loadCityList(sqlStr)

        # Load the business table
        sqlStr ="SELECT name, city, state FROM business WHERE state = '" + state + "' ORDER BY name;"
        print('Load business:')
        print(sqlStr)
        self.loadBusinessTable(sqlStr)

    # City changed event
    def cityChanged(self):
        # Get the selected city and state
        if self.ui.cityList.selectedItem() < 0 or self.ui.stateList.currentIndex() < 0:
            return
        city = self.ui.cityList.selectedItems()[0].text()      
        state = self.ui.stateList.currentText()
        
        # Load the business table
        sqlStr = "SELECT name, city, state FROM business WHERE state = '" + state + "' AND city = '" + city + "' ORDER BY name;"
        print('Load business:')
        print(sqlStr)
        self.loadBusinessTable(sqlStr)

    # Load the city list
    def loadCityList(self,sqlStr):
        # Clear the city list
        self.ui.cityList.clear()
        try:
            # Query the database
            results = self.execQuery(sqlStr)
            
            # Populating the city list
            for row in results:
                self.ui.cityList.addItem(row[0])

        except Exception as e:
            print("Unable to execute query.")
            print(e)
    
    # Load the business table
    def loadBusinessTable(self,sqlStr):
        # Clear the table
        for i in reversed(range(self.ui.businessTable.rowCount())):
            self.ui.businessTable.removeRow(i)
        
        try:
            # Query the database
            results = self.execQuery(sqlStr)
            
            # Styling the table
            style = "::section {""background-color: #f2f2f2; }"
            self.ui.businessTable.horizontalHeader().setStyleSheet(style)
            self.ui.businessTable.setRowCount(len(results))
            self.ui.businessTable.setColumnCount(len(results[0]))
            self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State'])
            self.ui.businessTable.resizeColumnsToContents()
            self.ui.businessTable.setColumnWidth(0, 300)
            self.ui.businessTable.setColumnWidth(1, 150)
            self.ui.businessTable.setColumnWidth(2, 50)
            
            # Populating the table
            curRow = 0
            for row in results:
                for col in range(len(row)):
                    self.ui.businessTable.setItem(curRow, col, QTableWidgetItem(row[col]))
                curRow += 1

        except Exception as e:
            print("Unable to execute query.")
            print(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = myApp()
    window.show()
    sys.exit(app.exec_())