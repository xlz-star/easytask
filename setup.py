from setuptools import find_packages, setup

with open("requirements.txt", "r", encoding="utf-8") as f:
    install_requires = f.readlines()

setup(
    name='easytask',
    version="1.0.0",
    author="XLZ",
    description='简易定时任务框架',
    keywords='Scheduled Tasks',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
    ],
    url='https://lyxlz.cn',
    author_email='xu-ling-zhi@qq.com',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=install_requires,
    zip_safe=False
)