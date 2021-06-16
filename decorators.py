from time import sleep, time
from random import random
from string import punctuation


def calc_duration(func):
    """
    A decorator that counts the execution time of a function
    and outputs it to the console.
    """
    def decorated(*args, **kwargs):
        start_time = time()
        func(*args, **kwargs)
        print(f"elapsed time is about {time()-start_time} seconds")
    return decorated


@calc_duration
def long_executing_task():
    for index in range(3):
        print(f'Iteration {index + 1}')
        sleep(random())


def suppress_errors(exp_err):
    """
    A decorator that displays a message instead of an exception
    """
    def decorator(func):
        def decorated(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exp_err as e:
                print(f"{type(e).__name__} due to {e}.")
        return decorated
    return decorator


@suppress_errors((
    KeyError,
    ValueError,
))
def potentially_unsafe_func(key: str):
    print(f'Get data by the key {key}')
    data = {'name': 'test', 'age': 30}
    return data[key]


def result_between(value_min, value_max):
    """
    A decorator validating by minimum and maximum value
    """
    def decorator(func):
        def decorated(*args, **kwargs):
            result = func(*args, **kwargs)
            if not(value_min <= result <= value_max):
                raise ValueError
            return result
        return decorated
    return decorator


def len_more_than(s_len):
    """
    A decorator validating by length string
    """
    def decorator(func):
        def decorated(*args, **kwargs):
            result = func(*args, **kwargs)
            if len(result) < s_len:
                raise ValueError
            return result
        return decorated
    return decorator


@result_between(0, 10)
def sum_of_values(numbers):
    return sum(numbers)


@len_more_than(10)
def show_message(message: str) -> str:
    return f'Hi, you sent: {message}'


def replace_commas(func):
    """
    A decorator that replaces punctuation marks with spaces
    """
    def decorated(*args, **kwargs):
        result = func(*args, **kwargs)
        for i in punctuation:
            result = result.replace(i, ' ')
        return result
    return decorated


def words_title(func):
    """
    A decorator makes the first and last letter uppercase in each word
    """
    def decorated(*args, **kwargs):
        result = func(*args, **kwargs)
        result = result.split(' ')
        i = 0
        for word in result:
            if word.isalnum():
                word = word[0].upper() + word[1:-1] + word[-1].upper()
            result[i] = word
            i += 1
        return ' '.join(result)
    return decorated


@words_title
@replace_commas
def process_text(text: str) -> str:
    return text.replace(':', ',')


@replace_commas
@words_title
def another_process(text: str) -> str:
    return text.replace(':', ',')


def cache_result():
    """
    A decorator-cache that stores the result of executing a function
    for the specified arguments and returns it
    if the function is called again with a certain set of arguments.
    """
    cache = {}

    def decorator(func):
        def decorated(*args, **kwargs):
            if args not in cache:
                cache[args] = func(*args, **kwargs)
            return cache[args]
        return decorated
    return decorator


@cache_result()
def some_func(last_name, first_name, age):
    return f'Hi {last_name} {first_name}, you are {age} years old'


if __name__ == '__main__':
    long_executing_task()

    print()
    print(potentially_unsafe_func('name'))
    print(potentially_unsafe_func('last_name'), "\n")

    try:
        print(sum_of_values((1, 3, 5, 7)))
    except ValueError:
        print("ValueError")

    try:
        print(show_message('Howdy, howdy my little friend'), "\n")
    except ValueError:
        print("ValueError")

    print(process_text('the French revolution resulted in 3 concepts: freedom,equality,fraternity'))
    print(another_process('the French revolution resulted in 3 concepts: freedom,equality,fraternity'), "\n")

    print(some_func('shulyak', 'dmitry', 30))
    print(some_func('ivanov', 'ivan', 25))
    print(some_func('shulyak', 'dmitry', 30), "\n")
