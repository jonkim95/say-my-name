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


def get_wordbet_output(file_name = 'no_c.txt'):
    input_file = open(file_name, 'r')
    wordbet_list = []
    for line_entry in input_file:
        wordbet_list.append('\t' + line_entry)
    print(wordbet_list[:10])
    return wordbet_list

def get_name_input (file_name = 'name.txt'):
    input_file = open(file_name, 'r')
    name_list = []
    for line_entry in input_file:
        name_list.append(line_entry.strip())
    print(name_list[:10])
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
        if len(ipaList) > 10:
            return
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


        for key in self.indexToNameIPA: 
            if len(self.indexToNameIPA[key]) % 2 == 1: 
                continue
            for currentIndex in range(0, len(self.indexToNameIPA[key])):
                if currentIndex == 0:
                    if self.indexToNameIPA[key][currentIndex] == '': 
                        break
                    nameFile.write(self.indexToNameIPA[key][currentIndex] + '\n')
                elif currentIndex == 1: 
                    ipaFile.write(self.indexToNameIPA[key][currentIndex] + '\n')
                elif currentIndex == 2:
                    if self.indexToNameIPA[key][currentIndex] == '': 
                        break
                    nameFile.write(self.indexToNameIPA[key][currentIndex] + '\n')
                elif currentIndex == 3: 
                    ipaFile.write(self.indexToNameIPA[key][currentIndex] + '\n')




    def combineData(self):
        input1 = "name.txt"
        input2 = "ipa.txt"
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


    

def main():
    util = Util()
    util.processRawData('lastNameTrans')
    util.processRawData('lastNameLabel')
    util.processRawData('firstNameTrans')
    util.processRawData('firstNameLabel')
    util.printDataStructure()
    util.writeData()
    util.combineData()
    util.outputFile()


if __name__== "__main__":
    main()
