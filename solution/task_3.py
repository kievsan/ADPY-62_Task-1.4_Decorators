# ЗАДАНИЕ-5.3
# Применить написанный логгер к приложению из любого предыдущего д/з,
# например:
#
# # ЗАДАНИЕ-4.4
# Доработать функцию flat_generator.
# Должен получиться генератор, который принимает список списков
# с любым уровнем вложенности и возвращает их плоское представление.
# Функция test в коде ниже также должна отработать без ошибок.


import types
from collections.abc import Iterable

import datetime
import os
import time


def logger(path):
    def __logger(func):
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
    return __logger


@logger(path='log3_1.log')
def flat_generator(list_of_lists, ignore_types=(str, bytes)):
    for chunk in list_of_lists:
        if isinstance(chunk, Iterable) and not isinstance(chunk, ignore_types):
            yield from flat_generator(chunk)
        else:
            # print(f'\t{chunk}', end=", ")    #
            yield chunk


def test_3():
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    check_list = ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    print(list_of_lists_2)

    paths = ('log3_1.log',)
    for path in paths:
        if os.path.exists(path):
            os.remove(path)

    flat_list = list(flat_generator(list_of_lists_2))
    print(flat_list)

    for flat_item, check_item in zip(flat_list, check_list):
        print(flat_item, flat_item == check_item, check_item)
        assert flat_item == check_item

    assert flat_list == check_list

    assert isinstance(flat_generator(list_of_lists_2), types.GeneratorType)
