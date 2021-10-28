from pyparsing import *
name = Word(initChars=alphas, bodyChars=(alphanums+'_'))
colum = Group(name + Optional(CaselessLiteral('INDEXED')))
colums = delimitedList(colum, delim=',')('colums')
command_create = CaselessLiteral('CREATE') + name('table_name') + '('+colums+');'
value = Suppress('“') + Word(printables, excludeChars='“') + Suppress('”')
values = delimitedList(value, delim = ',')('value')
command_insert = CaselessLiteral('INSERT') + Optional(CaselessLiteral('INTO')) + name('table_name') + '(' + values + ');'
operator = oneOf("= != > < >= <=")
condition = ((name('condition_column_name1') | value) + operator + (name('condition_column_name2') | value))('condition')
command_select = CaselessLiteral('SELECT') + ('*'|name('select_column_name')+ZeroOrMore(','+ name))('select_colum_names') + CaselessLiteral('FROM') + name('table1_name') + Optional(CaselessLiteral('LEFT_JOIN') + name('table2_name') + CaselessLiteral('ON') + name('t1_column') + '=' + name('t2_column')) + Optional(CaselessLiteral('WHERE') + condition) + ';'
command_delete = CaselessLiteral('DELETE') + Optional(CaselessLiteral('FROM')) + name('table_name') + Optional(CaselessLiteral('WHERE') + condition) + ';'
###
#Релятивная модель, тип данных - строки
#Перечень комманд:
#   CREATE table_name (column_name [INDEXED] [, ...]);
#   INSERT [INTO] table_name (“value” [, ...]);
#   SELECT ( * | column_name [, ...]) 
#       FROM table_name_1
#       [LEFT_JOIN table_name_2 ON t1_column = t2_column]
#       [WHERE condition];
#   DELETE [FROM] table_name [WHERE condition];
###

#from pyparsing import *
def isKeywordToStart(word):
    word = word.lower()
    keywords = ['insert', 'create', 'select', 'delete']
    for key in keywords:
        if key == word:
            return True
    return False

debug = True

print("Welcome to lab1!\nEnter cmd file path:")
INPT = "cmd.txt"
if not debug:
    INPT = input()
else:
    print("cmd.txt")


try:
    cmdfile = open(INPT, 'r')
    print("File opened")
except Exception:
    print("Unable to open file")
    exit()

cmdsRaw = []
buffer = []

for line in cmdfile:
    if line.find(";") != -1:
        buffer.append(line[0:line.find(";")])
        cmdsRaw.append(buffer)
        buffer = []
    else:
        buffer.append(line)

if debug:
    print(cmdsRaw)

cmds = []

for cmd in cmdsRaw:
    cmds.append(''.join(cmd))

if debug:
    print(cmds)

i = 0
while i < len(cmds):
    cmds[i] = cmds[i].replace('\n',' ')
    cmds[i] = cmds[i].replace('\t',' ')
    cmds[i] = cmds[i].replace('\r',' ')
    i += 1

if debug:
    print(cmds)

buffer = []
for cmd in cmds:
    if not isKeywordToStart(cmd.split(' ')[0]) or len(cmd.split("\"")) %2 != 1:
        print("Unsupported command: " + cmd)
        buffer.append(cmd)

for wrongCMD in buffer:
    cmds.remove(wrongCMD)

if debug:
    print(cmds)

parsedCmds = []
#buffer = []
i = 0
for cmd in cmds[:]:
    cmds[i] = cmds[i] + ';'
    i = i+1
print(cmds)
for cmd in cmds:
        cmdtype = cmd.split(' ')[0].lower()
        if cmdtype == 'create':
            try:
                parsed = command_create.parseString(cmd)
            except ParseException as pe:
                print('Command is wrond')
                print(pe)
                print('Сolumn: {}'.format(pe.column))
            else:
                print('Table "' + parsed.table_name + '" was created.')
                print('Created table contains the following columns:')
                for i in parsed.colums:
                    if (len(i) == 1):
                        print(i[0] + ' - non-indexed')
                    else:
                        print(i[0] + ' - indexed')
            pass
        if cmdtype == 'insert':
            try:
                parsed = command_insert.parseString(cmd)
            except ParseException as pe:
                print('Command is wrond')
                print(pe)
                print('Сolumn: {}'.format(pe.column))
            else:
                print('1 row has been inserted into "' + parsed.table_name + '".')
                print('Created row contains the following values:')
                for i in parsed.value:
                    print(i)
            pass
        if cmdtype == 'select':
            try:
                parsed = command_select.parseString(cmd)
            except ParseException as pe:
                print('Command is wrond')
                print(pe)
                print('Сolumn: {}'.format(pe.column))
            else:
                if parsed[1]=='*':
                    print('All rows has been selected from table "' + parsed.table1_name + '"')
                else:
                    print('Rows has been selected from "' + parsed.table1_name + '".')
                c = False
                for b in parsed:
                    if(b.lower() == 'where'):
                        c = True
                if (c):
                    print('Selected rows satisfying following condition:')
                    a = ''
                    for i in parsed.condition:
                        a = a + i
                    print(a)
            pass
        if cmdtype == 'delete':
            try:
                parsed = command_delete.parseString(cmd)
            except ParseException as pe:
                print('Command is wrond')
                print(pe)
                print('Сolumn: {}'.format(pe.column))
            else:
                c = False
                for b in parsed:
                    if(b.lower() == 'where'):
                        c = True
                
                if(c):
                    print('Rows has been deleted from "' + parsed.table_name + '".')
                    print('Deleted rows satisfying following condition:')
                    a = ''
                    for i in parsed.condition:
                        a = a + i
                    print(a)
                else:
                    if(parsed[1].lower() != 'from'):
                        print('Table "' + parsed.table_name + '" was deleted.')
                    else:
                        print('Table "' + parsed.table_name + '" was cleaned.')
            pass
