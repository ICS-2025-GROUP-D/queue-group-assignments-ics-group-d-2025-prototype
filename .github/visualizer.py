def snapshot(queue, event_name, tick):
    print(f"\n[Tick {tick}] After {event_name}:")
    print(queue)  # uses Queue.__repr__ to show contents
