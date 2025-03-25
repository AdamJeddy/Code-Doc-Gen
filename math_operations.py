# Description: This file contains the implementation of basic math operations

# add function
def add(a, b):
    return a + b

# subtract function
def subtract(a, b):
    return a - b

# multiply function
def multiply(a, b):
    return a * b

# very important to handle the case where b is 0
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# exponentiation function
def exponentiate(a, b):
    return a ** b

# modulo function
def modulo(a, b):
    return a % b