import sqlite3 
from datetime import datetime

dbname = 'customers.db'

def totRecords():
    # Assume no errors, can add try except blocks
    con = sqlite3.connect(dbname)
    curs = con.cursor()
    curs.execute('SELECT COUNT(*) FROM customer')
    record = curs.fetchall()
    con.close()
    return record[0][0]

def findCustomers(pDict): 
    sqlCmd = "1 = 1"
    if pDict['cusId'] != '':
        sqlCmd += " and cusId = " + pDict['cusId'].upper()
    if pDict['cusFname'] != '':
        sqlCmd += " and upper(cusFname) like '" + pDict['cusFname'].upper() + "%'"
    if pDict['cusLname'] != '':
        sqlCmd += " and upper(cusLname) like '" + pDict['cusLname'].upper() + "%'"
    if pDict['cusState'] != '':
        sqlCmd += " and cusState = " + pDict['cusState'].upper()
    if pDict['cusSalesYTD'] != '':
        sqlCmd += ' and cusSalesYTD >= ' + pDict['cusSalesYTD']
    if pDict['cusSalesPrev'] != '':
        sqlCmd += ' and cusSalesPrev >= ' + pDict['cusSalesPrev']

    sqlCmd = 'SELECT * FROM customer WHERE ' + sqlCmd

    con = sqlite3.connect(dbname)
    con.row_factory = sqlite3.Row
    curs = con.cursor()
    try:
        curs.execute(sqlCmd)
        record = curs.fetchall()
    except Exception as e:
        return ('Error ' + str(e))
    else:
        return record    
    finally:
        con.close()

def findCustomerById(cusId):
    sqlCmd = 'SELECT * FROM customer WHERE cusId = ?'

    con = sqlite3.connect(dbname)
    con.row_factory = sqlite3.Row
    curs = con.cursor()
    try:
        curs.execute(sqlCmd, (cusId,))
        record = curs.fetchall()
    except Exception as e:
        return ('Error ' + str(e))
    else:
        return record    
    finally:
        con.close()   

"""delete customer"""
def deleteCustomerById(cusId):
    sqlCmd = 'DELETE FROM customer WHERE cusId = ?'
    con = sqlite3.connect(dbname)
    con.row_factory = sqlite3.Row
    curs = con.cursor()
    try:
        curs.execute(sqlCmd, (cusId,))
        rowcount = curs.rowcount
        con.commit()
    except Exception as e:
        return ('Error ' + str(e))
    else:
        return rowcount   
    finally:
        con.close()  

"""update customer"""
def updateCustomer(pDict):
    con = sqlite3.connect(dbname)
    curs = con.cursor()
    try:
        sqlCmd = """UPDATE CUSTOMER 
                    SET cusFname = ?, cusLname = ?, cusState = ?, cusSalesYTD = ?, cusSalesPrev = ?
                    WHERE cusId = ?"""
        curs.execute(sqlCmd, (pDict['cusFname'], pDict['cusLname'], pDict['cusState'],int(pDict['cusSalesYTD']), int(pDict['cusSalesPrev']), int(pDict['cusId'])))
        rowcount = curs.rowcount
        con.commit()
    except Exception as e:
        return ('Error ' + str(e))
    else:
        return rowcount
    finally:
        con.close()
"""Export code"""
def export_cust(filename):
    con = sqlite3.connect(dbname)
    con.row_factory = sqlite3.Row
    curs = con.cursor()
    sqlcmd = """SELECT * FROM customer """
    curs.execute(sqlcmd)
    records = curs.fetchall()
    try:
        with open(filename, mode = 'w') as file:
            for customer in records:
                print(customer['cusId'],customer['cusFname'],customer['cusLname'],customer['cusState'],customer['cusSalesYTD'],customer['cusSalesPrev'])
    except Exception as e:
        return ('Error ' + str(e))
    return 'Success'
    con.close()

"""reports code"""
def reports(id):
    if id == '1':
        sqlCmd = """ SELECT *
                     FROM customer 
                     ORDER BY cusLname, cusFname """
    elif id =='2':
        sqlCmd = """ SELECT *
                     FROM customer 
                     ORDER BY cusSalesYTD DESC"""
    else:
        sqlCmd = """ SELECT *
                     FROM customer 
                     ORDER BY RANDOM() LIMIT 3 """

    con = sqlite3.connect(dbname)
    con.row_factory = sqlite3.Row
    curs = con.cursor()

    try:
        curs.execute(sqlCmd)
        records = curs.fetchall()

    except Exception as e:
        return 'error ' + str(e)
    
    else:
        return records

    finally:
        con.close()