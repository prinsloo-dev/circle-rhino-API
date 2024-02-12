# ensure that docker container jmsdb is running to be able to access the postgress database
# Running this app will start the flask server

from flask import Flask, jsonify, request
import psycopg2
 
app = Flask(__name__)
 
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
 
# Route to get query data (GET - read). UI sent payload: (table name)
@app.route('/query', methods=['GET'])
def get_data():
    try:
        thedata = request.json
        for item in thedata.keys():
            if item == 'table': # first itteration
                table = thedata[item]
        # Connect to the database
        connection = connect_db()
        # Create a cursor
        cursor = connection.cursor()
        # Execute a query
        cursor.execute(f"""SELECT * FROM {table} WHERE lock=false ORDER BY id ASC""")
        # Fetch all rows
        data = cursor.fetchall()
        # Close the cursor and connection
        cursor.close()
        connection.close()
        # Convert the result to a list of dictionaries for JSON response
        if table == 'customers':
            result = [{'id': row[0],
                        #'lock': row[1],
                        'address': row[2],
                        'tel_no': row[3],
                        'email': row[4],
                        'company_name': row[5],
                        'contact_person': row[6],
                        'contact_role': row[7]
                       } for row in data]
        if table == 'quotes':
            result = [{'id': row[0],
                        #'lock': row[1],
                        'quote_date': row[2],
                        'fitment_date': row[3],
                        'completion_date': row[4],
                        'total_price': row[5],
                        'customer_id': row[6],
                        'quote_no': row[7],
                        'status': row[8],
                        'fitment_address': row[9],
                        'status_reason': row[10]
                        } for row in data]
        if table == 'qoute_lines':
            result = [{'id': row[0],
                        #'lock': row[1],
                        'price': row[2],
                        'quotes_id': row[3],
                        'products_id': row[4],
                        'status': row[5],
                        'name': row[6],
                        'description': row[7],
                        'size': row[8],
                        'quantity': row[9]
                        } for row in data]
        if table == 'jobs':
            result = [{'id': row[0],
                        #'lock': row[1],
                        'job_date': row[2],
                        'quote_lines_id': row[3],
                        'job_no': row[4]
                        } for row in data]
        if table == 'departments':
            result = [{'id': row[0],
                        'name': row[1],
                        'entity_name': row[2]
                        } for row in data]
        if table == 'jobs_history':
            result = [{'id': row[0],
                        #'lock': row[1], 
                        'action_date': row[2],
                        'jobs_id': row[3], 
                        'departments_id': row[4],
                        'action_employees_id': row[5],
                        'owner_employees_id': row[6],
                        'status': row[7],
                        'payment': row[8],
                        'comment': row[9]
                       } for row in data]
        if table == 'employees':
            result = [{'id': row[0],
                       #'lock': row[1],
                        'appointment_date': row[2],
                        'termination_date': row[3],
                        'home_address': row[4],
                        'tel_no': row[5],
                        'email': row[6],
                        'name': row[7],
                        'surname': row[8],
                        'departments_id': row[9],
                        'employee_no': row[10],
                        'sa_id_number': row[11],
                        } for row in data]
        if table == 'products':
            result = [{'id': row[0],
                       #'lock': row[1],
                       'price': row[2],
                       'item_name': row[3],
                       'description': row[4], 
                       } for row in data]
        # add if statements for other tables
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Route to add new record (POST - create). UI sent payload: (table name, datafield1, datafield2, ...) (no id field)
@app.route('/add', methods=['POST'])
def add_data():
    try:
        # Get data from the request (assuming a JSON payload)
        thedata = request.json
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

        # Connect to the database
        connection = connect_db()
        # Create a cursor
        cursor = connection.cursor()
        # Execute a query
        cursor.execute(
            f"""
            INSERT INTO {table} ({mykeys})
            VALUES
            ({mydata});
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
        for item in thedata.keys():
            if item == 'table': # first itteration
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
        cursor.execute(
            f"""
                UPDATE {table}
                SET {mysetdata}
                where id={myid}
            """
        )
        connection.commit()
        # Close the cursor and connection
        cursor.close()
        connection.close()
        # return "success"
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
        for item in thedata.keys():
            if item == 'table': # first itteration
                table = thedata[item]
            if item == 'id':
                myid = thedata[item]
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





