import os
import string

#---------------------------------------------
#Classes
#---------------------------------------------
class Word:
    def __init__(self, word, count, lines, precedents, successors, similarWords):
        self.word = word
        self.count = count
        self.lines = lines
        self.precedents = precedents
        self.successors = successors
        self.similiarWords = similarWords

#---------------------------------------------
#Global Variables
#---------------------------------------------

optionsList = ['1', '2', '3']
wordInfo = Word('', 0, [], set(), set(), set())
filePath = '/home/hugo/Desktop/Python/text.txt'

#---------------------------------------------
#Functions
#---------------------------------------------

def menu():
    print('')
    print('Option List:')
    print('1) Search for word in file')
    print('2) List all words in file')
    print('3) Summary', end='\n \n')

    menuOption = input('Select a number: ')
    while menuOption not in optionsList:
        menuOption = input('Select a number: ')

    if menuOption == '1':

        wordToSearch = input('Enter Word: ')
        while not wordToSearch:
            wordToSearch = input('Enter Word: ')

        searchWord(wordToSearch.lower(), filePath)
        printSearchWord()

    elif menuOption == '2':
        printAllWords(listAllWords(filePath))

    elif menuOption == '3':
        printMainSummary(mostUsedWords())


def listAllWords(f):
    wordsDict = {}

    with open(f, 'r') as ficheiro:
        for linha in ficheiro:
            for palavra in linha.strip().split(' '):
                palavra = palavra.translate(str.maketrans('', '', string.punctuation))
                if palavra.lower() not in wordsDict.keys():
                    wordsDict[palavra.lower()] = 1
                else:
                    wordsDict[palavra.lower()] += 1
    
    wordsList = [(key, value) for key, value in wordsDict.items()]

    wordsList = sorted(wordsList, key=lambda x: x[0])

    return wordsList

def printAllWords(wordsList):

    print('Words:', end=' ')

    for item in wordsList:
        print('{}({})'.format(item[0], item[1]), end=', ')

    dialogOption = input('Get back to the menu? [Y/N] ')
    while dialogOption not in ['Y', 'N', 'y', 'n', 'yes', 'no']:
        dialogOption = input('Get back to the menu? [Y/N] ')

    if dialogOption == 'Y' or dialogOption == 'y' or dialogOption == 'yes':
        menu()
    else:
        quit()

def findResemblance(word, filePath):
    wordList = [element[0] for element in listAllWords(filePath) if len(element[0]) >= len(word)]

    for i in wordList:
        if word in i:
            wordInfo.similiarWords.add(i)

def searchWord(word, filePath):
    linhaNumber = 0

    with open(filePath, 'r') as f:
        for linha in f:
            linhaNumber += 1
            wordsInLine = linha.strip().split(' ')
            for palavraIndex in range(len(wordsInLine)):
                if wordsInLine[palavraIndex].lower() == word.lower():
                    wordInfo.word = word.lower()
                    wordInfo.count += 1
                    wordInfo.lines.append(linhaNumber)
                    if palavraIndex < len(wordsInLine) - 1:
                        wordInfo.successors.add(wordsInLine[palavraIndex+1].translate(str.maketrans('', '', string.punctuation)))
                    if palavraIndex > 0:
                        wordInfo.precedents.add(wordsInLine[palavraIndex-1].translate(str.maketrans('', '', string.punctuation)))

    findResemblance(word, filePath)

def printSearchWord():
    print('----------------------------------------------------------------------------------------------------')
    print('{:^100}'.format(wordInfo.word))
    print('----------------------------------------------------------------------------------------------------', end='\n \n')

    print('This word appears {} times. '.format(wordInfo.count), end='\n \n')
    print('Appears in lines: ', end='')
    for line in wordInfo.lines:
        print(line, end=', ')
    print('',end='\n \n')

    print('Is preceded by: ', end='')
    for word in wordInfo.precedents:
        print(word, end=', ')
    print('',end='\n \n')

    print('Is succeded by: ', end='')
    for word in wordInfo.successors:
        print(word, end=', ')
    print('',end='\n \n')

    print('Similiar words: ', end='')
    for word in wordInfo.similiarWords:
        print(word, end=', ')
    print('',end='\n \n')

    dialogOption = input('Get back to the menu? [Y/N] ')
    while dialogOption not in ['Y', 'N', 'y', 'n', 'yes', 'no']:
        dialogOption = input('Get back to the menu? [Y/N] ')

    if dialogOption == 'Y' or dialogOption == 'y' or dialogOption == 'yes':
        menu()
    else:
        quit()

def mostUsedWords():
    wordsList = listAllWords(filePath)

    wordsListByOcurrences = sorted(wordsList, key=lambda x: x[1], reverse=True)

    return wordsListByOcurrences[0:5]

def documentStats():
    totalLines = 0
    totalWords = 0
    totalChars = 0
    totalSpaces = 0
    with open(filePath, 'r') as f:
        for line in f:
            totalSpaces += line.count(' ')
            totalWords += len(line.strip().split(' '))
            totalLines += 1
            for word in line.strip().split(' '):
                totalChars += len(word)

    return [totalLines, totalWords, totalChars, totalSpaces]

def printMainSummary(mostUsedWords):
    print('----------------------------------------------------------------------------------------------------')
    print('{:^100}'.format('Summary'))
    print('----------------------------------------------------------------------------------------------------', end='\n \n')

    print('Most used words: ')
    print('1º "{}"({})'.format(mostUsedWords[0][0], mostUsedWords[0][1]))
    print('2º "{}"({})'.format(mostUsedWords[1][0], mostUsedWords[1][1]))
    print('3º "{}"({})'.format(mostUsedWords[2][0], mostUsedWords[2][1]))
    print('4º "{}"({})'.format(mostUsedWords[3][0], mostUsedWords[3][1]))
    print('5º "{}"({})'.format(mostUsedWords[4][0], mostUsedWords[4][1]), end='\n \n')

    print('Total lines:', documentStats()[0])
    print('Total words:', documentStats()[1])
    print('Total words (no repetitions):', len(listAllWords(filePath)))
    print('Total characters:', documentStats()[2])
    print('Total spaces:', documentStats()[3], end='\n \n')

    dialogOption = input('Get back to the menu? [Y/N] ')
    while dialogOption not in ['Y', 'N', 'y', 'n', 'yes', 'no']:
        dialogOption = input('Get back to the menu? [Y/N] ')

    if dialogOption == 'Y' or dialogOption == 'y' or dialogOption == 'yes':
        menu()
    else:
        quit()

#-------------------------------------------------- 
#Main Function
#--------------------------------------------------

def main():
    print('-------------------------------------------------')
    print('{:^50}'.format('WordSearcher Advanced'))
    print('-------------------------------------------------')
    #Menu
    menu()

main()
