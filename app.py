from sqlalchemy import Column, Integer, String
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qwerty@localhost/postgres'
db = SQLAlchemy(app)

class Defects(db.Model):
    __tablename__ = 'defects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(20), nullable=False)
    defect = Column(String(20), nullable=False)
    works_name = Column(String(20), nullable=False)
    unit = Column(String(20), nullable=False)
    number = Column(Integer, nullable=False)

    def json(self):
        return {
            'id': self.id,
            'code': self.code,
            'defect': self.defect,
            'works_name': self.works_name,
            'unit': self.unit,
            'number': self.number
        }

class Employees(db.Model):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee = Column(Integer, nullable=False)
    lastname = Column(String(30), nullable=False)
    firstname = Column(String(30), nullable=False)
    patronymic = Column(String(30))
    sent_sheets_num = Column(Integer, nullable=False)

    def json(self):
        return {
            'id': self.id,
            'employee': self.employee,
            'lastname': self.lastname,
            'firstname': self.firstname,
            'patronymic': self.patronymic,
            'sent_sheets_num': self.sent_sheets_num
        }


with app.app_context():
    db.create_all()
    with app.app_context():

        defect1 = Defects(code='А001', defect='Трещина', works_name='Стройка', unit='метр', number=5)
        defect2 = Defects(code='Б002', defect='Утечка', works_name='Сантехника', unit='куб.м', number=3)

        employee1 = Employees(employee=876589, lastname='Иванов', firstname='Иван', patronymic='Иванович',
                              sent_sheets_num=100)
        employee2 = Employees(employee=987654, lastname='Петров', firstname='Петр', patronymic='Петрович',
                              sent_sheets_num=150)

        db.session.add(defect1)
        db.session.add(defect2)
        db.session.add(employee1)
        db.session.add(employee2)
        db.session.commit()

# тест для проверки работы сервера
@app.route('/test', methods=['GET'])
def test():
    return make_response(jsonify({'message': 'test route'}), 200)

# CRUD для дефектов
@app.route('/defects', methods=['GET'])
def get_defects():
    try:
        defects = Defects.query.all()
        return make_response(jsonify([defect.json() for defect in defects]), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error while getting defects', 'error': str(e)}), 500)

@app.route('/defects/<int:id>', methods=['GET'])
def get_defect(id):
    try:
        defect = Defects.query.filter_by(id=id).first()
        if defect:
            return make_response(jsonify({'defect': defect.json()}), 200)
        return make_response(jsonify({'message': 'defect not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error while getting defect', 'error': str(e)}), 500)

@app.route('/defects', methods=['POST'])
def add_defect():
    try:
        data = request.get_json()
        new_defect = Defects(
            code=data.get('code', ''),
            defect=data.get('defect', ''),
            works_name=data.get('works_name', ''),
            unit=data.get('unit', ''),
            number=data.get('number', 0)
        )
        db.session.add(new_defect)
        db.session.commit()
        return make_response(jsonify({'message': 'defect created'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'error while creating defect', 'error': str(e)}), 500)

@app.route('/defects/<int:id>', methods=['PUT'])
def update_defect(id):
    try:
        defect = Defects.query.filter_by(id=id).first()
        if defect:
            data = request.get_json()
            defect.code = data.get('code', defect.code)
            defect.defect = data.get('defect', defect.defect)
            defect.works_name = data.get('works_name', defect.works_name)
            defect.unit = data.get('unit', defect.unit)
            defect.number = data.get('number', defect.number)
            db.session.commit()
            return make_response(jsonify({'message': 'defect updated'}), 200)
        return make_response(jsonify({'message': 'defect not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error while updating defect', 'error': str(e)}), 500)

@app.route('/defects/<int:id>', methods=['DELETE'])
def delete_defect(id):
    try:
        defect = Defects.query.filter_by(id=id).first()
        if defect:
            db.session.delete(defect)
            db.session.commit()
            return make_response(jsonify({'message': 'defect deleted'}), 200)
        return make_response(jsonify({'message': 'defect not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error while deleting defect', 'error': str(e)}), 500)

# CRUD для сотрудников
@app.route('/employees', methods=['GET'])
def get_employees():
    try:
        employees = Employees.query.all()
        return make_response(jsonify([employee.json() for employee in employees]), 200)
    except Exception as e:
        return make_response(jsonify({'message': 'error while getting employees', 'error': str(e)}), 500)

@app.route('/employees/<int:id>', methods=['GET'])
def get_employee(id):
    try:
        employee = Employees.query.filter_by(id=id).first()
        if employee:
            return make_response(jsonify({'employee': employee.json()}), 200)
        return make_response(jsonify({'message': 'employee not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error while getting employee', 'error': str(e)}), 500)

@app.route('/employees', methods=['POST'])
def add_employee():
    try:
        data = request.get_json()
        new_employee = Employees(
            employee=data.get('employee', 0),
            lastname=data.get('lastname', ''),
            firstname=data.get('firstname', ''),
            patronymic=data.get('patronymic', ''),
            sent_sheets_num=data.get('sent_sheets_num', 0)
        )
        db.session.add(new_employee)
        db.session.commit()
        return make_response(jsonify({'message': 'employee created'}), 201)
    except Exception as e:
        return make_response(jsonify({'message': 'error while creating employee', 'error': str(e)}), 500)

@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    try:
        employee = Employees.query.filter_by(id=id).first()
        if employee:
            data = request.get_json()
            employee.employee = data.get('employee', employee.employee)
            employee.lastname = data.get('lastname', employee.lastname)
            employee.firstname = data.get('firstname', employee.firstname)
            employee.patronymic = data.get('patronymic', employee.patronymic)
            employee.sent_sheets_num = data.get('sent_sheets_num', employee.sent_sheets_num)
            db.session.commit()
            return make_response(jsonify({'message': 'employee updated'}), 200)
        return make_response(jsonify({'message': 'employee not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error while updating employee', 'error': str(e)}), 500)

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    try:
        employee = Employees.query.filter_by(id=id).first()
        if employee:
            db.session.delete(employee)
            db.session.commit()
            return make_response(jsonify({'message': 'employee deleted'}), 200)
        return make_response(jsonify({'message': 'employee not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'message': 'error while deleting employee', 'error': str(e)}), 500)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
