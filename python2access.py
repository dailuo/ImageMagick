# -*- coding: cp936 -*-
import win32com.client
import pypyodbc
import random
def randomWords():
    randomNum = random.randint(1, 15328)

    conn = win32com.client.Dispatch(r'ADODB.Connection')   
    DSN = r'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=./database/enword.mdb;'   
    conn.Open(DSN)

    rs = win32com.client.Dispatch(r'ADODB.Recordset')   
    rs_name = 'Words'
    rs.Cursorlocation = 3 # don't use parenthesis here   
    rs.Open('Select * FROM [Words] where ID = '+str(randomNum), conn) # be sure conn is open
    return rs.Fields.Item(1).Value
    #rs.Open('Select * FROM [Words]', conn)
    #print rs.RecordCount # no parenthesis here either
    #15328

    #conn = pypyodbc.connect('Driver={Microsoft Access Driver (*.mdb)};DBQ=./EnWords_access.mdb')
    #cur = conn.cursor()
    #cur.execute('''SELECT * FROM saleout WHERE product_name LIKE '%Huawei%'''')
