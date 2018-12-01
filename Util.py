import collections
import math
import numpy as np
import os


'''
limitation with edge cases
- apostrophe 
'''


class Constant:
    def __init__(self):
        self.indexToLastName = 0
        self.indexToLastNameIPA = 1
        self.indexToFirstName = 2
        self.indexToFirstNameIPA = 3


def get_wordbet_output(file_name = 'output.csv'):
    input_file = open(file_name, 'r')
    wordbet_list = []
    for line_entry in input_file:
        wordbet_list.append('\t' + line_entry.lower())
    return wordbet_list

def get_name_input (file_name = 'input.csv'):
    input_file = open(file_name, 'r')
    name_list = []
    for line_entry in input_file:
        name_list.append(line_entry.strip().lower())
    return name_list

class Util (object):

    def __init__(self):
        self.trans_spell_lname_DirName = '/Users/jaewoojang/Desktop/Fall 2018/cs221/project/say-my-name/Corpus/LDC2006S15/spelled_spoken/trans/spell_lname/'
        self.label_say_lname_DirName = '/Users/jaewoojang/Desktop/Fall 2018/cs221/project/say-my-name/Corpus/LDC2006S15/spelled_spoken/labels/say_lname/'
        self.trans_spell_fname_DirName = '/Users/jaewoojang/Desktop/Fall 2018/cs221/project/say-my-name/Corpus/LDC2006S15/spelled_spoken/trans/spell_fname_pause/'
        self.label_say_fname_DirName ='/Users/jaewoojang/Desktop/Fall 2018/cs221/project/say-my-name/Corpus/LDC2006S15/spelled_spoken/labels/say_fname/'
        self.indexToNameIPA = collections.defaultdict(list)


    def parseNameTransFile(self, fileName): 
        tempIndex = fileName.split('.')[0]
        fileIndex = tempIndex.split('call')[1]
        inputFile = open(fileName, 'r')
        for lineEntry in inputFile: 
            lineEntry = lineEntry.strip()
            nameLetters = lineEntry.split(' ')
            filteredName = [ch for ch in nameLetters if len(ch) == 1]

            assembledName = ''.join(filteredName)
            if assembledName == '': 
                break
            # if assembledName == 'brack': 
            #     print (fileIndex)

            self.indexToNameIPA[fileIndex].append(assembledName)

    def parseNameLabelFile(self, fileName):
        tempIndex = fileName.split('.')[0]
        fileIndex = tempIndex.split('call')[1]
        counter = 0
        if 'ptlola' in fileName: 
            return
        inputFile = open(fileName, 'r')
        ipaList = []
        for lineEntry in inputFile: 
            counter += 1
            if counter < 3: continue
            if '.' in lineEntry: continue
            lineEntry = lineEntry.strip()
            ipaValue = lineEntry.split(' ')[2]
            ipaList.append(ipaValue)
        if fileIndex not in self.indexToNameIPA or len(self.indexToNameIPA[fileIndex])%2 == 0:
            return
        # if len(ipaList) > 10:
        #     return
        self.indexToNameIPA[fileIndex].append(''.join(ipaList))


    def selectDirName (self, directory):
        dirName = ''
        if directory == 'lastNameTrans':
            dirName = self.trans_spell_lname_DirName
        elif directory == 'lastNameLabel':
            dirName = self.label_say_lname_DirName
        elif directory == 'firstNameTrans':
            dirName = self.trans_spell_fname_DirName
        elif directory == 'firstNameLabel':
            dirName = self.label_say_fname_DirName
        return dirName



    def processRawData (self, directory):
        dirName = self.selectDirName(directory)

        def recurseNameDirectories(dirName):
            for suffix in os.listdir(dirName):
                fileName = dirName + suffix
                if os.path.isdir(fileName):
                    recurseNameDirectories(fileName + '/')
                else: 
                    if 'trans' in dirName:
                        self.parseNameTransFile(fileName) 
                    elif 'labels' in dirName:
                        self.parseNameLabelFile(fileName)

        recurseNameDirectories(dirName)

    def printDataStructure (self):
        print(self.indexToNameIPA)
    
    def getNameToIPAMap(self): 
        return self.indexToNameIPA

    def writeData(self):
        
        nameFile = open('name.txt', 'w') 
        ipaFile = open('ipa.txt', 'w')
        repeating = set()

        for key in self.indexToNameIPA: 
            if len(self.indexToNameIPA[key]) % 2 == 1: 
                continue
            repeat = False
            for currentIndex in range(0, len(self.indexToNameIPA[key])):
                
                if currentIndex == 0:
                    if self.indexToNameIPA[key][currentIndex] == '': 
                        continue
                    if len(self.indexToNameIPA[key][1]) > 16:
                        continue
                    if self.indexToNameIPA[key][currentIndex] in repeating:
                        repeat = True
                        continue
                    repeating.add(self.indexToNameIPA[key][currentIndex])
                    nameFile.write(self.indexToNameIPA[key][currentIndex] + '\n')
                elif currentIndex == 1: 
                    if len(self.indexToNameIPA[key][1]) > 16: 
                        continue
                    if repeat == True:
                        repeat = False
                        continue
                    ipaFile.write(self.indexToNameIPA[key][currentIndex] + '\n')
                elif currentIndex == 2:
                    if len(self.indexToNameIPA[key][3]) > 16: 
                        continue
                    if self.indexToNameIPA[key][currentIndex] == '': 
                        break
                    if self.indexToNameIPA[key][currentIndex] in repeating:
                        repeat = True
                        continue
                    repeating.add(self.indexToNameIPA[key][currentIndex])
                    nameFile.write(self.indexToNameIPA[key][currentIndex] + '\n')
                elif currentIndex == 3: 
                    if len(self.indexToNameIPA[key][3]) > 16: 
                        continue
                    if repeat == True:
                        repeat = False
                        continue
                    ipaFile.write(self.indexToNameIPA[key][currentIndex] + '\n')




    def combineData(self):
        input1 = "name.txt"
        input2 = "no_c.txt"
        outfile = "./combined.txt"

        f1 = []
        f2 = []

        with open(input1) as f:
            for line in f:
                f1.append(line.strip())

        with open(input2) as f:
            for line in f:
                f2.append(line.strip())

        with open(outfile, 'w') as f:
            for i in range(len(f1)):
                if i >= len(f2): break
                f.write(f1[i] + ' ' + f2[i] + '\n')


    def outputFile(self):
        nameFile = 'indexNameIPA.txt'

        with open(nameFile, 'w') as f:
            for i in range(0, len(self.indexToNameIPA)):
                if i >= len(self.indexToNameIPA): break
                listToPrint = [val for val in self.indexToNameIPA[i]]
                jointString = ''.join(listToPrint)
                f.write(jointString)

    def deleteOutput(self): 
        for key in self.indexToNameIPA: 
            if len(self.indexToNameIPA[key]) % 2 == 1: 
                continue
            finalIndex = len(self.indexToNameIPA[key]) - 1
            currentIndex = 1
            while currentIndex <= finalIndex: 
                wordLength = len(self.indexToNameIPA[key][currentIndex])
                if wordLength > 16: 
                    del self.indexToNameIPA[key][currentIndex-1]
                    del self.indexToNameIPA[key][currentIndex-1]
                    finalIndex-=2
                else:
                    currentIndex+=2 
            if len(self.indexToNameIPA[key]) == 0: 
                del self.indexToNameIPA[key]


    def cleanOutput(self): 
        input_f = "ipa.txt"
        outfile = "no_c.txt"

        f1 = []
        f2 = []

        with open(input_f) as f:
            for line in f:
                new_line = ''
                seen_c = False
                for ch in line.strip():
                    if not seen_c:
                        if ch == 'c':
                            seen_c = True
                        else:
                            new_line += ch
                    else:
                        seen_c = False
                f1.append(new_line)

        with open(outfile, 'w') as f:
            for i in range(len(f1)):
                #if i >= len(f2): break
                f.write(f1[i] + '\n')

def main():
    util = Util()
    util.processRawData('lastNameTrans')
    util.processRawData('lastNameLabel')
    util.processRawData('firstNameTrans')
    util.processRawData('firstNameLabel')
    # util.printDataStructure()
    # util.deleteOutput()
    util.writeData()
    # util.outputFile()
    util.cleanOutput()
    util.combineData()


if __name__== "__main__":
    main()
