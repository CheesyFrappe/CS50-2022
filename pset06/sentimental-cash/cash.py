from cs50 import get_float



def main():

    cents = get_cents()

    quarters = calculate_quarters(cents)
    cents = cents - quarters * 25

    dimes = calculate_dimes(cents)
    cents = cents - dimes * 10

    nickels = calculate_nickels(cents)
    cents = cents - nickels * 5

    pennies = calculate_pennies(cents)
    cents = cents - pennies * 1

    coins = quarters + dimes + nickels + pennies

    print(coins)


def get_cents():

    change = get_float("Change owed: ")

    while change <= 0:
        change = get_float("Change owed: ")

    change = round(change * 100)

    return change

def calculate_quarters(cents):

    i = 0
    while cents >= 25:
        cents = cents - 25
        i+=1

    return i

def calculate_dimes(cents):

    i = 0
    while cents >= 10:
        cents = cents - 10
        i+=1

    return i

def calculate_nickels(cents):

    i = 0
    while cents >= 5:
        cents = cents - 5
        i+=1

    return i

def calculate_pennies(cents):

    i = 0
    while cents >= 1:
        cents = cents - 1
        i+=1

    return i

main()