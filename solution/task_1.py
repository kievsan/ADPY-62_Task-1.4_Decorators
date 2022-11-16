# ЗАДАНИЕ-5.1
# Доработать декоратор logger,
# который записывает в файл 'main.log' дату и время вызова функции, имя функции, аргументы,
# с которыми вызвалась и возвращаемое значение.
# Функция test_1 должна отработать без ошибок.

import datetime
import os
import time


def logger(func):
    path = 'main.log'
    func_name = func.__name__

    def wrapper(*args, **kwargs):
        print(f'Работает wrapper для {func_name}:')
        if os.path.exists(path):
            logfile = open(path, 'at', encoding='utf-8')
        else:
            print(f'\tНе найден файл "{path}"!')
            logfile = open(path, 'wt', encoding='utf-8')
        print(f'\tОткрыт для записи файл "{path}"!')

        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()

        logfile.write(f'{datetime.datetime.now()}\t{func_name}:\n')
        logfile.write(f'\tПолучен результат: "{res}" = {func_name}{args}{kwargs}.\n')
        logfile.write(f'\tВремя выполнения: {end - start} секунд.\n')

        logfile.close()
        print(f'\tЗакрыт файл {path}')
        return res

    return wrapper


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'

    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'
