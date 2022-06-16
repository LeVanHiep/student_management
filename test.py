from datetime import datetime

job = "12:10 25/02/2000"
print(datetime.strptime(job, "%H:%M %d/%m/%Y"))