def printError(error):
    print(colored("Error:", "red"), error)


def multiLineInput(promt):
    text = ""
    while True:
        x = input(promt)
        if x:
            text += x + " "
        else:
            break
        if text[-2] == ";":
            break
    return text[:-1]


try:
    from tabulate import tabulate
except Exception:
    printError(
        "To run this program, you need to have tabulate library\nCan be installed by running: pip3 install tabulate"
    )
    exit()
try:
    from termcolor import colored
except Exception:
    printError(
        "To run this program, you need to have termcolor library\nCan be installed by running: pip3 install termcolor"
    )
    exit()


class column:
    def __init__(self, name, indexed):
        self.indexed = indexed
        self.columnName = name
        self.elements = []

    def addElement(self, el):
        print("Adding", el, "to", self.columnName)
        self.elements.append(el)

    def deleteElementByValue(self, val):
        self.elements.remove(val)

    def deleteElementByIndex(self, index):
        self.elements.pop(index)

    def deleteAllElements(self):
        self.elements = []

    # elements = []
    # indexed = False
    # columnName = ""


class table:
    # columns = []
    # tableName = ""
    def __init__(self, name, columns):
        self.tableName = name
        self.columns = columns

    def addColumn(self, column):
        self.columns.append(column)

    # def selectElements(self, columnm, columnsToPrint, condition):
    #     output = []
    #     for column in self.columns:
    #         if column.columnName == columnm:
    #             for element in column.elements:
    #                 if condition(element):
    #                     output.append((column.columnName, column.elements.index(element)))

    # return output


