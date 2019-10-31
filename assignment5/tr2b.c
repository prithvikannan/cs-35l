#include <stdlib.h>
#include <stdio.h>
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

    while (!feof(stdin))
    {
        char c = getchar();

        if (ferror(stdin))
        {
            fprintf(stderr, "Bad standard input");
            exit(1);
        }
        
        if (c == EOF)
        {
            break;
        }

        if (dict[c] != '\0')
        {
            char output = dict[c];
            putchar(output);
            if (ferror(stdout))
            {
                fprintf(stderr, "Unable to write");
                exit(1);
            }
        }
        else
        {
            putchar(c);
            if (ferror(stdout))
            {
                fprintf(stderr, "Unable to write");
                exit(1);
            }
        }
    }
}
