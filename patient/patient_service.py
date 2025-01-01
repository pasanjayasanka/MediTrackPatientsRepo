import pymysql.cursors
from flask import Flask, request, jsonify
import pymysql
import os

app = Flask(__name__)

# Database connection details
DB_HOST = 'meditrack-db.cdai64ksezzi.us-east-1.rds.amazonaws.com'  # e.g., 'mydb.c9q5e6c9khnv.us-west-2.rds.amazonaws.com'
DB_USER = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = 'meditrack'

# Function to get a database connection
def get_db_connection():
    return pymysql.connect(host=DB_HOST,
                           user=DB_USER,
                           password=DB_PASSWORD,
                           db=DB_NAME,
                           port=3306,  # Explicitly specifying the port
                           cursorclass=pymysql.cursors.DictCursor)

# POST route to add a new patient
@app.route('/patients', methods=['POST'])
def add_patient():
    patient = request.json
    name = patient.get('name')
    age = patient.get('age')
    current_medical_case = patient.get('current_medical_case')
    medical_history = patient.get('medical_history')
    phone_number = patient.get('phone_number')  # Adjusted to match the column name

    # Insert patient into the database
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO patients (name, age, current_medical_case, medical_history, phone_number) VALUES (%s, %s, %s, %s, %s)",
            (name, age, current_medical_case, medical_history, phone_number)
        )
        conn.commit()

    conn.close()
    return jsonify({"message": "Patient added"}), 201

# GET route to retrieve all patients
@app.route('/patients', methods=['GET'])
def get_patients():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM patients")
        patients = cursor.fetchall()
    
    conn.close()
    return jsonify({"patients": patients})

# PUT route to modify patient data by ID
@app.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    patient = request.json
    name = patient.get('name')
    age = patient.get('age')
    current_medical_case = patient.get('current_medical_case')
    medical_history = patient.get('medical_history')

    # Update patient data in the database
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE patients SET name=%s, age=%s, current_medical_case=%s, medical_history=%s WHERE id=%s",
            (name, age, current_medical_case, medical_history, patient_id)
        )
        conn.commit()
    
    conn.close()
    return jsonify({"message": "Patient updated"}), 200

# DELETE route to delete a patient by ID
@app.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    # Delete patient from the database
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM patients WHERE id=%s", (patient_id,))
        conn.commit()
    
    conn.close()
    return jsonify({"message": "Patient deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
