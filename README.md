# order-book

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
