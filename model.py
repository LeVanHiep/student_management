from redis_om import HashModel, Field, Migrator, JsonModel

class Student(HashModel):
    username : str = Field(index=True)  #set index to search with this attribute
    password : str
    name : str
    gender : str
    grade : str
    school_year : int
    age : int

# Before running queries, we need to run migrations to set up the
# indexes that Redis OM will use. You can also use the `migrate`
# CLI tool for this!
Migrator().run()

#print(Student.get("01G42BX3BDBY4SPSS1A8GC8RC8"))

# print("add a student to database")
# a = Student(username= "1", password = "1", name = "1", gender = "1", grade = "1", school_year = 1, age = 1)
# a = Student(username= "3", password = "1", name = "1", gender = "1", grade = "1", school_year = 1, age = 1)
# a = Student(username= "4", password = "1", name = "1", gender = "1", grade = "1", school_year = 1, age = 1)
# a = Student(username= "5", password = "1", name = "1", gender = "1", grade = "1", school_year = 1, age = 1)
# a = Student(username= "6", password = "1", name = "1", gender = "1", grade = "1", school_year = 1, age = 1)

# print("Success create a new student with id ", a.pk)

# print("save model to redis")
# a.save()

# Expire the model after 2 mins (120 seconds)
#a.expire(120)

# retrieve this student with its primary key:
# try:
#      print(Student.get('01G41Y2W7ZPCPJWWM8587J3SC0'))
# except Exception as e:
#     print(e)
# print(Student.find(Student.password != "1"  ).all())

