import random
import threading
import time
from dataclasses import dataclass, field
from enum import Enum


PHILOSOPHERS = 5
TIMEOUT = 5
WAIT = 0.1


@dataclass
class Fork:
    lock: threading.Lock = field(default_factory=threading.Lock)

    def acquire(self) -> bool:
        return self.lock.acquire(blocking=False)

    def release(self) -> None:
        time.sleep(WAIT)
        if self.lock.locked():
            self.lock.release()


class Side(str, Enum):
    LEFT = 'left'
    RIGHT = 'right'


@dataclass
class Philosopher:
    forks: dict[Side, Fork]
    name: str
    ate_count: int = 0

    def run(self) -> None:
        begin = time.monotonic()
        while time.monotonic() - begin < TIMEOUT:
            self._eat()
            self._think()

    def _eat(self) -> None:
        if not self._acquire_fork(Side.LEFT):
            print(f'{self.name} have not got left fork')
            return

        print(f'{self.name} has left fork')

        if not self._acquire_fork(Side.RIGHT):
            print(f'{self.name} have not got right fork')
            self.forks[Side.LEFT].release()
            return

        print(f'{self.name} is eating')
        time.sleep(WAIT)
        self.ate_count += 1

        self.forks[Side.LEFT].release()
        self.forks[Side.RIGHT].release()

    def _acquire_fork(self, side: Side) -> bool:
        print('Philosopher {} is trying to acquire {} fork'.format(self.name, side))
        time.sleep(WAIT)
        return self.forks[side].acquire()

    def _think(self) -> None:
        print(f'{self.name} is thinking')
        time.sleep(random.random())


def main() -> None:
    forks = [Fork() for _ in range(PHILOSOPHERS)]
    philosophers = [
        Philosopher(
            forks={
                Side.LEFT: forks[i],
                Side.RIGHT: forks[(i + 1) % PHILOSOPHERS],
            },
            name=f'Philosopher {i}',
        )
        for i in range(PHILOSOPHERS)
    ]
    threads = [threading.Thread(target=philosopher.run) for philosopher in philosophers]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    for philosopher in philosophers:
        print(f'{philosopher.name} ate {philosopher.ate_count} times')


if __name__ == '__main__':
    main()
