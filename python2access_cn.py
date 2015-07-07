# -*- coding: cp936 -*-
import win32com.client
import pypyodbc
import random

def randomWords_cn():

    randomNum = random.randint(1, 157658)

    conn = win32com.client.Dispatch(r'ADODB.Connection')   
    DSN = 'PROVIDER=Microsoft.Jet.OLEDB.4.0;DATA SOURCE=./database/cnword.mdb;'   
    conn.Open(DSN)

    rs = win32com.client.Dispatch(r'ADODB.Recordset')   
    rs_name = 'Words'
    rs.Cursorlocation = 3 # don't use parenthesis here   
    rs.Open('Select * FROM [cnword] where ID = ' + str(randomNum), conn) # be sure conn is open
    return rs.Fields.Item(1).Value
#rs.Open('Select * FROM [cnword]', conn)
#print rs.RecordCount # no parenthesis here either   
