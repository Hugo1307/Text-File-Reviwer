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
#Variáveis Globais
#---------------------------------------------

optionsList = ['1', '2', '3', '4']
wordInfo = Word('', 0, [], set(), set(), set())
filePath = ''

#---------------------------------------------
#Funções
#---------------------------------------------

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

def menu():
    print('')
    print('Option List:')
    print('1) List all words in file')
    print('2) Summary')
    print('3) Search for word in file (by word)')
    print('4) Search for word in file (by position)', end='\n \n')

    wordInfo.word = ''
    wordInfo.count = 0
    wordInfo.lines = []
    wordInfo.precedents = set()
    wordInfo.successors = set()
    wordInfo.similiarWords = set()

    menuOption = input('Select a number: ')
    while menuOption not in optionsList:
        menuOption = input('Select a number: ')

    if menuOption == '1':

        printAllWords(listAllWords(filePath))

    elif menuOption == '2':
        printMainSummary(mostUsedWords())

    elif menuOption == '3':
        wordToSearch = input('Enter Word: ')
        while not wordToSearch:
            wordToSearch = input('Enter Word: ')

        searchWord(wordToSearch.lower())
        printSearchWord()
    
    elif menuOption == '4':
        lineToSearch = input('Enter Line: ')
        while not lineToSearch.isnumeric():
            lineToSearch = input('Enter Line: ')

        posToSearch = input('Enter Position: ')
        while not posToSearch.isnumeric():
            posToSearch = input('Enter Position: ')

        searchWordByPos(int(lineToSearch), int(posToSearch))

def getToMenu():
    dialogOption = input('Get back to the menu? [Y/N] ')
    while dialogOption not in ['Y', 'N', 'y', 'n', 'yes', 'no']:
        dialogOption = input('Get back to the menu? [Y/N] ')

    if dialogOption == 'Y' or dialogOption == 'y' or dialogOption == 'yes':
        menu()
    else:
        quit()

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

    print()

    getToMenu()

def findResemblance(word, filePath):
    wordList = [element[0] for element in listAllWords(filePath) if len(element[0]) >= len(word)]

    for i in wordList:
        if word in i:
            wordInfo.similiarWords.add(i)

def searchWord(word):
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

    getToMenu()

def searchWordByPos(line, position):
    with open(filePath) as f:
        
        linesList = f.readlines()
        currentLine = linesList[line].strip().split(' ')

        if not linesList[line].strip():
            print()
            print('These line is empty.', end='\n \n')
            getToMenu()
            return

        if line > documentStats()[0]:
            print()
            print('These line is out of range.', end='\n \n')
            getToMenu()
            return
        
        if position >= len(currentLine):
            print()
            print('Position out of range.', end='\n \n')
            getToMenu()
            return

        for wordIndex in range(len(currentLine)):
            if wordIndex == position:
               searchWord(currentLine[wordIndex].translate(str.maketrans('', '', string.punctuation)))
               printSearchWord()


def mostUsedWords():
    wordsList = listAllWords(filePath)

    wordsListByOcurrences = sorted(wordsList, key=lambda x: x[1], reverse=True)

    return wordsListByOcurrences[0:5]

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
    print('Used words (no repetitions):', len(listAllWords(filePath)))
    print('Total characters:', documentStats()[2])
    print('Total spaces:', documentStats()[3], end='\n \n')

    getToMenu()

#-------------------------------------------------- 
#Função Main
#--------------------------------------------------

def main():
    print('-------------------------------------------------')
    print('{:^50}'.format('WordSearcher Advanced'))
    print('-------------------------------------------------')

    global filePath

    filePath = input('Enter file path: ')
    while not os.path.isfile(filePath):
        filePath = input('Enter file path: ')

    #Menu
    menu()

main()
