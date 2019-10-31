
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>

int main(int argc, const char *argv[])
{

    if (argc != 3)
    {
        fprintf(stderr, "Invalid number of arguments");
        exit(1);
    }
    const char *fromPtr = argv[1];
    const char *toPtr = argv[1];

    if (strlen(fromPtr) != strlen(toPtr))
    {
        fprintf(stderr, "Strings are different length");
        exit(1);
    }

    char dict[256] = {'\0'};

    char c[1];
    char output[1];
    int i;
    for (i = 0; i < strlen(fromPtr); i++)
    {
        if (dict[fromPtr[i]] != '\0')
        {
            fprintf(stderr, "Found duplicate letter");
            exit(1);
        }
        dict[fromPtr[i]] = toPtr[i];
    }

    while (read(0, c, 1) > 0)
    {
        if (dict[c[0]] != '\0')
        {
            output[0] = dict[c[0]];
            if (write(1, output, 1) < 0)
            {
                fprintf(stderr, "Unable to write");
                exit(1);
            }
        }
        else
        {
            if (write(1, c, 1) < 0)
            {
                fprintf(stderr, "Unable to write");
                exit(1);
            }
        }
    }
}