import time
from dataclasses import dataclass


@dataclass
class Scheduler:
    tasks: list

    def run(self):
        while self.tasks:
            for i, (task, task_name) in enumerate(self.tasks[:]):
                try:
                    next(task)
                except StopIteration:
                    self.tasks.pop(i)
                time.sleep(0.5)
                print(f'Running task {task_name}')

        print('Scheduler finished')


@dataclass
class MySleep:
    delay: int

    def run(self):
        begin = time.monotonic()
        while begin + self.delay > time.monotonic():
            yield



if __name__ == '__main__':
    scheduler = Scheduler([(MySleep(1).run(), '1'), (MySleep(2).run(), '2'), (MySleep(3).run(), '3')])
    scheduler.run()
