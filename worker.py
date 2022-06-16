
from model import Job, Student, Message
from json import dumps, loads
from datetime import datetime

print("Worker is running! Looking for jobs...")

while True:
    if Job.Exist():
        job_id_set = Job.GetAllID()
        for id in job_id_set:
            job = Job.GetByID(id)
            #print("Found job " + id + ": " + job["object"] + "." + job["method"])
            if "time" in job["args"][0]:
                arg = loads(job["args"][0])
                string_time = arg["time"]
                job_time = datetime.strptime(string_time, "%H:%M %d/%m/%Y")
                if job_time > datetime.now():
                    continue
            func = getattr(eval(job['object']), job['method'])
            if len(job["args"]) == 1:
                result = func(job["args"][0])
            else:
                result = func(job["args"])
            Job.DeleteByID(id)
            Job.CreateResult(id, dumps(result, ensure_ascii=False).encode('utf8'))
            
            print("Done job " + id + ": " + job["object"] + "." + job["method"])
