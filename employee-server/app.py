from flask import Flask, request, jsonify
from models import Database
from services import EmployeeService
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS so that our front-end (hosted elsewhere) can call this API

# Configure your database connection here
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "employee_db"
}

db = Database(**db_config)
employee_service = EmployeeService(db)

@app.route('/api/employees', methods=['GET'])
def get_employees():
    employees = employee_service.get_all_employees()
    # Convert Employee objects to dictionaries
    employees_dicts = [emp.__dict__ for emp in employees]
    return jsonify(employees_dicts), 200

@app.route('/api/employees/<int:emp_id>', methods=['GET'])
def get_employee(emp_id):
    employee = employee_service.get_employee_by_id(emp_id)
    if not employee:
        return jsonify({"message": "Employee not found"}), 404
    return jsonify(employee.__dict__), 200

@app.route('/api/employees', methods=['POST'])
def create_employee():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid request data"}), 400

    new_id = employee_service.create_employee(data)
    return jsonify({"message": "Employee created", "id": new_id}), 201

@app.route('/api/employees/<int:emp_id>', methods=['PUT'])
def update_employee(emp_id):
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid request data"}), 400

    existing_emp = employee_service.get_employee_by_id(emp_id)
    if not existing_emp:
        return jsonify({"message": "Employee not found"}), 404

    employee_service.update_employee(emp_id, data)
    return jsonify({"message": "Employee updated"}), 200

@app.route('/api/employees/<int:emp_id>', methods=['DELETE'])
def delete_employee(emp_id):
    existing_emp = employee_service.get_employee_by_id(emp_id)
    if not existing_emp:
        return jsonify({"message": "Employee not found"}), 404

    employee_service.delete_employee(emp_id)
    return jsonify({"message": "Employee deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)