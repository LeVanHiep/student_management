from flask import Flask, request
from model import Job

# Wait worker done the job and return Redis string for result
# After that delete result string
def result(id):
    while Job.get_result(id) is None:
        pass
    result = Job.get_result(id)
    Job.delete_result(id)
    return result
app = Flask(__name__) 

#Get all students
@app.route('/', methods=['GET'])
def homepage():
    return 'Student management system'


#Get a student by ID
@app.route('/<id>', methods=['GET'])
def get_by_id(id):
    id = Job.create("Student","get_by_id", [id])
    return result(id)

#Find a student by username
@app.route('/find/username/<value>', methods=['GET'])
def get_by_username(value):
    id = Job.create("Student","get_by_username", [value])
    return result(id)

#Find students by name
@app.route('/find/name/<value>', methods=['GET'])
def get_by_name(value):
    id = Job.create("Student","get_by_name", [value])
    return result(id)

#Find students by age in range
@app.route('/find/age/<min_value>/<max_value>', methods=['GET'])
def get_by_age(min_value, max_value):
    id = Job.create("Student","get_by_age", [min_value, max_value])
    return result(id)


#Find students by a prize in their prize list
@app.route('/find/prize/<value>', methods=["GET"])
def get_by_prize(value):
    id = Job.create("Student","get_by_prize", [value])
    return result(id)


#Find students by birth address city
@app.route('/find/city/<value>', methods=["GET"])
def get_by_birthaddresscity(value):
    id = Job.create("Student","get_by_birthaddresscity", [value])
    return result(id)


#create a student and return its ID
@app.route('/', methods=['POST'])
def create():
    try:
        data = request.json
        id = Job.create("Student","create", [data])
        return result(id)
    except Exception as error_message:
        return {"data": [], "msg": str(error_message), "status": 0}


#Update a student's name by ID
@app.route('/<id>/<name>', methods=['PUT'])
def update_name_by_id(id,name):
    id = Job.create("Student","update_name_by_id", [id, name])
    return result(id)


#Delete a student by ID
@app.route('/<id>', methods=['DELETE'])
def delete_by_id(id):
    id = Job.create("Student","DeleteByID", [id])
    return result(id)

# create a message and send to a student at time
@app.route('/message', methods=['POST'])
def create_message():
    try:
        data = request.json
        id = Job.create("Message","create", [data], schedule=True)
        return {"data": [id], "msg": "success", "status": 1}

    except Exception as error_message:
        return {"data": [], "msg": str(error_message), "status": 0}


@app.route('/message/<id>', methods=['GET'])
def get_message(id):
    id = Job.create("Message","get_by_id", [id])
    return result(id)


if __name__ == "__main__":
    app.run(debug=True)