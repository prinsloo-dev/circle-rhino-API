# ensure that docker container jmsdb is running to be able to access the postgress database
# Running this app will start the flask server
# This API will qeury, add, save and delete data from the database.
# The query routine will return data in json format using the exact column name in the
# database, excluding the lock column. Its up to the UI to change the order of data and to
# decide which columns to use.

from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database connection parameters
db_params = {
    'host': 'localhost',
    'dbname': 'jmsdb',
    'user': 'postgres',
    'password': 'postgres',
    'port': '5430'
}
 
# Function to connect to the database
def connect_db():
    connection = psycopg2.connect(**db_params)
    return connection
 
# Route to get query data (GET - read). UI sent payload: (fieldnames, fieldaliases, joinfields)
@app.route('/query', methods=['POST'])
def get_data():
    #try:
    thedata = request.json
    #print(thedata)
    # construct the query command
    fldnames = '' # contains the fields to return (SELECT)
    maintable = '' # main table with fields (FROM)
    joincode = '' # the code used to join fields (JOIN jt1 ON pk1=fk1 JOIN jt2 ON pk2=fk2 ....)
    filtercode = '' # how the selection is filtered (WHERE)
    for item in thedata.keys():
        if item == 'fieldnames': # field names to query
            for index, fldn in enumerate(thedata['fieldnames']):


                # print(index, fldn, thedata['fieldaliases'][index])
                myfield = fldn + ' as ' + thedata['fieldaliases'][index] + ', '
                fldnames = fldnames + myfield
                if maintable == '':
                    maintable = myfield.split('.')[0]
                    if "(" in maintable:
                        posit = maintable.find('(')
                        maintable = maintable[posit+1:]

                # else:
                #     if jointable == '' and myfield.split('.')[0] != maintable:
                #         jointable = myfield.split('.')[0]
        if item == 'joinfields': # tables and fields to do join
            for join in thedata[item]: # itterate through join list
                joincode = joincode + ' LEFT JOIN ' + join['jointable'] + ' ON ' +  join['primarykey'] + '=' + join['foreinkey']
        if item == 'filterfields':
            for fltr in thedata[item]:
                filtercode = filtercode + ' ' + fltr['field'] + '=' + f"""'{fltr['value']}'""" + ' AND'
    filtercode = filtercode + ' ' + maintable + '.lock=false'
    # remove end ', ' and ' = '
    fldnames = fldnames[:-2]
    # print("fieldnames:", fldnames)
    querycode = 'SELECT ' + fldnames + ' FROM ' + maintable
    print('filter code: ', filtercode)
    if len(joincode) > 0:
        querycode = querycode + joincode
    querycode = querycode + ' WHERE' + filtercode
    print('query command: ', querycode)     
    # Connect to the database
    connection = connect_db()
    # Create a cursor
    cursor = connection.cursor()
    # Execute a query
    cursor.execute(f"""{querycode} ORDER BY id ASC""")
    # Fetch all rows
    data = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    #print(colnames)
    #print(data)
    # Close the cursor and connection

    cursor.close()
    connection.close()
    result = []
    for row in data:
        myrow = {}
        for index, coln in enumerate(colnames):
            myrow[coln] = row[index]
        result.append(myrow)

    return jsonify(result)
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500
    
# Route to add new record (POST - create). UI sent payload: (table name, datafield1, datafield2, ...) (no id field)
@app.route('/add', methods=['POST'])
def add_data():
    #print("add data engaged...")
    try:
        # Get data from the request (assuming a JSON payload)
        thedata = request.json
        #print('add data called for table', thedata)
        mykeys = ''
        mydata = ''
        for item in thedata.keys():
            if item == 'table': # first itteration
                table = thedata[item]
            else:
                mykeys = mykeys + item + ', '
                mydata = mydata + "'" + thedata[item] + "', "
        mykeys = (mykeys + 'lock')
        mydata = (mydata + 'false')
        #print(table)
        #print(mykeys)
        #print(mydata)
        # Connect to the database
        connection = connect_db()
        # Create a cursor
        cursor = connection.cursor()
        # first check if the id counter exist
        # cursor.execute(f"""SELECT * FROM {table}""")
        # data = cursor.fetchall()
        # print(len(data))
        # if len(data) == 0:
        #     print('sequence not created, thus create first')
        # Execute a query
        print("adding to db command:",'INSERT INTO', table, '(', mykeys, ') VALUES (', mydata, ')')
        cursor.execute(
            f"""
            INSERT INTO {table} ({mykeys})
            VALUES ({mydata});
            """
        )
        connection.commit()
        # Close the cursor and connection
        cursor.close()
        connection.close()
        # return "success"
        return jsonify({'message': 'record added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
# Route to update record (PATCH - update). UI sent payload: (table name, id, datafield1, datafield2, ...)
@app.route('/save', methods=['PATCH'])
def save_data():
    try:
        # Get data from the request (assuming a JSON payload)
        thedata = request.json
        mysetdata = ''
        print(thedata)
        for item in thedata.keys():
            if item == 'table':
                table = thedata[item]
            elif item == 'id':
                myid = thedata[item]
            else:
                mysetdata = mysetdata + item + "='" + thedata[item] + "', "
        mysetdata = (mysetdata + 'lock=false')
        

        # Connect to the database
        connection = connect_db()
        # Create a cursor
        cursor = connection.cursor()
        # Execute a query
        print('save command: UPDATE', table, ' SET ', mysetdata, 'WHERE id=', myid)
        cursor.execute(
            f"""
                UPDATE {table}
                SET {mysetdata}
                WHERE id={myid}
            """
        )
        connection.commit()
        # Close the cursor and connection
        cursor.close()
        connection.close()
        return jsonify({'message': 'record saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
# Route to delete a record (PATCH - delete - update lock). UI sent payload: (table name, id)
@app.route('/delete', methods=['PATCH'])
def delete_data():
    # only changing lock to true
    try:
        # Get data from the request (assuming a JSON payload)
        thedata = request.json
        table = thedata['table']
        myid = thedata['id']
        # Connect to the database
        connection = connect_db()
        # Create a cursor
        cursor = connection.cursor()
        # Execute a query
        cursor.execute(
            f"""
                UPDATE {table}
                SET lock=true
                where id={myid}
            """
        )
        connection.commit()
        # Close the cursor and connection
        cursor.close()
        connection.close()
        return jsonify({'message': 'record locked successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)





