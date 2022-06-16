from flask import Flask, request
from model import Student, Message, Job

# Wait worker done the job and return Redis string for result
# After that delete result string
def Result(id):
    while Job.GetResult(id) is None:
        pass
    result = Job.GetResult(id)
    Job.DeleteResult(id)
    return result
app = Flask(__name__) 

#Get all students
@app.route('/', methods=['GET'])
def homepage():
    return 'Student management system'


#Get a student by ID
@app.route('/<id>', methods=['GET'])
def GetByID(id):
    id = Job.Create("Student","GetByID", [id])
    return Result(id)

#Find a student by username
@app.route('/find/username/<value>', methods=['GET'])
def GetByUsername(value):
    id = Job.Create("Student","GetByUsername", [value])
    return Result(id)

#Find students by name
@app.route('/find/name/<value>', methods=['GET'])
def GetByName(value):
    id = Job.Create("Student","GetByName", [value])
    return Result(id)

#Find students by age in range
@app.route('/find/age/<min_value>/<max_value>', methods=['GET'])
def GetByAge(min_value, max_value):
    id = Job.Create("Student","GetByAge", [min_value, max_value])
    return Result(id)


#Find students by a prize in their prize list
@app.route('/find/prize/<value>', methods=["GET"])
def GetByPrize(value):
    id = Job.Create("Student","GetByPrize", [value])
    return Result(id)


#Find students by birth address city
@app.route('/find/city/<value>', methods=["GET"])
def GetByBirthAddressCity(value):
    id = Job.Create("Student","GetByBirthAddressCity", [value])
    return Result(id)


#Create a student and return its ID
@app.route('/', methods=['POST'])
def Create():
    try:
        data = request.json
        id = Job.Create("Student","Create", [data])
        return Result(id)
    except Exception as error_message:
        return {"data": [], "msg": str(error_message), "status": 0}


#Update a student's name by ID
@app.route('/<id>/<name>', methods=['PUT'])
def UpdateNameByID(id,name):
    id = Job.Create("Student","UpdateNameByID", [id, name])
    return Result(id)


#Delete a student by ID
@app.route('/<id>', methods=['DELETE'])
def delete(id):
    id = Job.Create("Student","DeleteByID", [id])
    return Result(id)

# Create a message and send to a student at time
@app.route('/message', methods=['POST'])
def create_message():
    try:
        data = request.json
        id = Job.Create("Message","Create", [data])
        return {"data": [id], "msg": "success", "status": 1}

    except Exception as error_message:
        return {"data": [], "msg": str(error_message), "status": 0}


@app.route('/message/<id>', methods=['GET'])
def get_message(id):
    id = Job.Create("Message","GetByID", [id])
    return Result(id)


if __name__ == "__main__":
    app.run(debug=True)