from datetime import datetime

class PrintJob:
    def __init__(self, job_id, user_id, value, job_priority):
        self.job_id = job_id
        self.user_id = user_id
        self.job_priority = job_priority
        self.time_added = datetime.now()
        self.value = value

class PrintQueue:
    queue_capacity = 10
    def __init__(self):
        self.data = [None] * self.queue_capacity
        self.size = 0
        self.front = 0

    def enqueue_job(self, job_id, user_id, value, job_priority):
        if self.size == self.queue_capacity:
            print("Print queue is full")
            return
        avail = (self.front + self.size) % len(self.data)
        self.data[avail] = PrintJob(job_id, user_id, value, job_priority)
        self.size += 1

    def is_empty(self):
        return self.size == 0

    def show_status(self):
        print("Current Queue State:")
        index = self.front
        for _ in range(self.size):
            job = self.data[index]
            print(
                f"JobID: {job.job_id}, UserID: {job.user_id}, Priority: {job.job_priority}, Value: {job.value}, Time: {job.time_added}")
            index = (index + 1) % self.queue_capacity

    def print_job(self):
        if self.is_empty():
            print("Print queue is empty")
            return
        answer = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % len(self.data)
        self.size -= 1
        return answer.value