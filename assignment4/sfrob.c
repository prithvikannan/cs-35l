#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

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

// comparator function to pass into qsort in main
int cmp(const void *a, const void *b)
{

    return frobcmp(*(char **)a, *(char **)b);
}

int main()
{

    char current_char;

    // allocate memory for array of strings
    char **arr = (char **)malloc(sizeof(char *));
    // allocate memory for new string
    char *temp_string = (char *)malloc(sizeof(char));

    if (arr == NULL || temp_string == NULL)
    {
        fprintf(stderr, "Memory allocation error");
        exit(1);
    }

    int string_ptr = -1;
    int char_ptr = 0;
    arr[0] = temp_string;
    bool needNewString = true;

    // read from stdin until eof or error
    while (true)
    {
        // read text from standard input
        current_char = getchar();
        if (ferror(stdin))
        {
            fprintf(stderr, "Input read error");
            exit(1);
        }
        else if (feof(stdin))
        {
            break;
        }

        // if program is still adding characters to existing string
        if (!needNewString)
        {
            // increases size of string 
            temp_string = (char *)realloc(temp_string, (char_ptr + 1) * sizeof(char));

            // checks for memory error
            if (temp_string == NULL)
            {
                fprintf(stderr, "Memory allocation error");
                exit(1);
            }

            // space is delimiter of new strings
            if (current_char == ' ')
            {
                needNewString = true;
            }
        }

        // if program must create a new string
        else
        {
            char_ptr = 0;
            
            // if consecutive spaces, then skip iteration
            if (current_char == ' ' && char_ptr == 0)
            {
                continue;
            };

            string_ptr++;

            // increases size of string array
            arr = (char **)realloc(arr, (string_ptr + 1) * sizeof(char *));
            if (arr == NULL)
            {
                fprintf(stderr, "Memory allocation error");
                exit(1);
            }

            // increases size of string
            temp_string = (char *)malloc(sizeof(char));
            if (temp_string == NULL)
            {
                fprintf(stderr, "Memory allocation error");
                exit(1);
            }

            needNewString = false;
        }

        // add new char
        temp_string[char_ptr] = current_char;
        arr[string_ptr] = temp_string;
        char_ptr++;
    }

    // add trailing space if not present
    if (string_ptr != -1 && arr[string_ptr][char_ptr - 1] != ' ')
    {

        temp_string = (char *)realloc(temp_string, (char_ptr + 1) * sizeof(char));
        temp_string[char_ptr] = ' ';
        arr[string_ptr] = temp_string;
    }

    // use custom comparison operator to sort array of strings
    qsort(arr, string_ptr + 1, sizeof(char *), cmp);

    // print to stdout
    int i;
    for (i = 0; i < string_ptr + 1; i++)
    {
        int j = 0;
        while (true)
        {
            // print character by character and catch any errors
            if (putchar(arr[i][j]) == EOF)
            {
                fprintf(stderr, "Printing error");
                exit(1);
            }

            // if space then move to next iteration
            if (arr[i][j] == ' ')
            {
                break;
            }
            j++;
        }
        free(arr[i]);
    }
    free(arr);
    exit(0);
}
