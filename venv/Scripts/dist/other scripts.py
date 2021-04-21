queue, m, ms = [], 0, -1
for i in range(int(input())):
    queue.append(int(input()))
    if len(queue) == 7:
        dz =queue.pop(0)
        m = max([dz, m]) if dz % 2 else m
        ms = max([ms, queue[len(queue) - 1] + m]) if queue[len(queue) - 1] % 2 else ms
print(ms)