from flask import Flask, request
from model import Student
from redis_om.model import NotFoundError
from pydantic import ValidationError

app = Flask(__name__) 

def build_results(data):
    response = []
    for i in data:
        response.append(i.dict())

    return { "results": response }

#Get all students
@app.route('/', methods=['GET'])
def get_all():
    try:
        students = Student.find()
        return {"msg": "Success", "status": 1, "data": build_results(students)}
    except NotFoundError: #NotFoundError did not return anything
        return {"msg":  "NotFoundError", "status": 0, "data": []}


#Get a student by ID
@app.route('/<id>', methods=['GET'])
def get_one(id):
    try:
        person = Student.get(id)
        return {"msg": "Success", "status": 1, "data": [person.dict()]}
    except NotFoundError: #NotFoundError did not return anything
        return {"msg":  "NotFoundError", "status": 0, "data": []}

#Find students by exact username
@app.route('/find/username/<value>', methods=['GET'])
def find_username(value):
    try:
        students = Student.find(Student.username == value)
        return {"msg": "Success", "status": 1, "data": build_results(students)}
    except (Exception, NotFoundError, ValidationError) as error_message:
        if len(str(error_message)) == 0:  #NotFoundError did not return anything
            return {"msg": "NotFoundError", "status": 0, "data": []}
        else:
            return {"msg": str(error_message), "status": 0, "data": []}

#Find students by name (full-text search)
@app.route('/find/name/<value>', methods=['GET'])
def find_name(value):
    try:
        students = Student.find(Student.name % value)
        return {"msg": "Success", "status": 1, "data": build_results(students)}
    except (Exception, NotFoundError, ValidationError) as error_message:
        if len(str(error_message)) == 0:  #NotFoundError did not return anything
            return {"msg": "NotFoundError", "status": 0, "data": []}
        else:
            return {"msg": str(error_message), "status": 0, "data": []}

#Find students by age in range 
@app.route('/find/age/<int:min_value>/<int:max_value>', methods=['GET'])
def find_age(min_value, max_value):
    try:
        students = Student.find((Student.age >= min_value) & (Student.age <= max_value))
        return {"msg": "Success", "status": 1, "data": build_results(students)}
    except (Exception, NotFoundError, ValidationError) as error_message:
        if len(str(error_message)) == 0:  #NotFoundError did not return anything
            return {"msg": "NotFoundError", "status": 0, "data": []}
        else:
            return {"msg": str(error_message), "status": 0, "data": []}


#Find students by a prize in their prize list
@app.route('/find/prize/<value>', methods=["GET"])
def find_prize(value):
    try:
        students = Student.find(Student.prize << value)
        return {"msg": "Success", "status": 1, "data": build_results(students)}
    except (Exception, NotFoundError, ValidationError) as error_message:
        if len(str(error_message)) == 0:  #NotFoundError did not return anything
            return {"msg": "NotFoundError", "status": 0, "data": []}
        else:
            return {"msg": str(error_message), "status": 0, "data": []}


#Find students by birthplace city
@app.route('/find/city/<value>', methods=["GET"])
def find_city(value):
    try:
        students = Student.find(Student.birthplace.city == value)
        return {"msg": "Success", "status": 1, "data": build_results(students)}
    except (Exception, NotFoundError, ValidationError) as error_message:
        if len(str(error_message)) == 0:  #NotFoundError did not return anything
            return {"msg": "NotFoundError", "status": 0, "data": []}
        else:
            return {"msg": str(error_message), "status": 0, "data": []}


#Create a student and return its ID
@app.route('/', methods=['POST'])
def post():
    try:
        new_person = Student(**request.json)
        new_person.save()
        return {"msg": "Success", "status": 1, "data": [new_person.pk]}
    except (Exception, ValidationError) as error_message:
        return {"msg":  str(error_message), "status": 0, "data": []}


#Update a student by ID
@app.route('/<id>', methods=['PUT'])
def put(id):
    try:
        student = Student.get(id)
        changes = request.json
        print(changes)
        for key, value in changes.items():
            setattr(student, key, value)
        student.save()
        return {"msg": "Success", "status": 1, "data": []}
    except (Exception, NotFoundError, ValidationError) as error_message:
        if len(str(error_message)) == 0:  #NotFoundError did not return anything
            return {"msg": "NotFoundError", "status": 0, "data": []}
        else:
            return {"msg": str(error_message), "status": 0, "data": []}


#Delete a student by ID
@app.route('/<id>', methods=['DELETE'])
def delete(id):
    try:
        result = Student.delete(id)
        if result == 1:
            return {"msg": "Success", "status": 1, "data": []}
        else:
            return {"msg": "NotFoundError", "status": 0, "data": []}

    except Exception as error_message:
        return {"msg": str(error_message), "status": 0, "data": []}


if __name__ == "__main__":
    app.run(debug=True)