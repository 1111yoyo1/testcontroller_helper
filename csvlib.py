import os,csv,operator

def GetCsvEntries(csvfile):
    entryList = []
    with open(csvfile, 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            d = {}
            for key in row.keys():
                lowerKey = key.lower()
                try:  # try to convert to numeral
                    d[lowerKey] = eval(row[key])
                except:
                    d[lowerKey] = row[key]
            entryList.append(d)
    return entryList

def GetColumnAllElements(csvfile,columnname):
    caseList = GetCsvEntries(csvfile)
    for column in caseList:
        yield column[columnname]

def GetRowByElement(csvfile,columnname,element):
    caseList = GetCsvEntries(csvfile)
    #print caseList
    for index, column in enumerate(caseList): 
        if column[columnname] == element:
            yield index
            yield column

def IsEmptyGenerator(generator):
    try:
        generator.next()
    except StopIteration:
        return True
    return False

def GetListByElement(csvfile,columnname,element):
    generator = GetRowByElement(csvfile, columnname, element)
    if not IsEmptyGenerator(generator):
        for element in generator:
            return element
    else:
        #print "no found required list by specific element"
        return None

def ReturnCsvColumnNamebyList(listall):
    for dictpart in listall:
        listkey = []
        for key in sorted(dictpart.keys()):
            listkey.append(key)
    return listkey

def GetCsvListbyList(listall):
    list_key_value = []

    list_key_value.append(ReturnCsvColumnNamebyList(listall))

    for dictpart in listall:
        listvalue = []
        for key in sorted(dictpart.keys()):
            listvalue.append(dictpart[key])
        list_key_value.append(listvalue)

    return list_key_value

def WriteToSCVbyList(csvfile,listall):
    with open(csvfile, 'wb') as f:
        writer = csv.writer(f)
        for line in GetCsvListbyList(listall):
            writer.writerow(line)

def RemoveRowbyElement(csvfile,coloumnname, element):
    element = GetListByElement(csvfile,coloumnname, element)
    if element is not None:
        listall = GetCsvEntries(csvfile)
        listall.remove(element)
        WriteToSCVbyList(csvfile,listall)
    else:
        print "fail to remove specific element, no unit exists"

def AddRowbyElement(csvfile, coloumnname, element):
    element = GetListByElement(csvfile, coloumnname, element)
    if element is None:
        listall = GetCsvEntries(csvfile)
        listtmp = AddRow(listall, coloumnname, element)
        listall.append(listtmp)
        WriteToSCVbyList(csvfile,listall)
    else:
        print "fail to add specific element, add unit exists"

def ReplaceRowbyElement(csvfile, coloumnname, element, replace_value):
    element_value = GetListByElement(csvfile, coloumnname, element)
    repl = GetListByElement(csvfile, coloumnname, replace_value)
    if repl is None:
        if element_value is not None:
            listall = GetCsvEntries(csvfile)
            index = listall.index(element_value)
            listall[index][coloumnname] = replace_value
            WriteToSCVbyList(csvfile,listall)
        else:
            print "fail to replace specific element, origianl unit exists"
    else:
        print "fail to replace specific element, replace unit exists"

def SortColoumn(csvfile, coloumnname, element):
    pass

def AddRow(listall, coloumnname, element):
    target_dict = {}
    ColumnTitle = ReturnCsvColumnNamebyList(listall)
    for ele in ColumnTitle:
        if ele == coloumnname:
            target_dict[ele] = element
        else:
            target_dict[ele] = ''
    return target_dict

if __name__ == "__main__":
    csvfile ='TestCases.csv'
    #listall = GetCsvEntries(csvfile)
    #print GetCsvListbyList(listall)
    #RemoveRowbyElement(csvfile,'hostname', 'sh-racka03.lsi.com')
    #ReplaceRowbyElement(csvfile,'hostname', 'sh-racka01.lsi.com', 'sh-racka16.lsi.com')
    #AddRowbyElement(csvfile,'hostname', 'sh-racka16.lsi.com')

    # listall = GetCsvEntries(csvfile)
    # #print listall
    # for dict1 in listall:
    #     #print dict1
    #     dict1 = sorted(dict1.iteritems(), key=operator.itemgetter(1))
    #     #print dict1