from redis import Redis
from json import dumps, loads

r = Redis(host="localhost", port=6379, db=0, decode_responses=True)

class Student:
    # Create a student (a hash for student data with id attribute linked to address hashes and prize list )
    def Create(data):
        try:
            if type(data) is str:
                data = loads(data)
            # Check if next-id key exist if not then create one an set its value to 1
            # next-id variable is used to set ID for object in Redis
            if not r.exists("next-id:student"):
                r.set("next-id:student", 1)
            if not r.exists("next-id:address"):
                r.set("next-id:address", 1)
            if not r.exists("next-id:prize"):
                r.set("next-id:prize", 1)

            # Separate address dict and prize list to another variable
            # because Redis hash cannot store complex dict contain list, dict, set inside
            permanent_address = data["permanent_address"]
            birth_address = data["birth_address"]
            prize = data["prize"]   #prize is a list so we cannot store id inside
            
            #Set ID to Student, Addresses and Prize in Student dict
            data["id"] = r.get("next-id:student")
            data["permanent_address"] = r.get("next-id:address")
            data["birth_address"] = str(int(data["permanent_address"]) + 1)
            data["prize"] = r.get("next-id:prize")

            #Set ID for address dict
            permanent_address["id"] = data["permanent_address"]
            birth_address["id"] = data["birth_address"]
            #prize stored in list so we cannot set id inside a list variable

            #inserted_id is used to store IDs of all variable which we created after success
            inserted_id = []
            with r.pipeline() as pipe:
                #Create Redis hash for student, addresses and prize info
                #its name format is "object-name:ID". ex: "student:5933"
                pipe.hmset("student:" + data["id"], data)
                pipe.hmset("address:" + permanent_address["id"], permanent_address)
                pipe.hmset("address:" + birth_address["id"], birth_address)
                pipe.sadd("prize:" + data["prize"], *prize)

                # Create Redis indexes for Student attribute
                # Its format name  is "object-name:attribute-name"
                # Its value will be {ID, ID, ID, ...}
                # Create a temp set to link all indexes with main student hash
                temp_name = "temp:student:" + data["id"]
                value = data["id"]

                # username index set and temp set
                key = "student:username-" + data["username"]
                pipe.set(key, value)
                pipe.sadd(temp_name, key)

                # name index set and temp set
                key = "student:name-" + data["name"]
                pipe.sadd(key, value)
                pipe.sadd(temp_name, key)

                # age index set and temp set
                key = "student:age-" + str(data["age"])
                pipe.sadd(key, value)
                pipe.sadd(temp_name, key)

                # birth_address-city index set and temp set
                key = "student:birth_address-city-" + birth_address["city"]
                pipe.sadd(key, value)
                pipe.sadd(temp_name, key)

                # prize index set and temp set
                for prize_name in prize:
                    key = "student:prize-" + prize_name
                    pipe.sadd(key, data["id"])
                    pipe.sadd(temp_name, key)

                # Increasing next-ids in Redis
                pipe.incr("next-id:student", 1)
                pipe.incr("next-id:address", 2)
                pipe.incr("next-id:prize", 1)
                inserted_id = pipe.execute()
                # r.bgsave()
            return {"data": [inserted_id[-1]-1], "msg": "Success", "status": 1}

        except Exception as error_message:
            return {"data": [], "msg": str(error_message), "status": 0}


    # Merge a student information from student hash, addresses hash and prize list
    def Merge(id):
        student = r.hgetall("student:" + id)
        if student: #if student dict is not empty (empty dict = False)
            student["permanent_address"] = r.hgetall("address:" + student["permanent_address"])
            student["birth_address"] = r.hgetall("address:" + student["birth_address"])
            student["prize"] = list(r.smembers("prize:" + student["prize"])) #set is not JSON serializable so we convert it to list
            return student
        
        else:
            return None
            

    # Get a student by ID
    def GetByID(id):
        try:
            student_data = Student.Merge(id)
            return {"data": [student_data], "msg": "Success", "status": 1}

        except Exception as error_message:
            return {"data": [], "msg": str(error_message), "status": 0}


    # Get a student by username
    def GetByUsername(username):
        try:
            student_id = r.get("student:username-" + username)
            if student_id is not None:
                student_data = Student.Merge(student_id)
                return {"data": [student_data], "msg": "Success", "status": 1}

            else:
                return {"data": [], "msg": "Success", "status": 1}

        except Exception as error_message:
            return {"data": [], "msg": str(error_message), "status": 0}


    # Get a student by name
    def GetByName(name):
        try:
            all_data = []
            id_set = r.smembers("student:name-" + name)
            for id in id_set:
                data = Student.Merge(id)
                all_data.append(data)

            return {"data": all_data, "msg": "Success", "status": 1}

        except Exception as error_message:
            return {"data": [], "msg": str(error_message), "status": 0}


    # Get students by age in range
    def GetByAge(data):
        # try:
            max_age = int(data[0])
            min_age = int(data[1])
            all_data = []
            for age in range(min_age, max_age + 1):
                id_set = r.smembers("student:age-" + str(age))
                for id in id_set:
                    data = Student.Merge(id)
                    all_data.append(data)

            return {"data": all_data, "msg": "Success", "status": 1}

        # except Exception as error_message:
        #     return {"data": [], "msg": str(error_message), "status": 0}


    # Get students by birth_address city
    def GetByBirthAddressCity(city):
        try:
            all_data = []
            id_set = r.smembers("student:birth_address-city-" + city)
            for id in id_set:
                data = Student.Merge(id)
                all_data.append(data)

            return {"data": all_data, "msg": "Success", "status": 1}

        except Exception as error_message:
            return {"data": [], "msg": str(error_message), "status": 0}


    # Get students by contain a prize
    def GetByPrize(prize):
        try:
            all_data = []
            id_set = r.smembers("student:prize-" + prize)
            for id in id_set:
                data = Student.Merge(id)
                all_data.append(data)

            return {"data": all_data, "msg": "Success", "status": 1}

        except Exception as error_message:
            return {"data": [], "msg": str(error_message), "status": 0}

    #Update a student's name by ID
    def UpdateNameByID(data):
        # try:
            id = data[1]
            new_name = data[0]
            with r.pipeline() as pipe:
                old_name = r.hget("student:" + id, "name")
                if old_name is None:
                    return {"data": [], "msg": "Student does not exist", "status": 0}
                else:
                    old_index_key = "student:name-" + old_name
                    pipe.srem(old_index_key, id)    # remove this student ID from old name index set
                    pipe.srem("temp:student:" + id, old_index_key)   # remove name key in temp set

                    pipe.hset("student:" + id, "name", new_name)    #update student name

                    new_index_key = "student:name-" + new_name
                    pipe.sadd(new_index_key, id)    # add this ID to new name index set
                    pipe.sadd("temp:student:" + id, new_index_key)   #add name key in temp set

                    result = pipe.execute()

            return {"data": [result[-1]], "msg": "Success", "status": 1}

        # except Exception as error_message:
        #     return {"data": [], "msg": str(error_message), "status": 0}

    # Delete a student by ID
    def DeleteByID(id):
        try:
            with r.pipeline() as pipe:
                index_set = r.smembers("temp:student:" + id)    #get all indexes in temp set
                for index in index_set: 
                    if r.type(index) == "set":
                        pipe.srem(index, id)   #remove this ID from all index set
                    else:   #string value
                        pipe.delete(index)
                
                pipe.delete("temp:student:" + id)  #remove temp set
                address_id = r.hget("student:" + id, "permanent_address")
                if address_id is None:
                    return {"data": [], "msg": "Student does not exist", "status": 0}
                pipe.delete("address:" + address_id)  # delete permanent_address hash
                pipe.delete("address:" + r.hget("student:" + id, "birth_address"))  # delete birth_address hash
                pipe.delete("prize:" + r.hget("student:" + id, "prize"))    # delete prize set
                pipe.delete("student:" + id)    #delete student hash

                result = pipe.execute()

            return {"data": [result[-1]], "msg": "Success", "status": 1}

        except Exception as error_message:
            return {"data": [], "msg": str(error_message), "status": 0}


