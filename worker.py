from model import Job, Student, Message
from json import dumps

print("Worker with schedule is running! Looking for jobs...")

while True:
    if Job.exist():
        job_id_list = Job.get_all_id()
        for id in job_id_list:
            job = Job.get_by_id(id)
            #print("Found job " + id + ": " + job["object"] + "." + job["method"])
            func = getattr(eval(job['object']), job['method'])
            if len(job["args"]) == 1:
                result = func(job["args"][0])
            else:
                result = func(job["args"])
            Job.delete_by_id(id)
            Job.create_result(id, dumps(result, ensure_ascii=False).encode('utf8'))
            
            print("Done job " + id + ": " + job["object"] + "." + job["method"])
