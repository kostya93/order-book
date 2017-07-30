from setuptools import setup

setup(
    name='order-book',
    packages=['order_book'],
    entry_points={
        'console_scripts': ['order_book = order_book.order_book:main']
    },
    author='Kostya Charkin',
    author_email='93kostya@gmail.com',
    url='https://github.com/kostya93/order-book',
)
