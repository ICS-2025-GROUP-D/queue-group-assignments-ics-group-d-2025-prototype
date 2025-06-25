import time as tt
import threading
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
        self.lock = threading.Lock()

    def is_empty(self):
        with self.lock:
            return self.size == 0

    def enqueue_job(self, user_id, job_id, value, job_priority=1):
        with self.lock:
            if self.size == self.capacity:
                print("[ENQUEUE] Queue is full. Cannot enqueue new job.")
                return
            avail = (self.front + self.size) % len(self.queue)
            self.queue[avail] = PrintJob(user_id, job_id, value, job_priority)
            self.size += 1
            print(f"[ENQUEUE] New print job {self.queue[avail].job_id} added")

    def print_job(self):
        with self.lock:
            if self.size == 0:
                print("[PRINT] Queue is empty. Nothing to print.")
                return
            printed_job = self.queue[self.front]
            self.queue[self.front] = None
            self.front = (self.front + 1) % len(self.queue)
            self.size -= 1
            print(f"[PRINT] print job {printed_job.job_id} successfully printed")

    def tick(self):
        with self.lock:
            self.time += 1
            print(f"\n[TICK {self.time}] Advancing simulation...")
            for job in self.queue:
                if job is not None:
                    job.waiting_time += 1
            self.priority_aging()

    def priority_aging(self):
        for job in self.queue:
            if job is not None:
                if job.waiting_time % self.aging_interval == 0:
                    job.priority += 1
                    print(f"\n[PRIORITY] Job {job.job_id} upgraded to priority {job.priority}")
        for job in self.queue:
            if job is not None and job.waiting_time > self.expiry_time:
                print(f"[EXPIRED] Removing Job {job.job_id} after {job.waiting_time} ticks")
                self.remove_at(job)
        self.rearrange_queue()
        self.show_status()

    def show_status(self):
        print("\n[STATUS] Current Queue State:")
        with self.lock:
            if self.size == 0:
                print("Queue is empty.")
                return
            for job in self.queue:
                if job is not None:
                    print(job)

    def remove_at(self, job):
        with self.lock:
            for i in range(self.size):
                index = (self.front + i) % len(self.queue)
                if self.queue[index] == job:
                    removed_item = self.queue[index]
                    for j in range(i, self.size - 1):
                        from_index = (self.front + j + 1) % len(self.queue)
                        to_index = (self.front + j) % len(self.queue)
                        self.queue[to_index] = self.queue[from_index]
                    last_index = (self.front + self.size - 1) % len(self.queue)
                    self.queue[last_index] = None
                    self.size -= 1
                    return removed_item
        return None

    def rearrange_queue(self):
        with self.lock:
            if self.size == 0:
                return
            items = [self.queue[(self.front + i) % len(self.queue)] for i in range(self.size)]
            items.sort(key=lambda x: x.priority, reverse=True)
            self.queue = [None] * self.capacity
            for i, item in enumerate(items):
                self.queue[i] = item
            self.front = 0
            self.size = len(items)

def start_processing(print_queue):
    while True:
        print_queue.print_job()
        print_queue.tick()
        tt.sleep(3)

def print_files():
    print_queue = PrintQueueManager()

    try:
        user_id = int(input("Enter your user ID: "))
        job_count = int(input("Enter number of files to add initially: "))
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
        return

    for i in range(1, job_count + 1):
        file = input(f"Enter path to filename #{i}: ").strip()
        print_queue.enqueue_job(user_id, f"J-{i}", file)

    processor = threading.Thread(target=start_processing, args=(print_queue,), daemon=True)
    processor.start()

    print("\nSystem is now processing the queue.\nYou can still submit more files. Type 'exit' to stop.")
    job_index = job_count + 1
    while True:
        file = input("Enter file path (or 'exit' to stop): ").strip()
        if file.lower() == 'exit':
            print("Stopping input. Queue will continue processing remaining jobs...")
            break
        print_queue.enqueue_job(user_id, f"J-{job_index}", file)
        job_index += 1

if __name__ == "__main__":
    print_files()
