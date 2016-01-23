import inspect

import tests

if __name__ == '__main__':
    all_functions = dict(inspect.getmembers(tests, inspect.isfunction))

    for fn_name in [key for key in all_functions if key.startswith('test_')]:
        print("Running test {0}".format(fn_name))
        all_functions[fn_name]()
