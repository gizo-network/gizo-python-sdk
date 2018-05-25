import json

class JobRequest:
    def __init__(self, job_id: str, job_exec: dict):
        self.id = job_id
        self.job_exec = job_exec
    def jr(self):
        return json.dumps({'ID': self.id, 'Exec': self.job_exec})


