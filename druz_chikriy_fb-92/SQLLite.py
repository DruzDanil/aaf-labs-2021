from pyparsing import *
from classes import *
from conditions import *


def isKeywordToStart(word):
    word = word.lower()
    keywords = ["insert", "create", "select", "delete"]
    for key in keywords:
        if key == word:
            return True
    return False


def whatcond(cond, mod):
    # print(mod, cond)
    if mod:
        return {
            cond == "=": equal,
            cond == "!=": notequal,
            cond == ">": more,
            cond == "<": less,
            cond == ">=": moreorequal,
            cond == "=>": moreorequal,
            cond == "<=": lessorequal,
            cond == "=<": lessorequal,
        }[True]
    else:
        return {
            cond == "=": equal,
            cond == "!=": notequal,
            cond == ">": less,
            cond == "<": more,
            cond == ">=": moreorequal,
            cond == "=>": moreorequal,
            cond == "<=": lessorequal,
            cond == "=<": lessorequal,
        }[True]


##
# PyParse regular expressions
##
name = Word(initChars=alphas, bodyChars=(alphanums + "_"))
colum = Group(name + Optional(CaselessLiteral("INDEXED")))
colums = delimitedList(colum, delim=",")("colums")
command_create = CaselessLiteral("CREATE") + name("table_name") + "(" + colums + ");"
value = QuotedString('"')
values = delimitedList(value, delim=",")
command_insert = (
    CaselessLiteral("INSERT")
    + Optional(CaselessLiteral("INTO"))
    + name("table_name")
    + "("
    + values("value")
    + ");"
)
operator = oneOf("= != > < >= <= => =<")
condition = (
    (name | value)("condition_column_name")
    + operator("operator")
    + (name | value)("value")
)("condition")
select_colums = delimitedList(name, delim=",")
command_select = (
    CaselessLiteral("SELECT")
    + ("*" | select_colums)("select_colum_names")
    + CaselessLiteral("FROM")
    + name("table1_name")
    + Optional(
        CaselessLiteral("LEFT_JOIN")
        + name("table2_name")
        + CaselessLiteral("ON")
        + name("t1_column")
        + "="
        + name("t2_column")
    )("left_join")
    + Optional(CaselessLiteral("WHERE") + condition)
    + ";"
)
command_delete = (
    CaselessLiteral("DELETE")
    + Optional(CaselessLiteral("FROM"))
    + name("table_name")
    + Optional(CaselessLiteral("WHERE") + condition)
    + ";"
)
##
#
##


