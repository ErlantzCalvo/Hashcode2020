#!/usr/bin/python3
import sys
import os

def main():
    if len(sys.argv) < 2:
        sys.exit('Syntax: %s <filename>' % sys.argv[0])

    print('Running on file ', sys.argv[1])
    print("\n")

    filename = sys.argv[1]
    read_file(filename)

def read_file(filename):
    with open(filename, 'r') as f:
        line = f.readline()
        print(line)
        for l in range(int(line)):
            line = f.readline()
            a = int(line)
            for i in range(a):
                new_line = f.readline()
                print(new_line)

if __name__ == '__main__':
    main()