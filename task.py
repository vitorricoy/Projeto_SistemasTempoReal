import multiprocessing

class Task:
    def run_task(self, task, deadline, lost_deadline_register_func):
        p = multiprocessing.Process(target=task)
        p.start()
        p.join(deadline)

        if p.is_alive():
            p.terminate()
            lost_deadline_register_func()
        