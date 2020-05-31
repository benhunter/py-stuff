# Testing with threading and queue modules for Thread-based parallelism

import threading, queue, time


# The worker thread gets jobs off the queue.  When the queue is empty, it
# assumes there will be no more work and exits.
# (Realistically workers will run until terminated.)
def worker():
    print('Running worker')
    time.sleep(0.1)
    while True:
        try:
            arg = q.get(block=False) # False to terminate Thread when no work is available
        except queue.Empty:
            print('Worker', threading.currentThread(), end=' ')
            print('queue empty')
            break
        else:
            print('Worker', threading.currentThread(), end=' ')
            print('running with argument', arg)
            work_func(arg)  # do the work
            time.sleep(0.5)
            q.task_done()  # Create queue

# Work function that processes the arguments
def work_func(arg):
    print('Working on', arg)
    print('Square is', arg**2)
    print('Cube is', arg**3)

q = queue.Queue()

# Begin adding work to the queue
for i in range(20):
    q.put(i)

threadPool = []
# Start a pool of 5 workers
for i in range(5):
    t = threading.Thread(target=worker, name='worker %i' % (i + 1))
    t.start()
    threadPool.append(t)

# time.sleep(5)  # testing if workers die before work is queued - yes they do die

# q.join()

for i in range(20):
    q.put(i+20)

for t in threadPool:
    t.join()

# Give threads time to run
# print('Main thread sleeping')
# time.sleep(5)
print('Main thread finished')