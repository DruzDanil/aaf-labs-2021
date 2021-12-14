def printError(error):
    print(colored("Error:", "red"), error)


def multiLineInput(promt):
    text = ""
    while True:
        x = input(promt)
        if x == "":
            return multiLineInput(promt)
        if x.lower() == ".exit":
            exit()
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
        # print("Adding", el, "to", self.columnName)
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

    def selectOnCond(
        self,
        tabName,
        columnsToPrint,
        columnToAnal,
        condValue,
        condition,
        isColumn=False,
    ):
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
        if isColumn == False:
            while i < len(self.tables[tableIndex].columns[columnIndex].elements):
                if condition(
                    self.tables[tableIndex].columns[columnIndex].elements[i], condValue
                ):
                    valsIndexes.append(i)
                i += 1
        else:
            i = 0
            column2Index = -1
            while i < len(self.tables[tableIndex].columns):
                if self.tables[tableIndex].columns[i].columnName == condValue:
                    column2Index = i
                    break
                i += 1
            i = 0
            while i < len(self.tables[tableIndex].columns[columnIndex].elements):
                # print((self.tables[tableIndex].columns[columnIndex].elements[i], self.tables[tableIndex].columns[column2Index].elements[i]))
                if condition(
                    self.tables[tableIndex].columns[columnIndex].elements[i], self.tables[tableIndex].columns[column2Index].elements[i]
                ):
                    valsIndexes.append(i)
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
        isColum=False
    ):
        print("selecting left join on cond")
        # print(tabName1, tabName2, colToPrint, colToAnal, colToJoin1, colToJoin2)
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
        # print("Indexes found")
        columns = []
        if colToPrint == "*":
            i = 0
            while i < len(self.tables[table1Index].columns):
                # if self.tables[table1Index].columns[i].columnName == name:
                columns.append(
                    column(self.tables[table1Index].columns[i].columnName, False)
                )
                i += 1
            i = 0
            while i < len(self.tables[table2Index].columns):
                # if self.tables[table1Index].columns[i].columnName == name:
                columns.append(
                    column(self.tables[table2Index].columns[i].columnName, False)
                )
                i += 1
        else:
            for name in colToPrint:
                i = 0
                while i < len(self.tables[table1Index].columns):
                    if self.tables[table1Index].columns[i].columnName == name:
                        columns.append(column(name, False))
                    i += 1
            for name in colToPrint:
                i = 0
                while i < len(self.tables[table2Index].columns):
                    if (
                        self.tables[table2Index].columns[i].columnName == name
                        and i != colToJoin1Index
                    ):
                        columns.append(column(name, False))
                    i += 1
        self.createTable("LEFT_JOIN TMPTABLE", columns)
        # print("bp1")
        # self.selectNoCond("LEFT_JOIN TMPTABLE", "*")
        # print("bp2")
        # 2 цикла сюда
        columnsToPrint1Indexes = []
        columnsToPrint2Indexes = []
        if colToPrint == "*":
            for ind in range(0, len(self.tables[table1Index].columns)):
                columnsToPrint1Indexes.append(ind)
            for ind in range(0, len(self.tables[table2Index].columns)):
                # if ind != colToJoin2Index:
                columnsToPrint2Indexes.append(ind)
        else:
            for name in colToPrint:
                i = 0
                while i < len(self.tables[table1Index].columns):
                    if self.tables[table1Index].columns[i].columnName == name:
                        columnsToPrint1Indexes.append(i)
                    i += 1
            for name in colToPrint:
                i = 0
                while i < len(self.tables[table2Index].columns):
                    if (
                        self.tables[table2Index].columns[i].columnName
                        == name
                        # and i != colToJoin2Index
                    ):
                        columnsToPrint2Indexes.append(i)
                    i += 1
        valueIndexs = []
        i = 0
        while i < len(self.tables[table1Index].columns[colToJoin1Index].elements):
            j = 0
            while j < len(self.tables[table2Index].columns[colToJoin2Index].elements):
                if (
                    self.tables[table1Index].columns[colToJoin1Index].elements[i]
                    == self.tables[table2Index].columns[colToJoin2Index].elements[j]
                ):
                    valueIndexs.append((i, j))
                elif valueIndexs[-1][0] != i:
                    valueIndexs.append((i, -1))
                j += 1
            i += 1
        j = 0
        print(valueIndexs)
        # print("Values:",valueIndexs)
        # print("col 1", columnsToPrint1Indexes)
        # print("col 2", columnsToPrint2Indexes)
        if True:
            while j < len(valueIndexs):
                values = []
                for i in columnsToPrint1Indexes:
                    values.append(
                        self.tables[table1Index].columns[i].elements[valueIndexs[j][0]]
                    )
                for i in columnsToPrint2Indexes:
                    if valueIndexs[j][1] == -1:
                        values.append("")
                    else:
                        values.append(
                            self.tables[table2Index]
                            .columns[i]
                            .elements[valueIndexs[j][1]]
                        )
                #
                self.insertInTable("LEFT_JOIN TMPTABLE", values)
                j += 1

        # print("TMPTABLE filled")
        # print(self.tables[-1])
        # print(
        #     self.tables[-1].columns[0].columnName, self.tables[-1].columns[1].columnName
        # )
        self.selectOnCond("LEFT_JOIN TMPTABLE", "*", colToAnal, condVal, condition, isColumn = isColum)
        self.deleteTable("LEFT_JOIN TMPTABLE")

    def selectLeftJoinNoCond(
        self,
        tabName1,
        tabName2,
        colToPrint,
        colToJoin1,
        colToJoin2,
    ):
        # print("selecting left join")
        # print(tabName1, tabName2, colToPrint, colToAnal, colToJoin1, colToJoin2)
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
        # print("Indexes found")
        columns = []
        if colToPrint == "*":
            i = 0
            while i < len(self.tables[table1Index].columns):
                # if self.tables[table1Index].columns[i].columnName == name:
                columns.append(
                    column(self.tables[table1Index].columns[i].columnName, False)
                )
                i += 1
            i = 0
            while i < len(self.tables[table2Index].columns):
                # if self.tables[table1Index].columns[i].columnName == name:
                columns.append(
                    column(self.tables[table2Index].columns[i].columnName, False)
                )
                i += 1
        else:
            for name in colToPrint:
                i = 0
                while i < len(self.tables[table1Index].columns):
                    if self.tables[table1Index].columns[i].columnName == name:
                        columns.append(column(name, False))
                    i += 1
            for name in colToPrint:
                i = 0
                while i < len(self.tables[table2Index].columns):
                    if (
                        self.tables[table2Index].columns[i].columnName == name
                        and i != colToJoin1Index
                    ):
                        columns.append(column(name, False))
                    i += 1
        self.createTable("LEFT_JOIN TMPTABLE", columns)
        # print("bp1")
        # self.selectNoCond("LEFT_JOIN TMPTABLE", "*")
        # print("bp2")
        # 2 цикла сюда
        columnsToPrint1Indexes = []
        columnsToPrint2Indexes = []
        if colToPrint == "*":
            for ind in range(0, len(self.tables[table1Index].columns)):
                columnsToPrint1Indexes.append(ind)
            for ind in range(0, len(self.tables[table2Index].columns)):
                # if ind != colToJoin2Index:
                columnsToPrint2Indexes.append(ind)
        else:
            for name in colToPrint:
                i = 0
                while i < len(self.tables[table1Index].columns):
                    if self.tables[table1Index].columns[i].columnName == name:
                        columnsToPrint1Indexes.append(i)
                    i += 1
            for name in colToPrint:
                i = 0
                while i < len(self.tables[table2Index].columns):
                    if (
                        self.tables[table2Index].columns[i].columnName
                        == name
                        # and i != colToJoin2Index
                    ):
                        columnsToPrint2Indexes.append(i)
                    i += 1
        valueIndexs = []
        i = 0
        while i < len(self.tables[table1Index].columns[colToJoin1Index].elements):
            j = 0
            while j < len(self.tables[table2Index].columns[colToJoin2Index].elements):
                if (
                    self.tables[table1Index].columns[colToJoin1Index].elements[i]
                    == self.tables[table2Index].columns[colToJoin2Index].elements[j]
                ):
                    valueIndexs.append((i, j))
                elif valueIndexs[-1][0] != i:
                    valueIndexs.append((i, -1))
                j += 1
            i += 1
        j = 0
        # print("Values:",valueIndexs)
        # print("col 1", columnsToPrint1Indexes)
        # print("col 2", columnsToPrint2Indexes)
        if True:
            while j < len(valueIndexs):
                values = []
                for i in columnsToPrint1Indexes:
                    values.append(
                        self.tables[table1Index].columns[i].elements[valueIndexs[j][0]]
                    )
                for i in columnsToPrint2Indexes:
                    if valueIndexs[j][1] == -1:
                        values.append("")
                    else:
                        values.append(
                            self.tables[table2Index]
                            .columns[i]
                            .elements[valueIndexs[j][1]]
                        )

                self.insertInTable("LEFT_JOIN TMPTABLE", values)
                j += 1

        # print("TMPTABLE filled")
        # print(self.tables[-1])
        # print(
        #     self.tables[-1].columns[0].columnName, self.tables[-1].columns[1].columnName
        # )
        self.selectNoCond("LEFT_JOIN TMPTABLE", "*")
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


def rightcond(param1, param2, database, table1, table2 = ""):
    strToReturn = []
    table1Index = -1
    i = 0
    while i < len(database.tables):
        if database.tables[i].tableName == table1:
            table1Index = i
            break
        i += 1
    table2Index = -1
    if table2 != "":   
        i = 0
        while i < len(database.tables):
            if database.tables[i].tableName == table2:
                table2Index = i
                break
            i += 1
    if table2Index == -1 and table1Index == -1:
        printError("Table not found")
        return 
    i = 0
    columnIndex = -1
    if table1Index != -1:
        while i < len(database.tables[table1Index].columns):
            if database.tables[table1Index].columns[i].columnName == param2:
                columnIndex = i
                break
            i += 1
    elif table2Index != -1:
        while i < len(database.tables[table2Index].columns):
            if database.tables[table2Index].columns[i].columnName == param2:
                columnIndex = i
                break
            i += 1
    strToReturn.append(param1)
    strToReturn.append(param2)
    if columnIndex == -1:
        strToReturn.append(False)
    else:
        strToReturn.append(True)
    return strToReturn


# print("Creating DB")
# db = DB()
# print("Setting its name as name")
# db.setName("name")
# print("Creating table")
# db.createTable("TableName", [])
