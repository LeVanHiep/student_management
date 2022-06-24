
from model import Job, Student, Message
from json import loads
from datetime import datetime

print("Worker is running! Looking for jobs...")

while True:
    if Job.exist(schedule=True):
        job_id_list = Job.get_all_id(schedule=True)
        for id in job_id_list:
            job = Job.get_by_id(id)
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
            Job.delete_by_id(id, schedule=True)            
            print("Done job " + id + ": " + job["object"] + "." + job["method"])
