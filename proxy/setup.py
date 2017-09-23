from setuptools import setup

setup(
    name='MyProxy',
    version='0.1',
    py_modules=['myproxy'],
    install_requires=[
            'Click',
            'requests',
    ],
    entry_points='''
            [console_scripts]
            proxy=proxycli:cli
        ''',
)
