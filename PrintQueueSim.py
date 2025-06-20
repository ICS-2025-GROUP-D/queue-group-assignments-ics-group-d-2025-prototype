from datetime import datetime

class PrintJob:
    def __init__(self, user_id, job_id, value, priority):
        self.user_id = user_id
        self.job_id = job_id
        self.value = value
        self.priority = priority
        self.waiting_time = 0
        self.time_added = datetime.now()

    def __repr__(self):
        return f"JobID: {self.job_id}, UserID: {self.user_id}, Priority: {self.priority}, Waiting: {self.waiting_time}"

class PrintQueueManager:
    capacity = 10
    aging_interval = 5
    expiry_time = 20
    def __init__(self):
        self.queue = [None] * self.capacity
        self.size = 0
        self.front = 0
        self.time = 0

    def is_empty(self):
        return self.size == 0

    def enqueue_job(self, user_id, job_id, value, job_priority = 1):
        if self.size == self.capacity:
            print("[ENQUEUE] Queue is full. Cannot enqueue new job.")
            return
        avail = (self.front + self.size) % len(self.queue)
        self.queue[avail] = PrintJob(user_id, job_id, value, job_priority)
        self.size += 1

    def print_job(self):
        if self.is_empty():
            print("[PRINT] Queue is empty. Nothing to print.")
            return
        printed_job = self.queue[self.front]
        self.queue[self.front] = None
        self.front = (self.front + 1) % len(self.queue)
        self.size -= 1
        print(f"[PRINT] print job {printed_job.job_id} successfully printed")
        self.tick()

    def tick(self):
        self.time += 1
        print(f"\n[TICK {self.time}] Advancing simulation...")
        if self.is_empty() is False:
            for job in self.queue:
                if job is not None:
                    job.waiting_time += 1
            self.priority_aging()

    def priority_aging(self):
        if self.is_empty() is False:
            for job in self.queue:
                if job is not None:
                    if job.waiting_time % self.aging_interval == 0:
                        job.priority += 1
                        print(f"\n[PRIORITY] Job {job.job_id} upgraded to priority {job.priority}:")
            for job in self.queue:
                if job is not None:
                    if job.waiting_time > self.expiry_time:
                        print(f"[EXPIRED] Removing Job {job.job_id} after {job.waiting_time} ticks")
                        self.remove_at(job)


    def show_status(self):
        print("\n[STATUS] Current Queue State:")
        if self.is_empty():
            print("Queue is empty.")
            return
        index = self.front
        for job in self.queue:
            if job is not None:
                print(job)

    def remove_at(self, job):
        index = self.queue.index(job)
        actual_index = (self.front + index) % len(self.queue)
        removed_item = self.queue[actual_index]
        for i in range(index, self.size - 1):
            from_index = (self.front + i + 1) % len(self.queue)
            to_index = (self.front + i) % len(self.queue)
            self.queue[to_index] = self.queue[from_index]
        last_index = (self.front + self.size - 1) % len(self.queue)
        self.queue[last_index] = None
        self.size -= 1
        return removed_item

    def rearrange_queue(self):
        if self.is_empty():
            return
        items = [self.queue[(self.front + i) % len(self.queue)] for i in range(self.size)]
        try:
            items.sort(key=lambda x: getattr(x, "priority"))
        except AttributeError:
            raise Exception(f"Elements must have attribute 'priority'")
        self.queue = [None] * self.capacity
        for i, item in enumerate(items):
            self.queue[i] = item
        self.front = 0
        self.size = len(items)

if __name__ == '__main__':
    printer = PrintQueueManager()
    count = 0
    jobs = int(input("How many files do you want to print: "))
    print_details = []
    user_id = int(input("Enter your user id: "))
    while count < jobs:
        value = str(input("Enter name of file: "))
        printer.enqueue_job(23, f"J{count+1}",value)
        count += 1
    count = 0
    while count < jobs:
        printer.show_status()
        printer.print_job()
        count += 1