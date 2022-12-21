
# This function adds two numbers
def add(num1: float, num2: float) -> float:
    return num1 + num2


# This function subtracts two numbers
def subtract(num1: float, num2: float) -> float:
    return num1 - num2


# This function multiplies two numbers
def multiply(num1: float, num2: float) -> float:
    return num1 * num2


# This function divides two numbers
def divide(num1: float, num2: float) -> float:
    return num1 / num2


class InsufficientFunds(Exception):
    pass


class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFunds("Insufficient funds in account")

        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1
