from flask import Flask, request, jsonify

app = Flask(__name__)
patients = []

@app.route('/patients', methods=['POST'])
def add_patient():
    patient = request.json
    patients.append(patient)
    return jsonify({"message": "Patient added", "patients": patients}), 201

@app.route('/patients', methods=['GET'])
def get_patients():
    return jsonify({"patients": patients})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
