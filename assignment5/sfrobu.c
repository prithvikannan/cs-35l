#include <unistd.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <ctype.h>
#include <stdio.h>


bool isF = false;

// implements comparison between a and b without deobfuscating
int frobcmp(char const *a, char const *b)
{
    // make sure pointers are not null
    if (a != 0 && b != 0)
    {
        // iterate through char array with pointers a and b
        while (*a != ' ' && *b != ' ')
        {
            // unfrobnicate a single byte
            char a_i = *a ^ 42;
            char b_i = *b ^ 42;

            // compare a and b and check which ends first
            if (a_i < b_i || *a == ' ')
            {
                return -1;
            }
            else if (a_i > b_i || *b == ' ')
            {
                return 1;
            }

            a++;
            b++;
        }
    }
    // a and b always equal
    return 0;
}

// custom comparator that calls frobcmp
int cmp(const void *a, const void *b)
{
    return frobcmp(*(char **)a, *(char **)b);
}

int main(int argc, const char *argv[])
{

    // checks for -f option
    if (argc > 2)
    {
        write(2, "Error: Too many arguments.\n", 27);
        exit(1);
    }
    // verify -f option as only possible second argument
    else if (argc == 2)
    {
        if (argv[1][0] != '-' && argv[1][1] != 'f')
        {
            write(2, "Error: Invalid arguments.\n", 26);
            exit(1);
        }
        else
        {
            isF = true;
        }
    }
    isF = false;

    struct stat buf;
    fstat(0, &buf);
    size_t fileSize;
    if (fstat(0, &buf) < 0)
    {
        write(2, "Error with system call.\n", 24);
        exit(1);
    }

    char *regFile;
    char **strArray = NULL;
    int s = -1;
    bool addNewString = true;

    if (S_ISREG(buf.st_mode))
    {
        fileSize = buf.st_size;

        // allocate memory for file
        regFile = (char *)malloc(sizeof(char) * (fileSize + 1));
        if (read(0, regFile, fileSize) < 0)
        {
            write(2, "Error with system call.\n", 24);
            exit(1);
        }

        int words = 0;
        int i = 0;

        while (i < fileSize)
        {
            // make sure first character isn't a space
            if (i == 0 && regFile[i] != ' ')
            {
                words++;
            }

            if (regFile[i] == ' ')
            {
                // account for multiple spaces
                while (regFile[i] == ' ' && i < fileSize)
                {
                    i++;
                }
                // continue counting words
                if (i < fileSize)
                {
                    words++;
                }
            }
            i++;
        }

        // append space at the end of the file
        regFile[fileSize] = ' ';

        // allocate memory for array based on file's word count
        strArray = (char **)malloc(sizeof(char *) * words);
        if (strArray == NULL)
        {
            fprintf(stderr, "Memory allocation error");
            exit(1);
        }

        // add words in file to array
        for (i = 0; i < fileSize; i++)
        {
            if (addNewString && regFile[i] != ' ')
            {
                s++;
                addNewString = false;
                strArray[s] = &regFile[i];
            }
            if (!addNewString && regFile[i] == ' ')
            {
                addNewString = true;
            }
        }
    }
    else
    {
        // allocate new memory for array
        strArray = (char **)malloc(sizeof(char *));
        if (strArray == NULL)
        {
                fprintf(stderr, "Memory allocation error");
            exit(1);
        }
    }

    char *newString;
    char in[1];
    char newChar;
    int c = 0;
    while (true)
    {

        int r = read(0, in, 1);
        if (r == 0)
        {
            break;
        }
        else if (r < 0)
        {
            write(2, "Error reading from standard input.\n", 35);
            exit(1);
        }

        // read in character
        newChar = in[0];

        // if program is still adding characters to existing string
        if (!addNewString)
        {

            // reallocates memory for new character
            newString = (char *)realloc(newString, (c + 1) * sizeof(char));
            if (newString == NULL)
            {
                fprintf(stderr, "Memory allocation error");
                exit(1);
            }

            // updates growing string
            newString[c] = newChar;
            strArray[s] = newString;
            c++;

            // ignore multiple spaces
            if (newChar == ' ')
            {
                addNewString = true;
            }
        }

        // if program must create a new string
        else
        {

            // reset string length
            c = 0;

            // account for multiple spaces
            if (newChar == ' ' && c == 0)
            {
                continue;
            };

            s++;

            // reallocates memory for growing string
            strArray = (char **)realloc(strArray, (s + 1) * sizeof(char *));
            if (strArray == NULL)
            {
                fprintf(stderr, "Memory allocation error");
                exit(1);
            }

            // allocate memory for new string
            newString = (char *)malloc(sizeof(char));
            if (newString == NULL)
            {
                fprintf(stderr, "Memory allocation error");
                exit(1);
            }

            // updates growing string
            newString[c] = newChar;
            strArray[s] = newString;
            c++;

            addNewString = false;
        }
    }

    // append trailing space to the very end
    if (s != -1 && strArray[s][c - 1] != ' ')
    {

        newString = (char *)realloc(newString, (c + 1) * sizeof(char));
        newString[c] = ' ';
        strArray[s] = newString;
    }

    // use frobcomp to sort array of strings
    qsort(strArray, s + 1, sizeof(char *), cmp);

    // print characters to stdout
    int i;
    for (i = 0; i < s + 1; i++)
    {

        int j = 0;
        while (true)
        {

            in[0] = strArray[i][j];

            // print character by character and catch any errors
            if (write(1, in, 1) < 0)
            {
                write(2, "Error outputting characters.\n", 29);
                exit(1);
            }

            // skip to the next string if space byte is detected
            if (strArray[i][j] == ' ')
            {
                break;
            }
            j++;
        }

        if (!S_ISREG(buf.st_mode))
        {
            free(strArray[i]);
        }
    }

    if (S_ISREG(buf.st_mode))
    {
        free(regFile);
    }

    free(strArray);

    exit(0);
}