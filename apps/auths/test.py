import random


def generate_phones():
    first = str(random.randint(100, 999))
    second = str(random.randint(1, 888)).zfill(3)
    last = (str(random.randint(1, 9998)).zfill(4))
    template: list[str] = [
        '1111', '2222',
        '3333', '4444',
        '5555', '6666',
        '7777', '8888'
    ]
    while last in template:
        last = (str(random.randint(1, 9998)).zfill(4))
    return '+7{}-{}-{}'.format(first, second, last)
