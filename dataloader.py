import json
import requests

with open('data.json', encoding='utf-8') as f:
    students = json.loads(f.read())

for student in students:
    r = requests.post('http://127.0.0.1:5000/', json = student)
    print(f"Created person {student['name']} with {r.text}")