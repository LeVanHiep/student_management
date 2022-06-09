from flask import Flask, request
from model import Student

app = Flask(__name__) 

def build_results(data):
    response = []
    for i in data:
        response.append(i.dict())

    return { "results": response }

#Get all students
@app.route('/', methods=['GET'])
def homepage():
    return "Homepage"


#Get a student by ID
@app.route('/<id>', methods=['GET'])
def GetByID(id):
    return Student.GetByID(id)

#Find a student by username
@app.route('/find/username/<value>', methods=['GET'])
def GetByUsername(value):
    return Student.GetByUsername(value)

#Find students by name
@app.route('/find/name/<value>', methods=['GET'])
def GetByName(value):
    return Student.GetByName(value)

#Find students by age in range 
@app.route('/find/age/<int:min_value>/<int:max_value>', methods=['GET'])
def GetByAge(min_value, max_value):
    return Student.GetByAge(min_value, max_value)


#Find students by a prize in their prize list
@app.route('/find/prize/<value>', methods=["GET"])
def GetByPrize(value):
    return Student.GetByPrize(value)


#Find students by birth address city
@app.route('/find/city/<value>', methods=["GET"])
def GetByBirthAddressCity(value):
    return Student.GetByBirthAddressCity(value)


#Create a student and return its ID
@app.route('/', methods=['POST'])
def Create():
    try:
        data = request.json
        return Student.Create(data)
    except Exception as error_message:
        return {"data": [], "msg": str(error_message), "status": 0}


#Update a student's name by ID
@app.route('/<id>/<name>', methods=['PUT'])
def UpdateNameByID(id,name):
    return Student.UpdateNameByID(id, name)


#Delete a student by ID
@app.route('/<id>', methods=['DELETE'])
def delete(id):
    return Student.DeleteByID(id)


if __name__ == "__main__":
    app.run(debug=True)