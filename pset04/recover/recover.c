#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    FILE *input_file = fopen(argv[1], "r");
    FILE *output_file = NULL;

    if (input_file == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    unsigned char buffer[512];

    int count_image = 0;

    char *filename = malloc(8 * sizeof(char));

    while (fread(buffer, sizeof(char), 512, input_file) != 0)
    {
        if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0) {
            sprintf(filename, "%03i.jpg", count_image);

            output_file = fopen(filename, "w");

            count_image++;
        }

        if (output_file != NULL)
        {
            fwrite(buffer, sizeof(char), 512, output_file);
        }
    }
   
    return 0;
}