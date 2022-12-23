import threading

from loguru import logger

from easytask.task import Task


class Runnable:
    """
    执行任务类
    """

    def __init__(self) -> None:
        self.__log__ = logger
        self.__task__ = None
        self.__tasks__ = []

    def add_job(self, date: str = None, runner=None):
        """
        添加任务
        :args 
            date: str 要执行runner的时间, 格式为 00:00
            runner: function 要执行的方法
        """
        task = Task(runner=runner, date=date)
        self.__task__ = task

    def add_task(self, task: Task = None):
        """
        添加任务
        :args 
            task: Task 要执行的任务, 默认为None
        """
        self.__task__ = task

    def add_tasks(self, *tasks):
        """
        添加多任务
        :args
            tasks: list 要执行的多个任务,默认为空
        """
        if len(tasks) != 0:
            for task in tasks:
                self.__tasks__.append(task)

    def start(self):
        """
        启动任务
        """
        if len(self.__tasks__) == 0:
            self.__task__.run()
        else:
            for task in self.__tasks__:
                t = threading.Thread(target=task.run, name=task)
                self.__log__.debug(f"线程{task} 已启动")
                t.setDaemon(True)
                t.start()

        while len(threading.enumerate()) != 1:
            pass

