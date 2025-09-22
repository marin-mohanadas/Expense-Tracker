from setuptools import setup

setup(
    name="expense-tracker",
    version="1.0.0",
    py_modules=[
        "app",
        "utils",
        "expenses"
    ],
    entry_points={
        "console_scripts": [
            "expense-tracker=app:main",
        ],
    }, install_requires=['pandas', 'tabulate']
)
