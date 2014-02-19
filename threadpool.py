from Queue import Queue
from threading import Thread
from threading import Lock
import traceback

class Task():
    def __init__(self, func, args, kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

class TaskExecutor(Thread):
    running = True
    
    def __init__(self, queue, printlock):
        super(TaskExecutor, self).__init__()
        self.setDaemon(True)
        self.queue = queue
        self.lock = printlock
    
    def print_exc(self):
        self.lock.acquire()
        traceback.print_exc()        
        self.lock.release()
            
    def run(self):
        while self.running:
            try:
                task = self.queue.get()
                try:
                    task.func(*task.args, **task.kwargs)
                except:
                    self.print_exc()
                self.queue.task_done()
            except KeyboardInterrupt:
                self.running = False
                    
class ThreadPool:
    queue = None
    
    def __init__(self, size):
        self.queue = Queue(maxsize=(size * 2))
        self.start_threads(size)
        
    def __enter__(self):
        pass
        
    def __exit__(self, type, value, traceback):
        self.queue.join()
                
    def start_threads(self, num):
        printlock = Lock()
        tes = []
        for _ in range(0, num):
            te = TaskExecutor(self.queue, printlock)
            te.start()
            tes.append(te)

    def submit(self, func, *args, **kwargs):
        task = Task(func, args, kwargs)
        self.queue.put(task, block=True)
