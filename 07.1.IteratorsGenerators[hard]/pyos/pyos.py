from queue import Queue
from abc import ABC, abstractmethod
from typing import Generator, Optional, Any, Dict, List


class SystemCall(ABC):
    """SystemCall yielded by Task to handle with Scheduler"""

    @abstractmethod
    def handle(self, scheduler: 'Scheduler', task: 'Task') -> bool:
        """
        :param scheduler: link to scheduler to manipulate with active tasks
        :param task: task which requested the system call
        :return: an indication that the task must be scheduled again
        """


Coroutine = Generator[Optional[SystemCall], Any, None]


class Task:
    sys_return = None

    def __init__(self, task_id: int, target: Coroutine):
        """
        :param task_id: id of the task
        :param target: coroutine to run. Coroutine can produce system calls.
        System calls are being executed by scheduler and the result sends back to coroutine.
        """
        self._task_id = task_id
        self._target = target

    def step(self) -> Optional[SystemCall]:
        """
        Performs one step of coroutine, i.e. sends result of last system call
        to coroutine (generator), gets yielded value and returns it.
        """
        return self._target.send(self.sys_return)

    @property
    def task_id(self):
        return self._task_id

    def close_target(self):
        self._target.close()


class Scheduler:
    """Scheduler to manipulate with tasks"""

    def __init__(self) -> None:
        self.task_id = 0
        self.task_queue: Queue[Task] = Queue()
        self.task_map: Dict[int, Task] = {}  # task_id -> task
        self.wait_map: Dict[int, List[Task]] = {}  # task_id -> list of waiting tasks
        self.delete_list = []

    def new(self, target: Coroutine) -> int:
        """Create and schedule new task
        :param target: coroutine to wrap in task
        :return: id of newly created task
        """
        self.task_id += 1
        task = Task(self.task_id, target)
        self.task_map[self.task_id] = task
        self.schedule_task(task)
        id_to_return = self.task_id
        return id_to_return

    def schedule_task(self, task: Task) -> None:
        """PRIVATE API: can be used only from scheduler itself or system calls
        :param task: task to schedule for execution
        """
        self.task_queue.put(task)

    def exit_task(self, task: Task) -> None:
        """PRIVATE API: can be used only from scheduler itself or system calls
        :param task: task to remove from scheduler
        Hint: do not forget to reschedule waiting tasks
        """
        del self.task_map[task.task_id]

    def wait_task(self, task: Task, wait_id: int) -> bool:
        """PRIVATE API: can be used only from scheduler itself or system calls
        :param task: task to hold on until another task is finished
        :param wait_id: id of the other task to wait for
        :return: true if wait id is a valid task id
        """

    def run(self, ticks: Optional[int] = None) -> None:
        """Executes tasks consequently, gets yielded system calls,
        handles them and reschedules task if needed
        :param ticks: number of iterations (task steps), infinite if not passed
        """
        if ticks is None:
            while True:
                if not self.task_map:
                    break
                task = self.task_queue.get()
                if task.task_id in self.delete_list:
                    self.exit_task(task)
                    continue
                try:
                    sys_call = task.step()
                except StopIteration:
                    self.exit_task(task)
                    continue
                if sys_call is None:
                    pass
                else:
                    sys_call.handle(self, task)
                self.task_queue.put(task)
            return
        for _ in range(ticks):
            if not self.task_map:
                break
            task = self.task_queue.get()
            if task.task_id in self.delete_list:
                self.exit_task(task)
                continue
            try:
                sys_call = task.step()
            except StopIteration:
                self.exit_task(task)
                continue
            if sys_call is None:
                pass
            else:
                sys_call.handle(self, task)
            self.task_queue.put(task)

    def empty(self) -> bool:
        """Checks if there are some scheduled tasks"""
        return not bool(self.task_map)


class GetTid(SystemCall):
    """System call to get current task id"""

    def handle(self, scheduler: 'Scheduler', task: 'Task') -> bool:
        task.sys_return = task.task_id
        return True


class NewTask(SystemCall):
    """System call to create new task from target corotine"""

    def __init__(self, target: Coroutine):
        self.target = target

    def handle(self, scheduler: 'Scheduler', task: 'Task') -> bool:
        task.sys_return = scheduler.new(self.target)
        return True


class KillTask(SystemCall):
    """System call to kill task with particular task id"""

    def __init__(self, task_id: int):
        self.task_id = task_id

    def handle(self, scheduler: 'Scheduler', task: 'Task') -> bool:
        scheduler.delete_list.append(self.task_id)
        return True


class WaitTask(SystemCall):
    """System call to wait task with particular task id"""

    def __init__(self, task_id: int):
        self.task_id = task_id

    def handle(self, scheduler: 'Scheduler', task: 'Task') -> bool:
        # Note: One shouldn't reschedule task which is waiting for another one.
        # But one must reschedule task if task id to wait for is invalid.
        pass
