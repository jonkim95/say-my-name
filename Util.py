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


class Util (object):

    def __init__(self):
        self.trans_spell_lname_DirName = '/Users/jaewoojang/Desktop/Fall 2018/cs221/project/Corpus/LDC2006S15/spelled_spoken/trans/spell_lname/'
        self.label_say_lname_DirName = '/Users/jaewoojang/Desktop/Fall 2018/cs221/project/Corpus/LDC2006S15/spelled_spoken/labels/say_lname/'
        self.trans_spell_fname_DirName = '/Users/jaewoojang/Desktop/Fall 2018/cs221/project/Corpus/LDC2006S15/spelled_spoken/trans/spell_fname_pause/'
        self.label_say_fname_DirName ='/Users/jaewoojang/Desktop/Fall 2018/cs221/project/Corpus/LDC2006S15/spelled_spoken/labels/say_fname/'
        self.indexToNameIPA = collections.defaultdict(list)

    def startState(self):
        return 0

    # Return set of actions possible from |state|.
    # You do not need to modify this function.
    # All logic for dealing with end states should be placed into the succAndProbReward function below.
    def actions(self, state):
        return ['Shoot']

    def parseNameTransFile(self, fileName): 
        tempIndex = fileName.split('.')[0]
        fileIndex = tempIndex.split('call')[1]
        inputFile = open(fileName, 'r')
        for lineEntry in inputFile: 
            lineEntry = lineEntry.strip()
            nameLetters = lineEntry.split(' ')
            filteredName = [ch for ch in nameLetters if len(ch) == 1]
            assembledName = ''.join(filteredName)
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
        
        self.indexToNameIPA[fileIndex].append(' '.join(ipaList))


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
    



def main():
    util = Util()
    util.processRawData('lastNameTrans')
    util.processRawData('lastNameLabel')
    util.processRawData('firstNameTrans')
    util.processRawData('firstNameLabel')
    util.printDataStructure()


if __name__== "__main__":
    main()
