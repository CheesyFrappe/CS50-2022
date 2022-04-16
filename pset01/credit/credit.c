#include <cs50.h>
#include <stdio.h>

bool checksum(long long ccn);
int find_length(long long ccn);
void print_credit(long long ccn);

int main(void)
{

    long long ccn;
    do
    {
        ccn = get_long("number: ");
    } while (ccn < 0);

    // if credit car number is valid
    if (checksum(ccn))
        print_credit(ccn);
    else
        printf("INVALID\n");
}

bool checksum(long long ccn) // Luhn's Algorithm
{
    int sum = 0;
    for (int i = 0; ccn != 0; i++, ccn /= 10)
    {
        if (i % 2 == 0)
        {
            sum += ccn % 10;
        }
        else
        {
            int digit = 2 * (ccn % 10);
            sum += digit / 10 + digit % 10;
        }
    }
    return (sum % 10) == 0;
}

int find_length(long long ccn)
{
    int len = 0;
    for (int i = 0; ccn != 0; i++, ccn /= 10)
    {
        len++;
    }
    return len;
}

void print_credit(long long ccn)
{
    // if credit car number starts with 34 or 37 and the length is 15
    if ((ccn >= 34e13 && ccn < 35e13) || (ccn >= 37e13 && ccn < 38e13))
        printf("AMEX\n");
    // if credit car number starts with (51,52,53,54,55) and the length is 16
    else if ((ccn >= 51e14 && ccn < 56e14))
        printf("MASTERCARD\n");
    //  if credit car number starts with 4 and the length is 13 or 16
    else if ((ccn >= 4e12 && ccn < 5e12) || (ccn >= 4e15 && ccn < 5e15))
        printf("VISA\n");
    else
        printf("INVALID\n");
}