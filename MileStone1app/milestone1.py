import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2

qtCreatorFile = "MileStone1app\mw.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class myApp(QMainWindow):
    def __init__(self):
        super(myApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.loadStateList()
        self.ui.stateList.currentIndexChanged.connect(self.stateChanged)
        self.ui.sBox.currentIndexChanged.connect(self.stateChanged2)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.cList2.itemSelectionChanged.connect(self.cityChanged2)
        self.ui.zipList2.itemSelectionChanged.connect(self.zipChanged)
        self.ui.fCateList.itemSelectionChanged.connect(self.categoryChanged)
        self.ui.clearFBBtn.clicked.connect(self.clearFB)
        self.ui.searchBBtn.clicked.connect(self.searchFB)
    
    def execQuery(self, sqlStr):
        try:
            conn=psycopg2.connect("dbname='milestone1db' user='postgres' host='localhost' password='0'")
        except Exception as e:
            print("Unable to connect to the database.")
            print(e)
        cur=conn.cursor()
        cur.execute(sqlStr)
        conn.commit()
        result = cur.fetchall()
        cur.close()
        return result
    
    # Load the state list
    def loadStateList(self):
        # Clear the state list
        self.ui.stateList.clearEditText()
        self.ui.sBox.clearEditText()
        
        # Query the database
        sqlStr = "SELECT DISTINCT state FROM business ORDER BY state;"
        try:
            result = self.execQuery(sqlStr)
            
            # Populating the state list
            for row in result:
                self.ui.stateList.addItem(row[0])
                self.ui.sBox.addItem(row[0])
        
        except Exception as e:
            print("Unable to execute query.")
            print(e)
        
        # Set the state list to empty
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()
         # Set the state list to empty
        self.ui.sBox.setCurrentIndex(-1)
        self.ui.sBox.clearEditText()

    # State changed event
    def stateChanged(self):
        # Get the selected state
        if self.ui.stateList.currentIndex() < 0:
            return
        state=self.ui.stateList.currentText()
        
        # Load the city list
        sqlStr = "SELECT DISTINCT city FROM business WHERE state = '" + state + "' ORDER BY city;"
        print('Load city:')
        print(sqlStr)
        self.loadCityList(sqlStr, self.ui.cityList)

        # Load the business table
        sqlStr ="SELECT name, city, state FROM business WHERE state = '" + state + "' ORDER BY name;"
        print('Load business:')
        print(sqlStr)
        self.loadBusinessTable(sqlStr)

    # State changed event
    def stateChanged2(self):
        # Get the selected state
        if self.ui.sBox.currentIndex() < 0:
            return
        state=self.ui.sBox.currentText()
        self.clearZipcodeStats(True)

        # Load the city list
        sqlStr = "SELECT DISTINCT city FROM business WHERE state = '" + state + "' ORDER BY city;"
        print('Load city:')
        print(sqlStr)
        self.loadCityList(sqlStr,self.ui.cList2)

        # Load the business table
        sqlStr = """
        SELECT name, stars, address, numCheckins, reviewrating, reviewcount
        FROM business
        WHERE state = '{}';
        """.format(state)
        columns = ['Business Name', 'Stars', 'Address', 'Checkins', 'Review Rating', 'Review Count']
        print('Load business by city:')
        print(sqlStr)
        self.updateTables(sqlStr, columns)


    # City changed event
    def cityChanged(self):
        # Get the selected city and state
        if not self.ui.cityList.selectedItems() or self.ui.stateList.currentIndex() < 0:
            return
        city = self.ui.cityList.selectedItems()[0].text()      
        state = self.ui.stateList.currentText()
        
        # Load the business table
        sqlStr = "SELECT name, city, state FROM business WHERE state = '" + state + "' AND city = '" + city + "' ORDER BY name;"
        print('Load business:')
        print(sqlStr)
        self.loadBusinessTable(sqlStr)

    # City changed event
    def cityChanged2(self):
        # Get the selected city and state
        if not self.ui.cList2.selectedItems() or self.ui.sBox.currentIndex() < 0:
            return
        city = self.ui.cList2.selectedItems()[0].text()      
        state = self.ui.sBox.currentText()
        
        #Clear zipcode
        self.clearZipcodeStats()

        # Load the business table
        sqlStr = "SELECT DISTINCT zipcode FROM business WHERE state = '" + state + "' AND city = '" + city + "' ORDER BY zipcode;"
        print('Load Zipcode:')
        print(sqlStr)
        self.loadList(sqlStr,self.ui.zipList2)

        # Load the business table
        sqlStr = """
        SELECT name, stars, address, numCheckins, reviewrating, reviewcount
        FROM business
        WHERE state = '{}' AND city = '{}';
        """.format(state, city)
        columns = ['Business Name', 'Stars', 'Address', 'Checkins', 'Review Rating', 'Review Count']
        print('Load business by city:')
        print(sqlStr)
        self.updateTables(sqlStr, columns)

        

    def clearZipcodeStats(self, clear=False):
        # Clear the zipcode list
        if clear:
            self.ui.zipList2.clear()
        # Clear the zipcode statistics
        self.ui.numBLine.setText("")
        self.ui.popLine.setText("")
        self.ui.incomeLine.setText("")
        # Clear the category table
        self.clearTable(self.ui.cateTableZip)
        # Clear the category list
        self.ui.fCateList.clear()
    
    # Zipcode changed event
    def zipChanged(self):
        if not self.ui.zipList2.selectedItems() or self.ui.sBox.currentIndex() < 0:
            return
        zipcode = self.ui.zipList2.selectedItems()[0].text()      
        state = self.ui.sBox.currentText()
        city = self.ui.cList2.selectedItems()[0].text()

        # Update zipcode statistics (e.g., display total business count)
        self.updateZipStats(state, city, zipcode)

        # Load the categories list with business count per category
        sqlStr = """
        SELECT COUNT(*) as "numbusiness", cname
        FROM business_category bc
        JOIN business b ON bc.business_id = b.business_id
        WHERE b.state = '{}'  AND b.city = '{}' AND b.zipcode = '{}'
        GROUP BY cname
        ORDER BY COUNT(*) DESC;
        """.format(state, city, zipcode)
        print('Load categories with business count:')
        print(sqlStr)
        self.loadCategory(sqlStr)

        # Load the business table
        sqlStr = """
        SELECT name, stars, address, numCheckins, reviewrating, reviewcount
        FROM business
        WHERE state = '{}' AND city = '{}' AND zipcode = '{}';
        """.format(state, city, zipcode)
        columns = ['Business Name', 'Stars', 'Address', 'Checkins', 'Review Rating', 'Review Count']
        print('Load business by zipcode:')
        print(sqlStr)
        self.updateTables(sqlStr, columns)

    def updateTables(self,sqlStr, columns):
        
        # Load the business table
        try:
            # Query the database
            results = self.execQuery(sqlStr)
            self.ui.countLabel.setText(f"{len(results)}")
            # Update the business table
            self.loadBusinessTable1(results, self.ui.filterBTable, columns)
            self.loadBusinessTable1(results,self.ui.popBTable, columns)
            self.loadBusinessTable1(results,self.ui.sucBTable, columns)
        
        except Exception as e:
            print("Unable to execute query.")
            print(e)


    def categoryChanged(self):
        # Get the selected category and state
        if not self.ui.fCateList.selectedItems() or self.ui.sBox.currentIndex() < 0 \
            or not self.ui.cList2.selectedItems() or not self.ui.zipList2.selectedItems():
            return
        category = self.ui.fCateList.selectedItems()[0].text()      
        state = self.ui.sBox.currentText()
        city = self.ui.cList2.selectedItems()[0].text()
        zipcode = self.ui.zipList2.selectedItems()[0].text()

        # Load the business table
        sqlStr = """
        SELECT name, stars, address, numCheckins, reviewrating, reviewcount
        FROM business
        WHERE state = '{}' AND city = '{}' AND zipcode = '{}' 
        AND business_id IN (SELECT business_id FROM business_category WHERE cname = '{}');
        """.format(state, city, zipcode, category)
        columns = ['Business Name', 'Stars', 'Address', 'Checkins', 'Review Rating', 'Review Count']
        print('Load business by category:')
        print(sqlStr)
        self.updateTables(sqlStr, columns)
        
    def clearFB(self):
        # Clear the filter business table
        self.ui.fCateList.clearSelection()
        # Clear the filter business table
        self.clearTable(self.ui.filterBTable)
        self.clearTable(self.ui.popBTable)
        self.clearTable(self.ui.sucBTable)
        # Clear the category list

    def searchFB(self):
        # Get the selected state and city
        if self.ui.sBox.currentIndex() < 0:
            return
        if not self.ui.cList2.selectedItems():
            self.cityChanged2()
            return
        if not self.ui.zipList2.selectedItems():
            self.cityChanged2()
            return
        if not self.ui.fCateList.selectedItems():
            self.zipChanged()
            return
        self.categoryChanged()

    def clearTable(self, uiTable):
        # Clear the table
        for i in reversed(range(uiTable.rowCount())):
            uiTable.removeRow(i)

    
    def loadBusinessTable1(self, results, uiTable, columns: list):
        # Clear the table
        for i in reversed(range(uiTable.rowCount())):
            uiTable.removeRow(i)
        
        if results:   
            # Styling the table
            style = "QHeaderView::section { background-color: #2C6D9A; color: white; font-weight: bold; font-size: 12px; font-style: italic; }"
            uiTable.horizontalHeader().setStyleSheet(style)
            uiTable.setRowCount(len(results))
            uiTable.setColumnCount(len(columns))
            uiTable.setHorizontalHeaderLabels(columns)
            uiTable.horizontalHeader().setStretchLastSection(False)
            # Populating the table
            curRow = 0
            for row in results:
                for col in range(len(row)):
                    uiTable.setItem(curRow, col, QTableWidgetItem(str(row[col])))
                curRow += 1
        
            uiTable.resizeColumnsToContents()
            uiTable.setColumnWidth(columns.index("Address"), 360)
            uiTable.horizontalHeader().setStretchLastSection(True)
     


    def loadCategory(self,sqlStr):
        print(sqlStr)
        try:
            results = self.execQuery(sqlStr)
            self.updateTable(results,self.ui.cateTableZip)
            self.updateList(results,self.ui.fCateList,column=1)
        except Exception as e:
            print("Unable to load category table.")
            print(e)

    def updateTable(self, results, uiTable):
        # Clear the table
        for i in reversed(range(uiTable.rowCount())):
            uiTable.removeRow(i)
        
        # Styling the table
        style = "QHeaderView::section { background-color: #2C6D9A; color: white; font-weight: bold; font-size: 12px; font-style: italic; }"
        uiTable.horizontalHeader().setStyleSheet(style)
        uiTable.setRowCount(len(results))
        uiTable.setColumnCount(len(results[0]))
        uiTable.setHorizontalHeaderLabels(['# of Business', 'Category Name'])
        uiTable.resizeColumnsToContents()
        uiTable.setColumnWidth(0, 100)
        uiTable.setColumnWidth(1, 250)
        
        # Populating the table
        for i, record in enumerate(results):
            count, cname = record
            uiTable.setItem(i, 0, QTableWidgetItem(str(count)))
            uiTable.setItem(i, 1, QTableWidgetItem(cname))

    
    def updateZipStats(self,state, city, zipcode):
        # Retrieve the total number of businesses in the selected zipcode
        sqlStr = "SELECT COUNT(*) FROM business WHERE state = '{}' AND city = '{}' AND zipcode = '{}';".format(state, city, zipcode)
        # Retrieve the population and mean income for the selected zipcode
        sqlStrZipData = "SELECT population, meanincome FROM zipcodedata WHERE zipcode = '{}';".format(zipcode)
        try:
            # retrieve the total number of businesses in the selected zipcode
            print(sqlStr)
            result = self.execQuery(sqlStr)
            if result:
                count = result[0][0]
                self.ui.numBLine.setText(f"{count}")
            # Retrieve the population and mean income for the selected zipcode
            print(sqlStrZipData)
            result = self.execQuery(sqlStrZipData)
            if result:
                population = result[0][0]
                meanincome = result[0][1]
                self.ui.popLine.setText(f"{population}")
                self.ui.incomeLine.setText(f"{meanincome}")
        except Exception as e:
            print("Unable to update zipcode stats.")
            print(e)


    def updateList(self,results,uiList,column=0):
        # Clear the list
        uiList.clear()
        if results:
            # Populating the list
            for row in results:
                uiList.addItem(row[column])

       
    def loadList(self,sqlStr,uiList):
        # Clear the list
        uiList.clear()
        try:
            # Query the database
            results = self.execQuery(sqlStr)
            
            # Populating the list
            for row in results:
                uiList.addItem(row[0])

        except Exception as e:
            print("Unable to execute query.")
            print(e)

    # Load the city list
    def loadCityList(self,sqlStr,uiList):
        # Clear the city list
        uiList.clear()
        try:
            # Query the database
            results = self.execQuery(sqlStr)
            
            # Populating the city list
            for row in results:
                uiList.addItem(row[0])

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
            style = "QHeaderView::section { background-color: #2C6D9A; color: white; font-weight: bold; font-size: 18px; font-style: italic; }"
            self.ui.businessTable.horizontalHeader().setStyleSheet(style)
            self.ui.businessTable.setRowCount(len(results))
            self.ui.businessTable.setColumnCount(len(results[0]))
            self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State'])
            self.ui.businessTable.resizeColumnsToContents()
            self.ui.businessTable.setColumnWidth(0, 300)
            self.ui.businessTable.setColumnWidth(1, 170)
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