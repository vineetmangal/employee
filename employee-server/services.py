from models import Employee

class EmployeeService:
    def __init__(self, db):
        self.db = db

    def get_all_employees(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM employees ORDER BY id")
        rows = cursor.fetchall()
        employees = []
        for row in rows:
            employees.append(Employee(
                id=row["id"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                email=row["email"],
                department=row["department"],
                hire_date=str(row["hire_date"]) if row["hire_date"] else None
            ))
        return employees

    def get_employee_by_id(self, emp_id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM employees WHERE id = %s", (emp_id,))
        row = cursor.fetchone()
        if row:
            return Employee(
                id=row["id"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                email=row["email"],
                department=row["department"],
                hire_date=str(row["hire_date"]) if row["hire_date"] else None
            )
        return None

    def create_employee(self, emp_data):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO employees (first_name, last_name, email, department, hire_date)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            emp_data['first_name'],
            emp_data['last_name'],
            emp_data['email'],
            emp_data['department'],
            emp_data['hire_date'] or None
        ))
        conn.commit()
        return cursor.lastrowid

    def update_employee(self, emp_id, emp_data):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        sql = """
            UPDATE employees
            SET first_name = %s, last_name = %s, email = %s, department = %s, hire_date = %s
            WHERE id = %s
        """
        cursor.execute(sql, (
            emp_data['first_name'],
            emp_data['last_name'],
            emp_data['email'],
            emp_data['department'],
            emp_data['hire_date'] or None,
            emp_id
        ))
        conn.commit()

    def delete_employee(self, emp_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id = %s", (emp_id,))
        conn.commit()