#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;

    do
    {
        height = get_int("enter the height:");
    }while(height < 1 || height > 8);

    for(int row = 0; row < height; row++){
        for(int space = height - row - 1; space > 0; space--){
            printf(" ");
        }

        for(int hash = 0; hash < row + 1; hash++){
            printf("#");
        }
        printf("  ");

        for(int hash = 0; hash < row + 1; hash++){
            printf("#");
        }



        printf("\n");

    }
}