class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def __len__(self):
        return self.size

    def __repr__(self):
        """Returns a simple front → rear representation of the queue contents."""
        items = []
        current = self.front
        while current:
            items.append(str(current.value))
            current = current.next
        # Join with arrow to show order
        return " ← ".join(items)

    def enqueue(self, value):
        """Add a new value to the end of the queue."""
        new_node = Node(value)
        if not self.rear:
            # Empty queue: front and rear both point to new node
            self.front = self.rear = new_node
        else:
            # Link the old rear to the new node, then update rear
            self.rear.next = new_node
            self.rear = new_node
        self.size += 1

    def dequeue(self):
        """Remove and return the value at the front of the queue."""
        if not self.front:
            raise IndexError("Queue is empty")
        removed_value = self.front.value
        self.front = self.front.next
        if not self.front:
            # If it becomes empty, reset rear as well
            self.rear = None
        self.size -= 1
        return removed_value

    def peek(self):
        """Return the front value without removing it."""
        if not self.front:
            raise IndexError("Queue is empty")
        return self.front.value

    def is_empty(self):
        """Return True if the queue has no elements."""
        return self.front is None
