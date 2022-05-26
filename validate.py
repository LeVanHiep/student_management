from pydoc import locate

def is_validate(object, data):
    for key in object:
        if key not in data or data[key] == "":
            return "Missing " + key
        if not isinstance(data[key], locate(object[key])):
            return "Incorrect type of " + key
    return "OK"

# object = {  "password": "str",
#             "name": "str",
#             "age": "int"}

# data = {    
#             "name": "Hiep",
#             "age": "asddsa"}

# print(validate(object, data))