debug = False
cmdfile = ""
Database = DB()
Database.setName("NewDataBase")
print("Welcome to lab1!\nEnter cmds")
while cmdfile != ".EXIT":
    try:
        cmdfile = multiLineInput(colored("sqllite:", "green"))
        while True:
            if cmdfile[0] == " " or cmdfile[0] == "\t" or cmdfile[0] == "\n":
                cmdfile = cmdfile[1:]
            else:
                break
        if cmdfile == "debug":
            if debug:
                debug = False
                print("Debug mode off")
                continue
            else:
                debug = True
                print("Debug mode on")
                continue
        cmdsRaw = []
        buffer = []
        if (
            cmdfile.find(";") == -1
            and cmdfile.upper() != ".EXIT"
            and cmdfile != "debug"
        ):
            printError("Syntax error - command sholud end with ;")
            continue
        for line in cmdfile:
            if line.find(";") != -1:
                buffer.append(line[0 : line.find(";")])
                cmdsRaw.append(buffer)
                buffer = []
            else:
                buffer.append(line)

        if debug:
            print(cmdsRaw)

        cmds = []

        for cmd in cmdsRaw:
            cmds.append("".join(cmd))

        if debug:
            print(cmds)

        i = 0
        while i < len(cmds):
            cmds[i] = cmds[i].replace("\n", " ")
            cmds[i] = cmds[i].replace("\t", " ")
            cmds[i] = cmds[i].replace("\r", " ")
            i += 1

        if debug:
            print(cmds)

        buffer = []
        for cmd in cmds:
            if not isKeywordToStart(cmd.split(" ")[0]) or len(cmd.split('"')) % 2 != 1:
                print("Unsupported command: " + cmd)
                buffer.append(cmd)

        for wrongCMD in buffer:
            cmds.remove(wrongCMD)

        if debug:
            print(cmds)

        parsedCmds = []
        # buffer = []
        i = 0
        for cmd in cmds[:]:
            cmds[i] = cmds[i] + ";"
            i = i + 1

        for cmd in cmds:
            cmdtype = cmd.split(" ")[0].lower()
            if cmdtype == "create":
                try:
                    parsed = command_create.parseString(cmd)
                except ParseException as pe:
                    printError(
                        "Command is wrond\n" + pe + "\nСolumn: {}".format(pe.column)
                    )
                else:
                    # print("Creating table...")
                    columnn = []
                    for i in parsed.colums:
                        if len(i) == 1:
                            columnn.append(column(i[0], False))
                        else:
                            columnn.append(column(i[0], True))

                   
                    if Database.createTable(parsed.table_name, columnn) == -1:
                        break
                    # print("Database tables debug:", Database.tables)
                    print('Table "' + parsed.table_name + '" was created.')
                    # print("Created table contains the following columns:")
                    for i in parsed.colums:
                        if len(i) == 1:
                            print(i[0] + " - non-indexed")
                        else:
                            print(i[0] + " - indexed")
                pass
            if cmdtype == "insert":
                try:
                    parsed = command_insert.parseString(cmd)
                except ParseException as pe:
                    printError(
                        "Command is wrond\n" + pe + "\nСolumn: {}".format(pe.column)
                    )
                else:
                    if Database.insertInTable(parsed.table_name, parsed.value):
                        print(
                            '1 row has been inserted into "' + parsed.table_name + '".'
                        )
                        print("Created row contains the following values:")
                        for i in parsed.value:
                            print(i)
                    # for i in Database.tables[0].columns:
                    #     print(i.columnName)
                    #     print(i.elements)
            if cmdtype == "select":
                try:
                    parsed = command_select.parseString(cmd)
                except ParseException as pe:
                    printError(
                        "Command is wrond\n" + pe + "\nСolumn: {}".format(pe.column)
                    )
                else:
                    c = False
                    for b in parsed:
                        if b.lower() == "where":
                            c = True
                    if (
                        parsed[1] == "*" and c == True and parsed.left_join == ""
                    ):  # c == True -- есть условие  c != True -- условия нет
                        print(
                            'All rows has been selected from table "'
                            + parsed.table1_name
                            + '"'
                        )
                        str = Database.rightcond(
                            parsed.condition_column_name,
                            parsed.value,
                            parsed.table1_name,
                        )
                        if str != None:
                            # print("Selecting...")
                            if str[0] == parsed.condition_column_name:
                                Database.selectOnCond(
                                    parsed.table1_name,
                                    "*",
                                    str[0],
                                    str[1],
                                    whatcond(parsed.operator, True),
                                    parsed.operator,
                                    isColumn=str[2],
                                )
                                # print(str[2])
                            else:
                                Database.selectOnCond(
                                    parsed.table1_name,
                                    "*",
                                    str[0],
                                    str[1],
                                    whatcond(parsed.operator, False),
                                    parsed.operator,
                                    isColumn=str[2],
                                )
                            # print("Selected rows satisfying following condition:")
                            a = ""
                            for i in parsed.condition:
                                a = a + " " + i
                            print(a)
                    elif parsed[1] == "*" and c != True and parsed.left_join == "":
                        Database.selectNoCond(parsed.table1_name, "*")
                        print(
                            'All rows has been selected from table "'
                            + parsed.table1_name
                            + '"'
                        )
                    elif parsed[1] != "*" and c == True and parsed.left_join == "":
                        str = Database.rightcond(
                            parsed.condition_column_name,
                            parsed.value,
                            parsed.table1_name,
                        )
                        print(parsed.operator)
                        if str != None:
                            if str[0] == parsed.condition_column_name:
                                Database.selectOnCond(
                                    parsed.table1_name,
                                    parsed.select_colum_names,
                                    str[0],
                                    str[1],
                                    whatcond(parsed.operator, True),
                                    parsed.operator,
                                    isColumn=str[2],
                                )
                            else:
                                Database.selectOnCond(
                                    parsed.table1_name,
                                    parsed.select_colum_names,
                                    str[0],
                                    str[1],
                                    whatcond(parsed.operator, False),
                                    parsed.operator,
                                    isColumn=str[2],
                                )
                            print(
                                'Rows has been selected from "'
                                + parsed.table1_name
                                + '":'
                            )
                            print("Selected rows satisfying following condition:")
                            a = ""
                            for i in parsed.condition:
                                a = a + i
                                a = a + " "
                            print(a)
                    elif parsed[1] != "*" and c != True and parsed.left_join == "":
                        Database.selectNoCond(
                            parsed.table1_name, parsed.select_colum_names
                        )
                        print(
                            'Rows has been selected from "' + parsed.table1_name + '":'
                        )
                    elif parsed[1] == "*" and c != True and parsed.left_join != "":
                        Database.selectLeftJoinNoCond(
                            parsed.table1_name,
                            parsed.table2_name,
                            "*",
                            parsed.t1_column,
                            parsed.t2_column,
                        )
                        print(
                            'All rows has been selected from table "'
                            + parsed.table1_name
                            + '"'
                        )
                    elif parsed[1] != "*" and c == True and parsed.left_join != "":
                        print(
                            parsed.condition_column_name,
                            parsed.value,
                            Database,
                            parsed.table1_name,
                            parsed.table2_name,
                        )
                        str = Database.rightcond(
                            parsed.condition_column_name,
                            parsed.value,
                            parsed.table1_name,
                            table2=parsed.table2_name,
                        )
                        print(str)
                        if str != None:
                            print(
                                parsed.table1_name,
                                parsed.table2_name,
                                parsed.select_colum_names,
                                str[0],  # col to analyze
                                parsed.t1_column,
                                parsed.t2_column,
                                whatcond(parsed.operator, True),
                                str[1],  # condval
                                parsed.operator,
                                str[2],
                            )
                            if str[0] == parsed.condition_column_name:
                                Database.selectLeftJoinOnCond(
                                    parsed.table1_name,
                                    parsed.table2_name,
                                    parsed.select_colum_names,
                                    str[0],  # col to analyze
                                    parsed.t1_column,
                                    parsed.t2_column,
                                    whatcond(parsed.operator, True),
                                    str[1],  # condval
                                    parsed.operator,
                                    isColum=str[2],
                                )
                            else:
                                Database.selectLeftJoinOnCond(
                                    parsed.table1_name,
                                    parsed.table2_name,
                                    parsed.select_colum_names,
                                    str[0],
                                    parsed.t1_column,
                                    parsed.t2_column,
                                    whatcond(parsed.operator, False),
                                    str[1],
                                    parsed.operator,
                                    isColum=str[2],
                                )
                            print(
                                'Rows has been selected from "'
                                + parsed.table1_name
                                + '":'
                            )
                            print("Selected rows satisfying following condition:")
                            a = ""
                            for i in parsed.condition:
                                a = a + i
                                a = a + " "
                            print(a)
                    elif parsed[1] != "*" and c != True and parsed.left_join != "":
                        Database.selectLeftJoinNoCond(
                            parsed.table1_name,
                            parsed.table2_name,
                            parsed.select_colum_names,
                            parsed.t1_column,
                            parsed.t2_column,
                        )
                        print(
                            'Rows has been selected from "' + parsed.table1_name + '":'
                        )
                    elif parsed[1] == "*" and c == True and parsed.left_join != "":
                        print(
                            'All rows has been selected from table "'
                            + parsed.table1_name
                            + '"'
                        )
                        str = Database.rightcond(
                            parsed.condition_column_name,
                            parsed.value,
                            parsed.table1_name,
                            parsed.table2_name,
                        )
                        if str != None:
                            if str[0] == parsed.condition_column_name:
                                Database.selectLeftJoinOnCond(
                                    parsed.table1_name,
                                    parsed.table2_name,
                                    "*",
                                    str[0],
                                    parsed.t1_column,
                                    parsed.t2_column,
                                    whatcond(parsed.operator, True),
                                    str[1],
                                    parsed.operator,
                                    isColum=str[2],
                                )
                            else:
                                Database.selectLeftJoinOnCond(
                                    parsed.table1_name,
                                    parsed.table2_name,
                                    "*",
                                    str[0],
                                    parsed.t1_column,
                                    parsed.t2_column,
                                    whatcond(parsed.operator, False),
                                    str[1],
                                    parsed.operator,
                                    isColum=str[2],
                                )
                            print("Selected rows satisfying following condition:")
                            a = ""
                            for i in parsed.condition:
                                a = a + i
                            print(a)
            if cmdtype == "delete":
                try:
                    parsed = command_delete.parseString(cmd)
                except ParseException as pe:
                    printError(
                        "Command is wrond\n" + pe + "\nСolumn: {}".format(pe.column)
                    )
                else:
                    c = False
                    for b in parsed:
                        if b.lower() == "where":
                            c = True
                    str = Database.rightcond(
                        parsed.condition_column_name,
                        parsed.value,
                        parsed.table_name,
                    )
                    if c:
                        if str != None:
                            if str[0] == parsed.condition_column_name:
                                Database.deleteOnCond(
                                    parsed.table_name,
                                    str[0],
                                    whatcond(parsed.operator, True),
                                    str[1],
                                    isColumn = str[2]
                                )
                            else:
                                Database.deleteOnCond(
                                    parsed.table_name,
                                    str[0],
                                    whatcond(parsed.operator, False),
                                    str[1],
                                    isColumn = str[2]
                                )

                            print(
                                'Rows has been deleted from "'
                                + parsed.table_name
                                + '".'
                            )
                            print("Deleted rows satisfying following condition:")
                            a = ""
                            for i in parsed.condition:
                                a = a + i
                            print(a)
                    else:
                        # print(parsed.table_name)
                        if Database.clearTable(parsed.table_name):
                            print('Table "' + parsed.table_name + '" was cleaned.')
                pass
    except Exception:
        printError("Unknown error")
