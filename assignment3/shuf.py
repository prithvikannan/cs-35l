#!/usr/bin/python

# Prithvi Kannan
# UID: 405110096

import random, sys, argparse, string

from optparse import OptionParser

class shuf:

    def __init__(self, inputs, num_lines, isRepeat):
        self.inputs = inputs
        self.isRepeat = isRepeat
        self.num_lines = num_lines

        random.shuffle(self.inputs)

    def shuffleline(self):
        if not len(self.inputs):
            return
        
        if self.isRepeat:
            while self.num_lines > 0:
                sys.stdout.write(random.choice(self.inputs))
                self.num_lines = self.num_lines- 1
        else:
            for i in range(0, self.num_lines):
                sys.stdout.write(self.inputs[i])   


def main():
    version_msg = "%prog 2.0"
    usage_msg = """%prog [OPTION]... FILE
    or:  %prog -i LO-HI [OPTION]...
    Write a random permutation of the input lines to standard output."""

    parser = OptionParser(version=version_msg, usage=usage_msg)

    parser.add_option("-n", "--head-count",
        action="store", dest="num_lines", default=sys.maxsize,
        help="output at most count lines")
    
    parser.add_option("-i", "--input-range",
        action="store", dest="inputRange", default="",
        help="treat each number LO through HI as an input line")

    parser.add_option("-r", "--repeat",
        action="store_true", dest="isRepeat", default=False,
        help="output lines can be repeated")

    options, args = parser.parse_args(sys.argv[1:])

    try:
        num_lines = int(options.num_lines)
    except:
        parser.error("invalid count: {0}".format(options.num_lines))
    if num_lines < 0:
        parser.error("negative count {0}".format(num_lines))

    isRepeat = options.isRepeat

    inputRange = options.inputRange
    if len(inputRange) > 0:
        if len(args) != 0:
            parser.error("extra operand '{0}'".format(args[0]))

        try:
            isDash = inputRange.index('-')
        except ValueError as e:
            parser.error("invalid input range: '{0}'".
            format(options.inputRange))
        if isDash == 0:
            parser.error("invalid input range: '{0}'".
            format(options.inputRange))

        first, last = inputRange.split("-")
        
        try:
            firstNum = int(first)
        except ValueError as e:
            parser.error("invalid input range: '{0}'".
            format(options.inputRange))
        
        try:
            lastNum = int(last)
        except ValueError as e:
            parser.error("invalid input range: '{0}'".
            format(options.inputRange))

        if first > last:
            parser.error("invalid input range: '{0}'".
            format(options.inputRange))

        inputs = list(range(firstNum,lastNum+1))
        for i in range(len(inputs)):
            inputs[i] = str(inputs[i]) + "\n"

    else:
        if len(args) == 0: 
            if (len(args) == 1 and args[0] == "-"):
                inputs = sys.stdin.readlines()
        
        elif len(args) == 1:
            try:
                f = open(args[0], 'r')
                inputs = f.readlines()
                f.close()
            except IOError as e:
                errno, strerror = e.args
                parser.error("I/O error({0}): {1}".format(errno,strerror))

        else:
            parser.error("extra operand '{0}'".format(args[1]))


    if num_lines > len(inputs) and not isRepeat:
        num_lines = len(inputs)

    shuffler = shuf(inputs, num_lines, isRepeat)
    shuffler.shuffleline()

if __name__ == "__main__":
    main()