from peewee import *
from datetime import datetime
from flask_jwt_extended import create_access_token
from validate import is_validate

database = MySQLDatabase('school', host='localhost',
                   user='hiep', password='12345678')

class student(Model):
    id = AutoField(primary_key=True)
    password = TextField()
    name = TextField()
    age = IntegerField()
    gender = TextField()
    grade = TextField()
    school_year = IntegerField()

    class Meta:
        database = database
        db_table = 'student'

    #Login using id and password. return token if user matches
    def login(data):
        login_form = {  "username": "str",
                        "password": "str"}
        #Validate username and password
        validate_message = is_validate(login_form,data)
        if validate_message != "OK":
            return {"msg": validate_message, "status": 0, "data": []}
        #Check if username and password exist in database
        try:
            student.get( (student.id == data["username"]) & (student.password == data["password"]) ).id
        except Exception as error_message:
            return {"msg": str(error_message), "status": 0, "data": []}
        #Create JWT token to access APIs
        try:
            token = create_access_token(identity=data["username"])
        except Exception as error_message:
            return {"msg": str(error_message), "status": 0, "data": []}

        return {"msg": "Success", "status": 1, "data": [token]}

    #Get all students in database
    def get_all():
        try:
            data = list(student.select().dicts())
        except Exception as error_message:
            return {"msg": str(error_message), "status": 0, "data": []}

        return {"msg": "Success", "status": 1, "data": data}

    #Get a student by ID
    def get_one(id):
        #Validate input ID
        if not str.isdigit(id):
            return {"msg": "Incorrect ID", "status": 0, "data": []}
        #Get that student by ID
        try:
            data = student.select().where(student.id == id).dicts()
        except Exception as error_message:
            return {"msg": str(error_message), "status": 0, "data": []}
        #Check if that student exists
        if len(data) == 0:
            return {"msg": "No such student", "status": 1, "data": []}
        
        return {"msg": "Success", "status": 1, "data": [data[0]]}

    #Create a new student. Return student id if success
    def post(data):
        create_form = { "password": "str",
                        "name": "str",
                        "age": "int",
                        "gender": "str",
                        "grade": "str",
                        "school_year": "int"}
        #Validate input
        validate_message = is_validate(create_form, data)
        if validate_message != "OK":
            return {"msg": validate_message, "status": 0, "data": []}
        #Create a new student in database
        try:
            new_student_id = student.create(password = data["password"], 
                                            name = data["name"], 
                                            age = data["age"], 
                                            gender = data["gender"], 
                                            grade = data["grade"], 
                                            school_year = data["school_year"])
          
        except Exception as error_message:
            return {"msg": str(error_message), "status": 0, "data": []}

        return {"msg": "Success", "status": 1, "data": [new_student_id]}

    def put(id,data):
        #Validate input ID
        if not str.isdigit(id):
            return {"msg": "Incorrect ID", "status": 0, "data": []}
        
        #Validate input
        update_form = { "password": "str",
                        "name": "str",
                        "age": "int",
                        "gender": "str",
                        "grade": "str",
                        "school_year": "int"}
        validate_message = is_validate(update_form, data)
        if validate_message != "OK":
            return {"msg": validate_message, "status": 0, "data": []}
        
        #Update student in database
        try:
            query = student.update(password = data["password"], 
                                    name = data["name"], 
                                    age = data["age"], 
                                    gender = data["gender"], 
                                    grade = data["grade"], 
                                    school_year = data["school_year"]
                                ).where(student.id == id).execute() 
        except Exception as error_message:
            return {"msg": str(error_message), "status": 0, "data": []}

        #Check if student updated
        if query == 0:  #Nothing happen
            return {"msg": "Failed to update", "status": 0, "data": []}
        
        return {"msg": "Success", "status": 1, "data": []}

    def remove(id):
        #Validate input ID
        if not str.isdigit(id):
            return {"msg": "Incorrect ID", "status": 0, "data": []}

        #Delete student from database
        try:
            student.get(student.id == id).delete_instance()
        except Exception as error_message:
            return {"msg": str(error_message), "status": 0, "data": []}

        return {"msg": "Success", "status": 1, "data": []}



class log(Model):
    id = AutoField(primary_key=True)
    actor = IntegerField()
    action = TextField()
    detail = TextField()
    subject = IntegerField()
    table = TextField()
    time = DateTimeField()

    class Meta:
        database = database
        db_table = 'log'

    def get_all():
        try:
            data = list(log.select().dicts())
        except Exception as error_message:
            return {"msg": str(error_message), "status": 0, "data": []}

        return {"msg": "Success", "status": 1, "data": data}


    def post(_actor, _action, _detail, _subject, _table):
        try:
            new_log_id = log.create(actor = _actor, action = _action, detail = _detail, subject = _subject, table = _table, time = datetime.now())
        except Exception as error_message:
            return {"msg": str(error_message), "status": 0, "data": []}

        return {"msg": "Success", "status": 1, "data": []}


# database.connect()
# print(student.remove(20))
# for i in student.select().dicts():
#     print(i)
