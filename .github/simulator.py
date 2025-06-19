from my_queue import Queue
from visualizer import snapshot

def main():
    q = Queue()
    tick = 0

    # 1) Enqueue a few items
    for job in [11, 22, 33]:
        tick += 1
        q.enqueue(job)
        snapshot(q, "enqueue", tick)

    # 2) Dequeue once
    tick += 1
    removed = q.dequeue()
    print(f"\nRemoved: {removed}")
    snapshot(q, "dequeue", tick)

if __name__ == "__main__":
    main()
