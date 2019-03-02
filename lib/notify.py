from termcolor import colored

def normal(s, *args, **kwargs):
    print(s, *args, **kwargs)

def highlight(s, *args, **kwargs):
    print(colored(s, 'yellow'), *args, **kwargs)

def success(s, *args, **kwargs):
    print(colored(s, 'green'), *args, **kwargs)

def failed(s, *args, **kwargs):
    print(colored(s, 'red'), *args, **kwargs)

def subtle(s, *args, **kwargs):
    print(colored(s, 'blue'), *args, **kwargs)
