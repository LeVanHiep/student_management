from flask import Flask, request
from model import q, Student, Message
from datetime import datetime, timedelta

app = Flask(__name__) 

#Get all students
@app.route('/', methods=['GET'])
def homepage():
    return 'Student management system'


#Get a student by ID
@app.route('/<id>', methods=['GET'])
def GetByID(id):
    a = q.enqueue(Student.GetByID, id)
    while a.result is None:
        pass
    return str(a.result)

#Find a student by username
@app.route('/find/username/<value>', methods=['GET'])
def GetByUsername(value):
    a = q.enqueue(Student.GetByUsername, value)
    while a.result is None:
        pass
    return str(a.result)

#Find students by name
@app.route('/find/name/<value>', methods=['GET'])
def GetByName(value):
    a = q.enqueue(Student.GetByName, value)
    while a.result is None:
        pass
    return str(a.result)

#Find students by age in range
@app.route('/find/age/<int:min_value>/<int:max_value>', methods=['GET'])
def GetByAge(min_value, max_value):
    a = q.enqueue(Student.GetByAge, min_value, max_value)
    while a.result is None:
        pass
    return str(a.result)


#Find students by a prize in their prize list
@app.route('/find/prize/<value>', methods=["GET"])
def GetByPrize(value):
    a = q.enqueue(Student.GetByPrize, value)
    while a.result is None:
        pass
    return str(a.result)


#Find students by birth address city
@app.route('/find/city/<value>', methods=["GET"])
def GetByBirthAddressCity(value):
    a = q.enqueue(Student.GetByBirthAddressCity, value)
    while a.result is None:
        pass
    return str(a.result)


#Create a student and return its ID
@app.route('/', methods=['POST'])
def Create():
    try:
        data = request.json
        a = q.enqueue(Student.Create, data)
        while a.result is None:
            pass
        return str(a.result)
    except Exception as error_message:
        return {"data": [], "msg": str(error_message), "status": 0}


#Update a student's name by ID
@app.route('/<id>/<name>', methods=['PUT'])
def UpdateNameByID(id,name):
    a = q.enqueue(Student.UpdateNameByID, id, name)
    while a.result is None:
        pass
    return str(a.result)


#Delete a student by ID
@app.route('/<id>', methods=['DELETE'])
def delete(id):
    a = q.enqueue(Student.DeleteByID, id)
    while a.result is None:
        pass
    return str(a.result)

@app.route('/message', methods=['POST'])
def create_message():
    try:
        data = request.json
        if "send_time" in data:
            a = q.enqueue_at(datetime.strptime(data["send_time"], "%H:%M %d/%m/%Y"), Message.Create, data)
            print(str(a))
        else:
            a = q.enqueue(Message.Create, data)
        return {"data": [str(a.id)], "msg": "Success", "status": 1}
    except Exception as error_message:
        return {"data": [], "msg": str(error_message), "status": 0}


@app.route('/message/<id>', methods=['GET'])
def get_message(id):
    a = q.enqueue(Message.GetByID, id)
    while a.result is None:
        pass
    return str(a.result)


if __name__ == "__main__":
    app.run(debug=True)