from flask import Flask, render_template, request
import dbtasks
import sqlite3 
from datetime import datetime

dbname = 'customers.db'

app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
@app.route('/customers', methods = ['POST', 'GET'])
def customers():
   if request.method == 'GET':
      totRec = dbtasks.totRecords()
      #Empty customers dictionary for GET
      customer = {}
      return render_template('customers.html', totRec=totRec, customer=customer)  

   if request.method == 'POST':# and request.value!="Add Customer":
      print(request)
      source = 'post'
      totRec = dbtasks.totRecords()
      customer = request.form
      cusRecords = dbtasks.findCustomers(customer)
      return render_template('customers.html', totRec=totRec, customer=customer, cusRecords=cusRecords, source=source)  
  
   if request.method == 'POST':
      details = request.form
      cusId = details['cusId']
      cusFname = details['cusFname']
      cusLname = details['cusLname']
      cusState = details['cusState']
      cusSalesYTD = details['cusSalesYTD']
      cusSalesPrev = details['cusSalesPrev']
      cur = mysql.connection.cursor()
      cur.execute("INSERT INTO customer(cusId, cusFname, cusLname, cusState, cusSalesYTD, cusSalesPrev) VALUES (%s, %s, %s, %s, %s, %s)", (cusId, cusFname, cusLname, cusState, cusSalesYTD, cusSalesPrev))
      mysql.connection.commit()
      cur.close()
      return render_template('customer.html')

"""delete customer"""
@app.route('/delete/<cusId>', methods = ['POST', 'GET'])
def delete(cusId):
    if request.method == 'GET':
        #Retrieve customer information and send to delete form
        customer = dbtasks.findCustomerById(cusId)
        return render_template('delete.html', customer=customer)

    if request.method == 'POST':
        customer = request.form
        msg = dbtasks.deleteCustomerById(cusId)
        if msg == 1:
            message = 'Customer Deleted Successfully'
        else:
            message = 'Error Deleting Customer.  Error: ' + msg
            
        return render_template('message.html', message=message)

"""update customer"""
@app.route('/update/<cusId>', methods = ['POST', 'GET'])
def update(cusId):
    if request.method == 'GET':
        #Retrieve customer information and send to update form
        source = 'GET'
        customer = dbtasks.findCustomerById(cusId)
        return render_template('update.html', source=source, customer=customer)

    if request.method == 'POST':
        source = 'POST'
        customer = request.form
        msg = dbtasks.updateCustomer(customer)
        if msg == 1:
           message = 'Customer Updated Successfully'
           return render_template('message.html', message=message, customer=customer)  
        else:
           message = 'Error Updating Customer.  Message: ' + msg
           return render_template('update.html', message=message, customer=customer) 

"""add new customer"""
@app.route('/redirect', methods=['GET', 'POST'])
def redirect():
     customer = {}
     totRec = dbtasks.totRecords()
     if request.method == 'POST' or request.method=='GET':
         return render_template('addcustomer.html', customer= customer)
     else:
         return render_template('addcustomer.html', customer= customer)

@app.route('/addcustomers', methods=['GET', 'POST'])
def addnewcustomer():
    con = sqlite3.connect(dbname)
    con.row_factory = sqlite3.Row
    curs = con.cursor()
    if request.method == 'POST':
        customer = request.form
    # Create cursor and execute insert statement
        curs = con.cursor()
    # Use exception handling
        try:
            print(customer)
            curs.execute('INSERT INTO customer(cusId, cusFname, cusLname, cusState, cusSalesYTD, cusSalesPrev) VALUES(?, ?, ?, ?, ?, ?)', (int(customer['cusId']),customer['cusFname'],customer['cusLname'],customer['cusState'],int(customer['cusSalesYTD']),int(customer['cusSalesPrev'])))
        except sqlite3.IntegrityError:
            print('Record already exists', customer)
            with open('insert_er.txt', mode='a') as errorfile:
                for item in customer:
                    print(item, end=' ', file=errorfile)
                print(file=errorfile)
        except Exception as e:
            print('exception', str(e))
        con.commit()
        con.close()
    customer={}
    return render_template('addcustomer.html',customer=customer)

"""reports code"""
@app.route('/', methods = ['POST', 'GET'])
@app.route('/reports', methods = ['POST', 'GET'])
def reports():
    if request.method == 'GET':
        source = 'GET'
        totRec = dbtasks.totRecords()
        return render_template('reports.html', source=source, totRec=totRec)

    if request.method == 'POST':
        source = 'POST'
        report = request.form
        result = dbtasks.reports(report['report'])
        #return render_template('reports.html', msg=msg, totRec=totRec, status=status, file=file)
        return render_template('reports.html', source=source, result=result)

"""import code"""
def sql_insert_customer(collection, errfile):
    #create cursor and execute insert statement
    con = sqlite3.connect('customers.db')
    curs = con.cursor()
    #Use exception handling
    try:
        curs.execute('INSERT INTO customer(cusId, cusFname, cusLname, cusState, cusSalesYTD, cusSalesPrev) VALUES(?, ?, ?, ?, ?, ?)', collection)
    except sqlite3.IntegrityError as e:
        with open(errfile, mode='a') as errorfile:
            for item in collection:
                print(item, end=' ', file=errorfile)
            print(file=errorfile)
        return 'Error' + str(e)
    except Exception as e:
        print('exception', str(e))
        return 'Error' + str(e)
    con.commit()
    return 'Success'

@app.route('/imports')
def imports():
   return render_template('imports.html')
   
@app.route('/importresult', methods = ['POST','GET'])
def importresult():
   if request.method == 'POST':
      files = request.form
      txtfile = files['txtfile'] 
      dbfile = files['dbfile']
      print(dbfile)
      errorfile = 'input_error.txt'
      status = 'Success'
      customer={}
      with open(txtfile, mode='r') as stufile:
        for record in stufile:
          rec = record.split()
          msg = sql_insert_customer(rec, errorfile)
          if msg != 'Success':
            status = msg 
          if msg == 'Success':
              customer[rec[0]]=rec[1]
        return render_template('importresult.html', status = status, errorfile = errorfile ,customer=customer) 

"""Export code"""
@app.route('/exports')
def exports():
    totRec = dbtasks.totRecords()
    return render_template('exports.html', totRec = totRec)

@app.route('/exportresult', methods = ['POST','GET'])
def exportresult():
    if request.method == 'POST':
        files = request.form
        totRec = dbtasks.totRecords()
        txtfile = files['export']
        errorfile = 'experror.txt'
        status = dbtasks.export_cust(txtfile)
        return render_template('exportresult.html', totRec=totRec, status = status, files = files, errorfile = errorfile)

if __name__ == '__main__':
      app.run(debug = True)

