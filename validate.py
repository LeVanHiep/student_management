def login(data):
    if "username" not in data or data["username"] == "": return "Missing username"
    if "password" not in data or data["password"] == "": return "Missing password"
    return "OK"

def id(id):
    if str.isdigit(id): return "OK"
    return "Incorrect ID"

def student(data):
    if "password" not in data or data["password"] == "":        return "Missing password"
    if "name" not in data or data["name"] == "":                return "Missing name"
    if "age" not in data or data["age"] == "":                  return "Missing age"
    if "gender" not in data or data["gender"] == "":            return "Missing gender"
    if "grade" not in data or data["grade"] == "":              return "Missing grade"
    if "school_year" not in data or data["school_year"] == "":  return "Missing school_year"

    if not isinstance(data["age"], int):
        return "Incorrect age"
    if data["gender"] != "nam" and data["gender"] != "nữ":
        return "Incorrect gender"
    if not isinstance(data["school_year"], int):
        return "Incorrect school_year"
    
    return "OK"