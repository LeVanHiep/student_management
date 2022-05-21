from select import select
from peewee import *
from datetime import datetime

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

    def check_login(_username,_password):
        try:
            student.get( (student.id == _username) & (student.password == _password) ).id
            return True
        except DoesNotExist:
            return False

    def get_all():
        return list(student.select().dicts())

    def get_one(_id):
        result = student.select().where(student.id == _id).dicts()
        if len(result) == 0:
            return None
        else:
            return result[0]

    #Create a new student. Return student id if success
    def post(data):
        try:
            new_student_id = student.create(password = data["password"], 
                                            name = data["name"], 
                                            age = data["age"], 
                                            gender = data["gender"], 
                                            grade = data["grade"], 
                                            school_year = data["school_year"])
          
        except:
            return 0
        return new_student_id

    def put(id,data):
        try:
            query = student.update(password = data["password"], 
                                    name = data["name"], 
                                    age = data["age"], 
                                    gender = data["gender"], 
                                    grade = data["grade"], 
                                    school_year = data["school_year"]
                                ).where(student.id == id).execute()
            if query == 0:
                return False
                
        except:
            return False
        return True

    def remove(_id):
        try:
            student.get(student.id == _id).delete_instance()
        except:
            return False
        
        return True



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
        return list(log.select().dicts())


    def post(_actor, _action, _detail, _subject, _table):
        try:
            new_log_id = log.create(actor = _actor, action = _action, detail = _detail, subject = _subject, table = _table, time = datetime.now())
                
        except:
            return 0
        return new_log_id


# database.connect()
# print(student.remove(20))
# for i in student.select().dicts():
#     print(i)