class Message:
    # Create a message with data = {"id": "recieve_student_id", "data": "message_content", "send_time": "HH:MM dd/mm/yyyy"}
    def Create(data):
        try:
            data = loads(data)
            if r.exists("student:" + data["id"]):
                result = r.lpush("message:" + data["id"], data["message"])
                return {"data": [result], "msg": "Success", "status": 1}
                
            else:
                return {"data": [], "msg": "Student does not exist", "status": 1}
                
        except Exception as error_message:
            return {"data": [], "msg": str(error_message), "status": 0}

    # Get message list of student with ID
    def GetByID(id):
        try:
            message_list = list(r.lrange("message:" + id, 0, -1))
            return {"data": message_list, "msg": "Success", "status": 1}

        except Exception as error_message:
            return {"data": [], "msg": str(error_message), "status": 0}


class Job:
    def Create(object, method, args):
        id = "1"
        if not r.exists("next-id:job"):
            r.set("next-id:job", 1)
        else:
            id = r.get("next-id:job")

        r.hset("job:" + id, "object", object)
        r.hset("job:" + id, "method", method)
        for arg in args:
            if type(arg) is not str:
                arg = dumps(arg, ensure_ascii=False).encode('utf8')    # covert arg to string with encode utf 8
            
            r.lpush("job:" + id + ":arg", arg)
        
        r.incr("next-id:job")
        r.sadd("job:queue", id)

        return id


    def DeleteByID(id):
        r.srem("job:queue", id)
        r.delete("job:" + id)
        r.delete("job:" + id + ":arg")
        return 1

    def Exist():
        return r.exists("job:queue")

    def GetAllID():
        return r.smembers("job:queue")

    def GetByID(id):
        job = r.hgetall("job:" + id)
        job_args = r.lrange("job:" + id + ":arg", 0, -1)
        job["args"] = job_args
        return job

    def CreateResult(id, result):
        r.set("job: " + id + ":result", result)
        r.expire("job: " + id + ":result", 300)
        return 1
    
    def GetResult(id):
        return r.get("job: " + id + ":result")

    def DeleteResult(id):
        return r.delete("job: " + id + ":result")

data = {
        "username" : "ha",
        "password" : "12345678",
        "name" : "Lê Văn Hảo",
        "gender" : "nam",
        "grade" : "DHKTPM01",
        "school_year" : 13,
        "age" : 22,
        "permanent_address":
        {
            "unit" : "12/1A",
            "street" : "Đình Thôn",
            "ward": "Mỹ Đình",
            "district" : "Nam Từ Liêm",
            "city" : "Hà Nội",
            "country" : "Việt Nam"
        },
        "birth_address" :
        {
            "unit" : "123/1A",
            "street" : "Đình Thôn",
            "ward": "Mỹ Đình",
            "district" : "Nam Từ Liêm",
            "city" : "Hà Nội",
            "country" : "Thanh Hóa"
        },
        "prize" :
        [
            "Giải nhất cuộc thi AI Tank - IT Festival",
            "Giải nhất cuộc thi ABC"
        ]
    }
# print(Job.Create("Student", "Create", [data]))
# print(Job.Create("Student", "Create", [data]))
# print(Job.Create("Student", "Create", [data]))
# print(Job.Create("Student", "Create", [data]))
# print(Job.DeleteByID("3"))
# print(Job.GetResult("8"))