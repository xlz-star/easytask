import datetime
import re
import time
from loguru import logger


class Task:
    """
    任务类，单个任务类的run为阻塞型任务, 需要通过Runnable进行线程调度
    """

    def __init__(self, runner=None, date="") -> None:
        """
        :args
            runner: 要执行的函数
            date: 执行函数的时间
        """
        self.__log__ = logger
        self.__runner__ = runner
        self.__date__ = self.__checkDate__(date)
        # 下次执行的时间
        self.__nextTime__: bool = False
        self.__nextRunTime__: str = self.__getNextRunTime__()

    def run(self) -> None:
        """
        启动任务
        """
        self.__log__.info(f"任务开始，下一次执行时间为 [ {self.__nextRunTime__} ]")
        # 验证任务是否存在
        if self.__runner__ is None:
            self.__log__.error("未指定任务")
            raise Exception("task任务错误")
        # 当执行时间匹配时执行任务
        if self.__checkTime__():
            self.__log__.info("任务执行完成")
            self.__runner__()

    def __checkTime__(self) -> bool:
        """
        未到时间使线程休眠
        """
        # 获取执行时间的时、分
        date_split = self.__date__.split(":")
        date_hour = int(date_split[0])
        date_minute = int(date_split[1])
        while True:
            now = time.strftime("%H:%M:%S", time.localtime())
            self.__log__.debug(f"当前时间{str.join(':', now.split(':')[0:2])} 目标时间{self.__date__}")
            if str.join(":", now.split(":")[0:2]) != self.__date__:
                # 获取当前时间的时、分
                now_split = now.split(":")
                now_hour = int(now_split[0])
                now_minute = int(now_split[1])
                now_sec = int(now_split[2])
                # 获取剩余等待时间
                hour = date_hour - now_hour
                minute = date_minute - now_minute
                sleep_time = 0
                if minute > 0:
                    if hour > 0:
                        sleep_time = 60 * 60 * hour + minute - now_sec
                    elif hour < 0:
                        sleep_time = 60 * 60 * (24 + hour) + minute - now_sec
                    elif hour == 0:
                        sleep_time = 60 * minute - now_sec
                    elif hour == 1:
                        sleep_time = 60 * 60 * hour + minute - now_sec
                elif minute < 0:
                    if hour > 0:
                        sleep_time = 60 * 60 * hour + (60 - minute) - now_sec
                    elif hour < 0:
                        sleep_time = 60 * 60 * (24 + hour) + (60 - minute) - now_sec
                    elif hour == 0:
                        sleep_time = 60 * 60 * 24 + (60 - minute) - now_sec
                    elif hour == 1:
                        sleep_time = 60 * 60 * hour + (60 - minute) - now_sec
                self.__log__.info(f"正在等待, 线程休眠 {self.getSleepStr(sleep_time)}")
                time.sleep(sleep_time)
            else:
                return True

    def __getNextRunTime__(self):
        """
        获取下一次执行任务的时间
        """
        now_hour = int(time.strftime("%H", time.localtime()))
        now_minute = int(time.strftime("%M", time.localtime()))
        hour = int(self.__date__.split(":")[0])
        minute = int(self.__date__.split(":")[1])
        ""
        if ((hour - now_hour) < 0) or ((minute - now_minute) < 0):
            self.__nextTime__ = True
        if self.__nextTime__:
            nextRunTime = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        else:
            nextRunTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        return re.sub(r"\d\d:\d\d", self.__date__, nextRunTime)

    def __checkDate__(self, date):
        """
        验证日期
        """
        # 验证日期格式是否正确
        date_check_match = re.compile(r"\d{1,2}:\d{1,2}")
        if re.fullmatch(date_check_match, date) is None:
            self.__log__.error("日期格式不正确")
            raise Exception("task日期错误")
        # 前后补零
        result = date
        date_hour_format_match = re.compile(r"\d:\d\d")
        date_minute_format_match = re.compile(r"\d\d:\d")
        if re.fullmatch(date_hour_format_match, date):
            self.__log__.debug("小时补零")
            result = '0' + date
        elif re.fullmatch(date_minute_format_match, date):
            self.__log__.debug("分钟补零")
            date_split = date.split(":")
            result = str.join(":", [date_split[0], '0' + date_split[1]])
        return result

    def getSleepStr(self, sleepTime):
        """
        将等待时间转换为时分秒的格式
        """
        self.__log__.debug(sleepTime)
        m, s = divmod(sleepTime, 60)
        h, m = divmod(m, 60)
        return f"{h}时 {m}分 {s}秒"

    def __str__(self) -> str:
        return str(self.__runner__) + " -> " + str(self.__date__)





