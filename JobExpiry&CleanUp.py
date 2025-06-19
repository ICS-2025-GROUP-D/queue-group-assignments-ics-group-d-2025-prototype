class PrintQueueManager:
    def __init__(self, expiry_time=10):
        self.jobs = []
        self.expiry_time = expiry_time

    def enqueue_job(self, user_id, job_id, priority):
        job = {
            'user_id': user_id,
            'job_id': job_id,
            'priority': priority,
            'waiting_time': 0
        }
        self.jobs.append(job)
        print(f"Job {job_id} enqueued by User {user_id} with Priority {priority}.")

    def tick(self):
        for job in self.jobs:
            job['waiting_time'] += 1
        print("System ticked: All job waiting times updated.")

    def remove_expired_jobs(self):
        expired_jobs = [job for job in self.jobs if job['waiting_time'] > self.expiry_time]
        for job in expired_jobs:
            print(f"[EXPIRED] Job {job['job_id']} from User {job['user_id']} "
                  f"expired after {job['waiting_time']} ticks. Removed from queue.")
        self.jobs = [job for job in self.jobs if job['waiting_time'] <= self.expiry_time]

    def show_status(self):
        if not self.jobs:
            print("Queue is currently empty.")
        else:
            print("Current Queue Status:")
            for job in self.jobs:
                print(f"JobID: {job['job_id']} | User: {job['user_id']} | "
                      f"Priority: {job['priority']} | Wait: {job['waiting_time']} ticks")
