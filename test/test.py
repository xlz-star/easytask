import datetime

from easytask import Task, Runnable


def test1():
    print("测试")


def test2():
    print("测试2")


if __name__ == "__main__":
    task1 = Task(runner=test1, date="11:14")
    task2 = Task(runner=test2, date="11:19")
    runner = Runnable()
    runner.add_tasks(task1, task2)
    runner.start()
