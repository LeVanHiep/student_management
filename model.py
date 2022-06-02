from redis_om import Field, Migrator, JsonModel
from typing import List

class Address(JsonModel):
    unit : str = Field(index=True)
    street : str = Field(index=True)
    ward : str = Field(index=True)
    district : str = Field(index=True)
    city : str = Field(index=True)
    country : str = Field(index=True)


class Student(JsonModel):
    username : str = Field(index=True)  #set index to search with this attribute
    password : str
    name : str = Field(index=True, full_text_search=True)
    gender : str = Field(index=True)
    grade : str = Field(index=True)
    school_year : int = Field(index=True)
    age : int = Field(index=True)
    permanent_address : Address
    birthplace : Address
    prize: List[str] = Field(index=True)

# Before running queries, we need to run migrations to set up the
# indexes that Redis OM will use. You can also use the `migrate`
# CLI tool for this!
Migrator().run()

#print(Student.get("01G42BX3BDBY4SPSS1A8GC8RC8"))
# print("Success create a new student with id ", a.pk)

# print("save model to redis")


# Expire the model after 2 mins (120 seconds)
#a.expire(120)

# retrieve this student with its primary key:
# try:
#      print(Student.get('01G41Y2W7ZPCPJWWM8587J3SC0'))
# except Exception as e:
#     print(e)
# print("people: ")
# people = Student.find().all()
# for i in people:
#     print(i)