class DB:
    def __init__(self):
        self.tables = []
        self.name = ""

    def addTable(self, table):
        self.tables.append(table)

    def setName(self, name):
        self.name = name

    def createTable(self, tableName, columns):
        for tab in self.tables:
            if tab.tableName == tableName:
                printError("Table already exists")
                return -1
        tableToAppend = table(tableName, columns)
        self.tables.append(tableToAppend)

    def insertInTable(self, tableName, params):
        errFlag = False
        tabFlag = False
        for table in self.tables:
            if table.tableName == tableName:
                tabFlag = True
                if len(params) != len(table.columns):
                    printError("Params amount isn`t equal amount columns")
                    errFlag = True
                    return
                i = 0
                # print(params)
                while i < len(table.columns):
                    table.columns[i].addElement(params[i])
                    # print(table.columns[i].columnName)
                    i += 1
        if not tabFlag:
            printError("Table not found")
        return errFlag

    def selectOnCond(self, tabName, columnsToPrint, columnToAnal, condValue, condition):
        tableIndex = -1
        i = 0
        while i < len(self.tables):
            if self.tables[i].tableName == tabName:
                tableIndex = i
                break
            i += 1
        if tableIndex == -1:
            printError("Table not found")
            return
        i = 0
        columnIndex = -1
        while i < len(self.tables[tableIndex].columns):
            if self.tables[tableIndex].columns[i].columnName == columnToAnal:
                columnIndex = i
                break
            i += 1
        if columnIndex == -1:
            printError("Column not found")
            return
        columnsToPrintIndexes = []
        if columnsToPrint == "*":
            for ind in range(0, len(self.tables[tableIndex].columns)):
                columnsToPrintIndexes.append(ind)
        else:
            for columnToPrint in columnsToPrint:
                i = 0
                while i < len(self.tables[tableIndex].columns):
                    if self.tables[tableIndex].columns[i].columnName == columnToPrint:
                        columnsToPrintIndexes.append(i)
                    i += 1

        valsIndexes = []
        i = 0
        printString = ""
        for index in columnsToPrintIndexes:
            printString += " " + self.tables[tableIndex].columns[index].columnName
        printString += "\n"
        while i < len(self.tables[tableIndex].columns[columnIndex].elements):
            if condition(
                condValue, self.tables[tableIndex].columns[columnIndex].elements[i]
            ):
                valsIndexes.append(i)
                # for index in columnsToPrintIndexes:
                # printString += " " + self.tables[tableIndex].columns[index].elements[i]
                # printString += '\n'
            i += 1
        # print(printString)
        # print(valsIndexes, columnsToPrintIndexes)
        headers = []
        for col in columnsToPrintIndexes:
            headers.append(self.tables[tableIndex].columns[col].columnName)
        rows = []
        for row in valsIndexes:
            rowOut = []
            for index in columnsToPrintIndexes:
                rowOut.append(self.tables[tableIndex].columns[index].elements[row])
            rows.append(rowOut)
            pass
        print(colored(tabulate(rows, headers=headers, tablefmt="orgtbl"), "yellow"))

    def selectNoCond(self, tabName, columnsToPrint):
        tableIndex = -1
        i = 0
        while i < len(self.tables):
            if self.tables[i].tableName == tabName:
                tableIndex = i
                break
            i += 1
        if tableIndex == -1:
            printError("Table not found")
            return
        columnsToPrintIndexes = []
        if columnsToPrint == "*":
            for ind in range(0, len(self.tables[tableIndex].columns)):
                columnsToPrintIndexes.append(ind)
        else:
            for columnToPrint in columnsToPrint:
                i = 0
                while i < len(self.tables[tableIndex].columns):
                    if self.tables[tableIndex].columns[i].columnName == columnToPrint:
                        columnsToPrintIndexes.append(i)
                    i += 1

        valsIndexes = []
        for ind in range(
            0, len(self.tables[tableIndex].columns[columnsToPrintIndexes[0]].elements)
        ):
            valsIndexes.append(ind)
        headers = []
        for col in columnsToPrintIndexes:
            headers.append(self.tables[tableIndex].columns[col].columnName)
        rows = []
        for row in valsIndexes:
            rowOut = []
            for index in columnsToPrintIndexes:
                rowOut.append(self.tables[tableIndex].columns[index].elements[row])
            rows.append(rowOut)
            pass
        print(colored(tabulate(rows, headers=headers, tablefmt="orgtbl"), "yellow"))

    def deleteTable(self, tabName):
        tableIndex = -1
        i = 0
        while i < len(self.tables):
            if self.tables[i].tableName == tabName:
                tableIndex = i
                break
            i += 1
        if tableIndex == -1:
            printError("Table not found")
            return False
        self.tables.pop(tableIndex)

    def selectLeftJoinOnCond(
        self,
        tabName1,
        tabName2,
        colToPrint,
        colToAnal,
        colToJoin1,
        colToJoin2,
        condition,
        condVal,
    ):
        print(tabName1, tabName2, colToPrint, colToAnal, colToJoin1, colToJoin2)
        table1Index = -1
        i = 0
        while i < len(self.tables):
            if self.tables[i].tableName == tabName1:
                table1Index = i
                break
            i += 1
        if table1Index == -1:
            printError("Table 1 not found")
            return False
        table2Index = -1
        i = 0
        while i < len(self.tables):
            if self.tables[i].tableName == tabName2:
                table2Index = i
                break
            i += 1
        if table2Index == -1:
            printError("Table 2 not found")
            return False
        colToJoin1Index = -1
        i = 0
        while i < len(self.tables[table1Index].columns):
            if self.tables[table1Index].columns[i].columnName == colToJoin1:
                colToJoin1Index = i
                break
            i += 1
        if colToJoin1Index == -1:
            printError("Column to join 1 not found")
            return False
        colToJoin2Index = -1
        i = 0
        while i < len(self.tables[table2Index].columns):
            if self.tables[table2Index].columns[i].columnName == colToJoin2:
                colToJoin2Index = i
                break
            i += 1
        if colToJoin2Index == -1:
            printError("Column to join 2 not found")
            return False
        print("Indexes found")
        columns = []
        for name in colToPrint:
            columns.append(column(name, False))
        self.createTable("LEFT_JOIN TMPTABLE", columns)
        self.selectNoCond("LEFT_JOIN TMPTABLE", "*")
        # 2 цикла сюда
        self.deleteTable("LEFT_JOIN TMPTABLE")

    def clearTable(self, tabName):
        tableIndex = -1
        i = 0
        while i < len(self.tables):
            if self.tables[i].tableName == tabName:
                tableIndex = i
                break
            i += 1
        if tableIndex == -1:
            printError("Table not found")
            return False
        # self.tables[tableIndex].columns = []
        for col in self.tables[tableIndex].columns:
            col.elements = []
        return True

    def deleteOnCond(self, tabName, colName, condition, condVal):
        tableIndex = -1
        i = 0
        while i < len(self.tables):
            if self.tables[i].tableName == tabName:
                tableIndex = i
                break
            i += 1
        if tableIndex == -1:
            printError("Table not found")
            return
        i = 0
        # rowsToDelete = []
        columnIndex = -1
        while i < len(self.tables[tableIndex].columns):
            if self.tables[tableIndex].columns[i].columnName == colName:
                columnIndex = i
                break
            i += 1
        if columnIndex == -1:
            printError("Column not found")
            return
        while i < len(self.tables[tableIndex].columns[columnIndex].elements):
            if condition(
                self.tables[tableIndex].columns[columnIndex].elements[i], condVal
            ):
                j = 0
                while j < len(self.tables[tableIndex].columns):
                    self.tables[tableIndex].columns[j].elements.pop(i)
                    j += 1
                i -= 2
            i += 1


def rightcond(param1, param2, database, table):
    strToReturn = []
    tableIndex = 0
    i = 0
    while i < len(database.tables):
        if database.tables[i].tableName == table:
            tableIndex = i
            break
        i += 1
    if tableIndex == -1:
        printError("Table not found")
        return
    i = 0
    columnIndex = -1
    while i < len(database.tables[tableIndex].columns):
        if database.tables[tableIndex].columns[i].columnName == param1:
            columnIndex = i
            break
        i += 1
    if columnIndex == -1:
        i = 0
        while i < len(database.tables[tableIndex].columns):
            if database.tables[tableIndex].columns[i].columnName == param2:
                columnIndex = i
                break
            i += 1
        if columnIndex == -1:
            printError("Column not found")
            return
        strToReturn.append(param2)
        strToReturn.append(param1)
    else:
        strToReturn.append(param1)
        strToReturn.append(param2)
    return strToReturn


# print("Creating DB")
# db = DB()
# print("Setting its name as name")
# db.setName("name")
# print("Creating table")
# db.createTable("TableName", [])
