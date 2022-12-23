# easyTask
一款简单易用的定时任务框架
## 快速入门
安装dist\easytask-1.0.0-py3-none-any.whl
```cmd
pip install easytask-1.0.0-py3-none-any.whl
```
导入easytask中的Runnable和Task类
```python
from easytask import Runnable, Task
```
创建任务
```python
def test1():
    print("测试")

t = Task(runner=test1, date="8:00")
```
将任务添加到启动器中并启动
```python
runner = Runnable()
runner.add_job(t)
runner.start()
```
您也可以创建多个任务
```python
def test1():
    print("测试")


def test2():
    print("测试2")
    task1 = Task(runner=test1, date="11:14")
    task2 = Task(runner=test2, date="11:19")
```
使用add_jobs()方法批量添加
```python
runner = Runnable()
runner.add_tasks(task1, task2)
runner.start()
```
