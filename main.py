#!/usr/bin/python3
import sys
import os
import functools, math


numbooks = 0
numLibraries = 0
numDays = 0
actualDay = 0
books = {}
libraries = []

@functools.total_ordering
class Library:

    def __init__(self, libraryNumber, bookNumber, signupDays, booksPerDay):
        self.libraryNumber = libraryNumber
        self.bookNumber = bookNumber
        self.signupDays = signupDays
        self.booksPerDay = booksPerDay
        self.books = []
        self.score = 0

    def __eq__(self,library):
        return self.libraryNumber == library.libraryNumber

    def __gt__(self,library):
        return self.score > library.score if self.score != library.score else len(self.books) / self.booksPerDay < len(library.books) / library.booksPerDay

    def addBook(self, book):
        self.books.append(book)
        
    def fitness(self):
        global numDays
        global actualDay
        score = ((numDays - actualDay - self.signupDays) - self.bookNumber/self.booksPerDay)      
        if score > 0:
            self.score = 1/score
        elif score < 0:
            self.score = -1*score
        else:
            self.score = math.inf

@functools.total_ordering
class Book:
    def __init__(self, score, bookId):
        self.score = score
        self.bookId = bookId
        
    def __gt__(self,book):
        return self.score > book.score

    def __eq__(self,book):
        return self.bookId == book.bookId

    def __str__(self):
        return str(self.bookId)

def main():
    if len(sys.argv) < 2:
        sys.exit('Syntax: %s <filename>' % sys.argv[0])
        
    global actualDay, numDays, libraries, books, numBooks, numLibraries, numbooks
    print('Running on file ', sys.argv[1])
    print("\n")

    filename = sys.argv[1]
    read_file(filename)

    librariesToScan = 0
    finalString = ""

    for i in libraries:
        i.fitness()
    
    while (actualDay <= numDays) and len(libraries) != 0:
        libraries.sort(reverse=True)
        actualDay += libraries[0].signupDays
        l = libraries.pop(0)
        l.books.sort()
        estimatedScans = ((numDays - actualDay) * l.booksPerDay)
        if estimatedScans > 0 and len(l.books) > 0:

            if estimatedScans > len(l.books):
                numScans = len(l.books)
            else:
                numScans = estimatedScans

            booksToRemove = l.books[:numScans]
            librariesToScan += 1
            finalString += f"{l.libraryNumber} {numScans}\n{' '.join([str(x) for x in booksToRemove])}\n"
            # write_file(sys.argv[2], toWrite)
            
            for i in libraries:
                for j in booksToRemove:
                    try:
                        i.books.remove(j)
                    except ValueError:
                        pass
                i.fitness()
        else:
            actualDay -= l.signupDays
    
    write_file(sys.argv[2], f"{librariesToScan}\n" + finalString)

'''
output

Num librerias
Orden de las librerias
'''        

def read_file(filename):
    with open(filename, 'r') as f:
        line = f.readline()
        print(line)
        line = line.split(' ')

        global numBooks, numLibraries, numDays, libraries, books

        numBooks = int(line[0])
        numLibraries = int(line[1])
        numDays = int(line[2])

        line = f.readline()
        bookScores = line.split(' ')
        #añadimos books a array de libros
        for i in range(len(bookScores)):
            b = Book(int(bookScores[i]),i)
            books[i] = b

        line = f.readline()
        
        for i in range(numLibraries):
            actualLib = line.split(' ')
            l = Library(i, int(actualLib[0]), int(actualLib[1]), int(actualLib[2]))
            libraries.append(l)
            line = f.readline()
            lbooks = line.split(' ')
            for j in range(l.bookNumber):
                l.addBook(books[int(lbooks[j])])
            line = f.readline()        

def write_file(filename, data):
    with open(filename, 'a') as f:
        f.write(data + '\n')

if __name__ == '__main__':
    main()