def tick(self):
        prev = None
        current = self.front
        while current:
            job = current.value
            job['wait_time'] += 1
            # Priority aging
            if job['wait_time'] % 5 == 0:
                job['priority'] += 1
            # Expiry check
            if job['wait_time'] >= job['max_wait_time']:
                print(f"Expired: Job({job['job_id']}, P:{job['priority']}, W:{job['wait_time']})")
                if prev:
                    prev.next = current.next
                    if current == self.rear:
                        self.rear = prev
                else:
                    self.front = current.next
                    if self.front is None:
                        self.rear = None
                self.size -= 1
                current = current.next if prev else self.front
            else:
                prev = current
                current = current.next

