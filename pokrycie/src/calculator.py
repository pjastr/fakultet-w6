def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Nie można dzielić przez zero!")
    return a / b

def power(a, b):
    return a ** b