import pytest

from app.calculations import BankAccount, add, divide, InsufficientFunds, multiply, subtract


# Bank accounts fixtures ---------------------------------------

@pytest.fixture
def zero_bank_account():
    print("creating empty bank account")
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


# Testing Basic calculations ---------------------------------------

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 6, 9),
    (3, 2, 5),
    (10, 100, 110)
])
def test_add(num1, num2, expected):
    print("Testing add function")
    assert add(num1, num2) == expected


# def test_add():
#     print("Testing add function")
#     assert add(10, 4) == 14


def test_divide():
    print("Testing divide function")
    assert divide(10, 4) == 2.5


def test_multiply():
    print("Testing multiply function")
    assert multiply(10, 4) == 40


def test_subtract():
    print("Testing subtract function")
    assert subtract(10, 4) == 6


# Testing Bank accounts ---------------------------------------
def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    print("testing my bank account")
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80


def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55


@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 500, 700)

])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
