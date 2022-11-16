# Домашнее задание к лекции 3
# «Decorators»

from solution.task_1 import test_1
from solution.task_2 import test_2
from solution.task_3 import test_3


def print_task_header(title, n=25):
    print('\n', '-' * n, 'ЗАДАНИЕ-' + title, '-' * n)


if __name__ == '__main__':
    print_task_header('1')
    test_1()
    print_task_header('2')
    test_2()
    print_task_header('3')
    test_3()
