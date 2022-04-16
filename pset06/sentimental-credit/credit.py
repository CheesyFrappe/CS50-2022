import sys
from cs50 import get_int

def main():
    ccn = get_int("Number: ")

    while ccn < 0:
        ccn = get_int("Number: ")

    #checking if the card is invalid
    validate_credit(ccn)

    if check_sum(ccn):
        print_credit(ccn)
    else:
        print("INVALID")


def check_sum(ccn):

    ccn_str = str(ccn)
    sum = 0
    for i in range(len(ccn_str)):

        if ccn == 0:
            break

        if i % 2 == 0:
            sum += ccn % 10
        else:
            digit = 2 * (ccn % 10)
            sum += digit // 10 + digit % 10

        ccn = ccn // 10
    return (sum % 10) == 0

def print_credit(ccn):

    str_ccn = str(ccn)
    first_digit = int(str_ccn[0])
    second_digit = int(str_ccn[1])

    if first_digit == 3 and second_digit == 4 or second_digit == 7:
        print("AMEX")
    elif first_digit == 5 and 1 <= second_digit <= 5:
        print("MASTERCARD")
    elif first_digit == 4:
        print("VISA")
    else:
        print("INVALID")

def validate_credit(ccn):
    credit_card = str(ccn)

    if len(credit_card) < 13 or 16 < len(credit_card):
        print("INVALID")
        sys.exit(0)


if __name__ == "__main__":
    main()
