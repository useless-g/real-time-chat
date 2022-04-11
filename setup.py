from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='my_chat',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    entry_points={
        'console_scripts':[
            'runserver = my_chat.server:main',
            'runclient = my_chat.client:main',
            ]
    },
)