# order-book

## Table of contents

  * [Specification](#specification)
  * [Usage](#usage)
    * [Using the order_book_runner.py wrapper](#1-using-the-order_book_runnerpy-wrapper)
    * [Installation sets up order_book command](2-installation-sets-up-order_book-command)
  * [Tests](#tests)
    * [unittest](#unittest)
    * [mypy](#mypy)
    * [pycodestyle](#pycodestyle)

## Specification
Необходимо разработать программу для анализа набора промаркированных данных содержащих сообщения двух типов:
 - Добавление заказа (с указанием его цены)
 - Удаление ранее добавленного заказа

В программе должен быть реализован класс `OrderBook`, поддерживающий список текущих заказов, которые были добавлены, но не удалены. Также должна быть возможность запросить текущую максимальную цену заказа. Вы должны использовать этот класс в программе, которая читает входной файл и выводит взвешенную по времени среднюю наивысшую цену заказов. Программа должна принимать один параметр – имя входного файла. 

Формат входных данных.

Каждая строка содержит 3 или 4 поля, разделенные пробелами.
1) Timestamp операции (целое, миллисекунды с начала поступления заказов)
2) Тип операции (один знак, I – добавление заказа, E – удаление заказа)
3) Идентификатор (32-bit целое)
4) Только для добавления заказа. Цена заказа (вещественное, с двойной точностью)

Например:
```
1000 I 100 10.0
2000 I 101 13.0
2200 I 102 13.0
2400 E 101
2500 E 102
4000 E 100
```

В приведенных выше данных есть три интервала, со следующими максимальными ценами заказов:
```
1000-2000 10.0
2000-2500 13.0
2500-4000 10.0
```

Таким образом, взвешенная по времени средняя максимальная цена: 
```
((10 * 1000) + (13 * 500) + (10 * 1500)) / 3000 = 10.5
```

Замечания по поводу формата файла:
- Timestamp'ы монотонно возрастают
- Могут быть периоды, когда нет заказов (в этом случае, такие периоды не должны учитываться)
- Каждый идентификатор появляется ровно два раза: один при добавлении, второй при удалении
- Удаление заказа всегда идет после его добавления

## Usage

### Cloning repository
```
$ git clone https://github.com/kostya93/order-book.git
$ cd order-book
```

### Usage

#### 1. Using the order_book_runner.py wrapper
```bash
$ python3.6 order_book_runner.py [-h] file

positional arguments:
  file        file with list of operations with orders

optional arguments:
  -h, --help  show this help message and exit

```

##### Example
```bash
$ python3.6 order_book_runner.py order_book/example.txt
```

#### 2. Installation sets up order_book command
```
$ python3.6 -m setup.py install
```

Now, the `order_book` command is available.
##### Example
```bash
$ order_book order_book/example.txt
```

## Tests

### unittest
```bash
$ python3.6 -m unittest discover
```

### mypy
```bash
$ python3.6 -m mypy order_book
```

### pycodestyle

```bash
$ python3.6 -m pycodestyle order_book
```
