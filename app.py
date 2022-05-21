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

    message = validate.login(data)
    if message != "OK":
        return {"msg": message}

    if not student.check_login(data["username"], data["password"]):
        return {"msg": "Incorrect username or password"}

    token = create_access_token(identity=data["username"])
    return {"msg": "Login success", "token": token}


#Get all students
@app.route('/', methods=['GET'])
@jwt_required()
def get():
    myresult = student.get_all()
    return json.dumps(myresult, ensure_ascii=False)


#Get a student by ID
@app.route('/<id>', methods=['GET'])
@jwt_required()
def get_one(id):
    if not validate.id(id):
        return {"msg": "Invalid id"}

    myresult = student.get_one(id)
    return json.dumps(myresult, ensure_ascii=False)

#Create a student
@app.route('/', methods=['POST'])
@jwt_required()
def post():
    data = request.json
    message = validate.student(data)
    if message != "OK":
        return {"msg": message}

    new_student_id = student.post(data)
    if new_student_id == 0 :
        return {"msg": "Failed to create new student"}

    new_log_id = log.post(get_jwt_identity(), "post", json.dumps(data, ensure_ascii=False), new_student_id, "student")
    if new_log_id == 0:
        return {"msg": "Failed to create log"}
        
    return {"msg": "Successfully created new student"}


#Update a student by ID and return 1 if success
@app.route('/<id>', methods=['PUT'])
@jwt_required()
def put(id):
    if not validate.id(id):
        return {"msg": "Invalid id"}

    data = request.json
    message = validate.student(data)
    if message != "OK":
        return {"msg": message}

    if not student.put(id, data):
        return {"msg": "Failed to update student"}

    if not log.post(get_jwt_identity(), "put", json.dumps(data, ensure_ascii=False), id, "student"):
        return {"msg": "Failed to create log"}

    return {"msg": "Successfully updated student"}

#Delete a student by ID and return 1 if success
@app.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    message =validate.id(id)
    if message != "OK":
        return {"msg": message}

    if not student.remove(id):
        return {"msg": "Failed to delete "}
    
    if not log.post(get_jwt_identity(), "delete", "", id, "student"):
        return {"msg": "Failed to create log"}

    return {"msg": "Successfully deleted"}



#Get all logs
@app.route('/logs', methods=['GET'])
@jwt_required()
def get_all_logs():
    myresult = log.get_all()
    return json.dumps(myresult, ensure_ascii=False, default=str)


if __name__ == "__main__":
    app.run(debug=True)