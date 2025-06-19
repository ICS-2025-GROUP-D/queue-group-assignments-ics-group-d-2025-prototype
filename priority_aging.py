import heapq
import time

class PrintJob:
    def __init__(self, user_id, job_id, priority):
        self.user_id = user_id
        self.job_id = job_id
        self.original_priority = priority
        self.timestamp = time.time()
        self.status = "queued"

    def __repr__(self):
        return f"Job({self.job_id}, User:{self.user_id}, P:{self.original_priority}, T:{int(self.timestamp)})"

class PrintQueueManager:
    def __init__(self, aging_interval=30, priority_step=1, min_priority=1):
        self.queue = []
        self.aging_interval = aging_interval
        self.priority_step = priority_step
        self.min_priority = min_priority
        self.current_time = time.time()


    def enqueue_job(self, user_id, job_id, priority):
        job = PrintJob(user_id, job_id, priority)
        heapq.heappush(self.queue, (priority, job.timestamp, job))

    # apply priority aging based on the wait time
    def apply_priority_aging(self):
        aged_queue = []
        for _, _, job in self.queue:
            wait_time = self.current_time - job.timestamp
            aging_steps = int(wait_time // self.aging_interval)
            new_priority = max(self.min_priority, job.original_priority - (aging_steps * self.priority_step))
            aged_queue.append((new_priority, job.timestamp, job))
        heapq.heapify(aged_queue)
        self.queue = aged_queue
