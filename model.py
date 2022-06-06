import redis

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

class Student:
    # Create a student (a hash for student data with id attribute linked to address hashes and prize list )
    def Create(data):
        try:
            # Check if next-id key exist if not then create one an set its value to 1
            # next-id variable is used to set ID for object in Redis
            if not r.exists("next-id:student"):
                r.set("next-id:student",1)
            if not r.exists("next-id:address"):
                r.set("next-id:address",1)
            if not r.exists("next-id:prize"):
                r.set("next-id:prize",1)

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
                pipe.hmset("student:"+data["id"], data)
                pipe.hmset("address:"+permanent_address["id"], permanent_address)
                pipe.hmset("address:"+birth_address["id"], birth_address)
                pipe.lpush("prize:"+data["prize"], *prize)

                # Create Redis list for indexing Student attribute
                # Its name format is "object-name:attribute-name"
                # Its value will be [ID, ID, ID, ...]
                pipe.set("student:username-" + data["username"], data["id"])
                pipe.lpush("student:name-" + data["name"], data["id"])
                pipe.lpush("student:age-" + str(data["age"]), data["id"])
                pipe.lpush("student:birth_address-city-" + birth_address["city"], data["id"])
                for prize_name in prize:
                    pipe.lpush("student:prize-" + prize_name, data["id"]) # ERROR: tao vong for index cho tung giai thuong mot

                #Increasing next-ids in Redis
                pipe.incr("next-id:student", 1)
                pipe.incr("next-id:address", 2)
                pipe.incr("next-id:prize", 1)
                inserted_id = pipe.execute()
                #r.bgsave()
            return {"data": [inserted_id[-1]], "msg": "Success", "status": 1}

        except Exception as error_message:
            return {"data": [], "msg": str(error_message), "status": 0}


    # Merge a student information from student hash, addresses hash and prize list
    def Merge(id):
        student = r.hgetall("student:" + id)
        if student: #if student dict is not empty (empty dict = False)
            student["permanent_address"] = r.hgetall("address:" + student["permanent_address"])
            student["birth_address"] = r.hgetall("address:" + student["birth_address"])

            prize_id = student["prize"]
            student["prize"] = []
            prize_list_len = r.llen("prize:" + prize_id)
            for i in range(prize_list_len):
                student["prize"].append(r.lindex("prize:" + prize_id, i))
                print("prize: ", i)
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
            list_size = r.llen("student:name-" + name)
            for i in range(list_size):  # student:name-abc [id, id, id , ...]
                student_id = r.lindex("student:name-" + name, i)
                student_data = Student.Merge(student_id)
                all_data.append(student_data)

            return {"data": all_data, "msg": "Success", "status": 1}

        except Exception as error_message:
            return {"data": [], "msg": str(error_message), "status": 0}


    # Get students by age in range
    def GetByAge(min_age, max_age):
        try:
            all_data = []
            for age in range(min_age, max_age+1):   # [20 21 22 23]
                age_size = r.llen("student:age-" + str(age))
                for i in range(age_size):  # student:age-20 [id, id, id , ...]
                    student_id = r.lindex("student:age-" + str(age), i)
                    student_data = Student.Merge(student_id)
                    all_data.append(student_data)

            return {"data": all_data, "msg": "Success", "status": 1}

        except Exception as error_message:
            return {"data": [], "msg": str(error_message), "status": 0}


    # Get students by birth_address city
    def GetByBirthAddressCity(city):
        try:
            all_data = []
            list_size = r.llen("student:birth_address-city-" + city)
            for i in range(list_size):  # student:birth_address-city [id, id, id , ...]
                student_id = r.lindex("student:birth_address-city-" + city, i)
                student_data = Student.Merge(student_id)
                all_data.append(student_data)

            return {"data": all_data, "msg": "Success", "status": 1}

        except Exception as error_message:
            return {"data": [], "msg": str(error_message), "status": 0}


    # Get students by contain a prize
    def GetByPrize(prize):
        try:
            all_data = []
            list_size = r.llen("student:prize-" + prize)
            for i in range(list_size):  # student:birth_address-prize [id, id, id , ...]
                student_id = r.lindex("student:prize-" + prize, i)
                student_data = Student.Merge(student_id)
                all_data.append(student_data)

            return {"data": all_data, "msg": "Success", "status": 1}

        except Exception as error_message:
            return {"data": [], "msg": str(error_message), "status": 0}






# print(Student.GetByID(1))