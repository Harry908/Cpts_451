# Import necessary modules
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2  # PostgreSQL connector

# Load the UI file created using Qt Designer
qtCreatorFile = "MileStone1app\mw.ui"  # Path to UI file
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# Main application class
class myApp(QMainWindow):

    #   ------ Initialization / Setup ------

    def __init__(self):
        super(myApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Load state list and connect GUI elements to event handler methods
        self.loadStateList()
        self.ui.stateList.currentIndexChanged.connect(self.stateChanged)
        self.ui.sBox.currentIndexChanged.connect(self.stateChanged2)
        self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
        self.ui.cList2.itemSelectionChanged.connect(self.cityChanged2)
        self.ui.zipList2.itemSelectionChanged.connect(self.zipChanged)
        self.ui.fCateList.itemSelectionChanged.connect(self.categoryChanged)
        self.ui.clearFBBtn.clicked.connect(self.clearFB)
        self.ui.searchBBtn.clicked.connect(self.searchFB)

    # Loads unique states from the business table and populates the state selection widgets
    def loadStateList(self):
        self.ui.stateList.clearEditText()
        self.ui.sBox.clearEditText()
        sqlStr = "SELECT DISTINCT state FROM business ORDER BY state;"
        try:
            result = self.execQuery(sqlStr)
            for row in result:
                self.ui.stateList.addItem(row[0])
                self.ui.sBox.addItem(row[0])
        except Exception as e:
            print("Unable to execute query.")
            print(e)
        self.ui.stateList.setCurrentIndex(-1)
        self.ui.stateList.clearEditText()
        self.ui.sBox.setCurrentIndex(-1)
        self.ui.sBox.clearEditText()

    #   ------ Database Interaction / Connection ------

    # Executes a SQL query and returns the result
    def execQuery(self, sqlStr):
        try:
            conn = psycopg2.connect("dbname='milestone3db' user='postgres' host='localhost' password='WSUEverett'")
        except Exception as e:
            print("Unable to connect to the database.")
            print(e)
        cur = conn.cursor()
        cur.execute(sqlStr)
        conn.commit()
        result = cur.fetchall()
        cur.close()
        return result
    
    #   --------- For Milestone 1 Only ---------

    # Triggered when state is selected from stateList
    def stateChanged(self):
        if self.ui.stateList.currentIndex() < 0:
            return
        state = self.ui.stateList.currentText()
        # Load cities for selected state
        sqlStr = f"SELECT DISTINCT city FROM business WHERE state = '{state}' ORDER BY city;"
        print('Load city:')
        print(sqlStr)
        self.loadCityList(sqlStr, self.ui.cityList)
        # Load businesses for selected state
        sqlStr = f"SELECT name, city, state FROM business WHERE state = '{state}' ORDER BY name;"
        print('Load business:')
        print(sqlStr)
        self.loadBusinessTable(sqlStr)

    # Triggered when a city is selected in cityList
    def cityChanged(self):
        if not self.ui.cityList.selectedItems() or self.ui.stateList.currentIndex() < 0:
            return
        city = self.ui.cityList.selectedItems()[0].text()
        state = self.ui.stateList.currentText()
        sqlStr = f"SELECT name, city, state FROM business WHERE state = '{state}' AND city = '{city}' ORDER BY name;"
        print('Load business:')
        print(sqlStr)
        self.loadBusinessTable(sqlStr)
    
    # Load business table for basic state/city queries
    def loadBusinessTable(self, sqlStr):
        self.clearTable(self.ui.businessTable)
        try:
            results = self.execQuery(sqlStr)
            style = "QHeaderView::section { background-color: #2C6D9A; color: white; font-weight: bold; font-size: 18px; font-style: italic; }"
            self.ui.businessTable.horizontalHeader().setStyleSheet(style)
            self.ui.businessTable.setRowCount(len(results))
            self.ui.businessTable.setColumnCount(len(results[0]))
            self.ui.businessTable.setHorizontalHeaderLabels(['Business Name', 'City', 'State'])
            self.ui.businessTable.resizeColumnsToContents()
            self.ui.businessTable.setColumnWidth(0, 300)
            self.ui.businessTable.setColumnWidth(1, 170)
            self.ui.businessTable.setColumnWidth(2, 50)
            for curRow, row in enumerate(results):
                for col in range(len(row)):
                    self.ui.businessTable.setItem(curRow, col, QTableWidgetItem(row[col]))
        except Exception as e:
            print("Unable to execute query.")
            print(e)

    #   --------- For Milestone 2 ---------

    #   ------ Event Handlers ------

    #   --- Event Handlers - State and City Selection ---

    # Triggered when state is selected from sBox (used for zipcode view)
    def stateChanged2(self):
        if self.ui.sBox.currentIndex() < 0:
            return
        state = self.ui.sBox.currentText()
        self.clearZipcodeStats(True)
        # Load cities
        sqlStr = f"SELECT DISTINCT city FROM business WHERE state = '{state}' ORDER BY city;"
        print('Load city:')
        print(sqlStr)
        self.loadCityList(sqlStr, self.ui.cList2)
        # Load businesses
        sqlStr = f"""
        SELECT name, stars, address, numCheckins, reviewrating, reviewcount
        FROM business
        WHERE state = '{state}';
        """
        columns = ['Business Name', 'Stars', 'Address', 'Checkins', 'Review Rating', 'Review Count']
        print('Load business by city:')
        print(sqlStr)
        self.updateTables(sqlStr, columns)

    # Triggered when a city is selected in cList2
    def cityChanged2(self):
        if not self.ui.cList2.selectedItems() or self.ui.sBox.currentIndex() < 0:
            return
        city = self.ui.cList2.selectedItems()[0].text()
        state = self.ui.sBox.currentText()
        self.clearZipcodeStats()
        # Load zipcodes
        sqlStr = f"SELECT DISTINCT zipcode FROM business WHERE state = '{state}' AND city = '{city}' ORDER BY zipcode;"
        print('Load Zipcode:')
        print(sqlStr)
        self.loadList(sqlStr, self.ui.zipList2)
        # Load businesses
        sqlStr = f"""
        SELECT name, stars, address, numCheckins, reviewrating, reviewcount
        FROM business
        WHERE state = '{state}' AND city = '{city}';
        """
        columns = ['Business Name', 'Stars', 'Address', 'Checkins', 'Review Rating', 'Review Count']
        print('Load business by city:')
        print(sqlStr)
        self.updateTables(sqlStr, columns)

    #   --- Event Handlers - Zipcode and Category Selection ---

    # Triggered when a zipcode is selected
    def zipChanged(self):
        if not self.ui.zipList2.selectedItems() or self.ui.sBox.currentIndex() < 0:
            return
        zipcode = self.ui.zipList2.selectedItems()[0].text()
        state = self.ui.sBox.currentText()
        city = self.ui.cList2.selectedItems()[0].text()
        self.updateZipStats(state, city, zipcode)
        # Load category list and counts
        sqlStr = f"""
        SELECT COUNT(*) as "numbusiness", cname
        FROM business_category bc
        JOIN business b ON bc.business_id = b.business_id
        WHERE b.state = '{state}'  AND b.city = '{city}' AND b.zipcode = '{zipcode}'
        GROUP BY cname
        ORDER BY COUNT(*) DESC;
        """
        print('Load categories with business count:')
        print(sqlStr)
        self.loadCategory(sqlStr)
        # Load businesses
        sqlStr = f"""
        SELECT name, stars, address, numCheckins, reviewrating, reviewcount
        FROM business
        WHERE state = '{state}' AND city = '{city}' AND zipcode = '{zipcode}';
        """
        columns = ['Business Name', 'Stars', 'Address', 'Checkins', 'Review Rating', 'Review Count']
        print('Load business by zipcode:')
        print(sqlStr)
        self.updateTables(sqlStr, columns)

    # Triggered when a category is selected
    def categoryChanged(self):
        if not self.ui.fCateList.selectedItems() or self.ui.sBox.currentIndex() < 0 \
            or not self.ui.cList2.selectedItems() or not self.ui.zipList2.selectedItems():
            return
        category = self.ui.fCateList.selectedItems()[0].text()
        state = self.ui.sBox.currentText()
        city = self.ui.cList2.selectedItems()[0].text()
        zipcode = self.ui.zipList2.selectedItems()[0].text()
        sqlStr = f"""
        SELECT name, stars, address, numCheckins, reviewrating, reviewcount
        FROM business
        WHERE state = '{state}' AND city = '{city}' AND zipcode = '{zipcode}' 
        AND business_id IN (SELECT business_id FROM business_category WHERE cname = '{category}');
        """
        columns = ['Business Name', 'Stars', 'Address', 'Checkins', 'Review Rating', 'Review Count']
        print('Load business by category:')
        print(sqlStr)
        self.updateTables(sqlStr, columns)

    #   --- Event Handlers - Button clicks ---

    # Clears filter and tables
    def clearFB(self):
        self.ui.fCateList.clearSelection()
        self.clearTable(self.ui.filterBTable)
        self.clearTable(self.ui.popBTable)
        self.clearTable(self.ui.sucBTable)

    # Logic for search button depending on user selection
    def searchFB(self):
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

    #   ------ UI Update Helpers ------

    # Runs a query and updates all three business tables with results
    def updateTables(self, baseQuery, columns):
        try:
            results = self.execQuery(baseQuery)
            self.ui.countLabel.setText(f"{len(results)}")

            # Load original filtered data
            self.loadBusinessTable1(results, self.ui.filterBTable, columns)

            # Load success-sorted data
            success_sorted = sorted(results, key=lambda row: float(row[5]) * (float(row[4]) / 5.0), reverse=True)
            self.loadBusinessTable1(success_sorted, self.ui.sucBTable, columns)

            # Load popularity-sorted data
            popularity_sorted = sorted(results, key=lambda row: (float(row[5]) * 0.5) + (float(row[3]) / 10.0) + (float(row[4]) * 15.0), reverse=True)
            self.loadBusinessTable1(popularity_sorted, self.ui.popBTable, columns)

        except Exception as e:
            print("Unable to execute query.")
            print(e)

    # Updates zipcode statistics: number of businesses, population, income
    def updateZipStats(self, state, city, zipcode):
        sqlStr = f"SELECT COUNT(*) FROM business WHERE state = '{state}' AND city = '{city}' AND zipcode = '{zipcode}';"
        sqlStrZipData = f"SELECT population, meanincome FROM zipcodedata WHERE zipcode = '{zipcode}';"
        try:
            print(sqlStr)
            result = self.execQuery(sqlStr)
            if result:
                self.ui.numBLine.setText(f"{result[0][0]}")
            print(sqlStrZipData)
            result = self.execQuery(sqlStrZipData)
            if result:
                self.ui.popLine.setText(f"{result[0][0]}")
                self.ui.incomeLine.setText(f"{result[0][1]}")
        except Exception as e:
            print("Unable to update zipcode stats.")
            print(e)

    # Clears all UI elements and tables related to zipcodes
    def clearZipcodeStats(self, clear=False):
        if clear:
            self.ui.zipList2.clear()
        self.ui.numBLine.setText("")
        self.ui.popLine.setText("")
        self.ui.incomeLine.setText("")
        self.clearTable(self.ui.cateTableZip)
        self.ui.fCateList.clear()

    # Clears all rows from a table
    def clearTable(self, uiTable):
        for i in reversed(range(uiTable.rowCount())):
            uiTable.removeRow(i)

    #   ------ Table and List Loaders ------

    # Load business data into given table
    def loadBusinessTable1(self, results, uiTable, columns: list):
        self.clearTable(uiTable)
        if results:
            style = "QHeaderView::section { background-color: #2C6D9A; color: white; font-weight: bold; font-size: 12px; font-style: italic; }"
            uiTable.horizontalHeader().setStyleSheet(style)
            uiTable.setRowCount(len(results))
            uiTable.setColumnCount(len(columns))
            uiTable.setHorizontalHeaderLabels(columns)
            uiTable.horizontalHeader().setStretchLastSection(False)
            for curRow, row in enumerate(results):
                for col in range(len(row)):
                    uiTable.setItem(curRow, col, QTableWidgetItem(str(row[col])))
            uiTable.resizeColumnsToContents()
            uiTable.setColumnWidth(columns.index("Address"), 360)
            uiTable.horizontalHeader().setStretchLastSection(True)

    # Loads city list
    def loadCityList(self, sqlStr, uiList):
        uiList.clear()
        try:
            results = self.execQuery(sqlStr)
            for row in results:
                uiList.addItem(row[0])
        except Exception as e:
            print("Unable to execute query.")
            print(e)

    # Loads a list of values from query into a QListWidget
    def loadList(self, sqlStr, uiList):
        uiList.clear()
        try:
            results = self.execQuery(sqlStr)
            for row in results:
                uiList.addItem(row[0])
        except Exception as e:
            print("Unable to execute query.")
            print(e)

    # Loads business categories and updates table and list
    def loadCategory(self, sqlStr):
        print(sqlStr)
        try:
            results = self.execQuery(sqlStr)
            self.updateTable(results, self.ui.cateTableZip)
            self.updateList(results, self.ui.fCateList, column=1)
        except Exception as e:
            print("Unable to load category table.")
            print(e)

    # Updates table with given results
    def updateTable(self, results, uiTable):
        self.clearTable(uiTable)
        style = "QHeaderView::section { background-color: #2C6D9A; color: white; font-weight: bold; font-size: 12px; font-style: italic; }"
        uiTable.horizontalHeader().setStyleSheet(style)
        uiTable.setRowCount(len(results))
        uiTable.setColumnCount(len(results[0]))
        uiTable.setHorizontalHeaderLabels(['# of Business', 'Category Name'])
        uiTable.resizeColumnsToContents()
        uiTable.setColumnWidth(0, 100)
        uiTable.setColumnWidth(1, 250)
        for i, record in enumerate(results):
            count, cname = record
            uiTable.setItem(i, 0, QTableWidgetItem(str(count)))
            uiTable.setItem(i, 1, QTableWidgetItem(cname))

    # Updates a QListWidget with a list of values
    def updateList(self, results, uiList, column=0):
        uiList.clear()
        if results:
            for row in results:
                uiList.addItem(row[column])

#   ------ Main App Entry Point ------

# Launch the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = myApp()
    window.show()
    sys.exit(app.exec_())

