from flask import Flask, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token , get_jwt_identity
import json
import validate
from model import student, log

app = Flask(__name__)  
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "chuoisieubimat"



#Login
@app.route('/login', methods=['GET'])
def login_page():
    return "Login page"

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    return student.login(data)


#Get all students
@app.route('/', methods=['GET'])
@jwt_required()
def get():
    return student.get_all()


#Get a student by ID
@app.route('/<id>', methods=['GET'])
@jwt_required()
def get_one(id):
    return student.get_one(id)

#Create a student
@app.route('/', methods=['POST'])
@jwt_required()
def post():
    data = request.json
    result = student.post(data)
    if result["status"] == 1:
        return log.post(get_jwt_identity(), "post", json.dumps(data, ensure_ascii=False), result["data"][0], "student")

    return result


#Update a student by ID and return 1 if success
@app.route('/<id>', methods=['PUT'])
@jwt_required()
def put(id):
    data = request.json
    result = student.put(id, data)
    if result["status"] == 1:
        return log.post(get_jwt_identity(), "put", json.dumps(data, ensure_ascii=False), id, "student")

    return result

#Delete a student by ID and return 1 if success
@app.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    result = student.remove(id)
    if result["status"] == 1:
        return log.post(get_jwt_identity(), "delete", "", id, "student")

    return result


#Get all logs
@app.route('/logs', methods=['GET'])
@jwt_required()
def get_all_logs():
    return log.get_all()


if __name__ == "__main__":
    app.run(debug=True)