"""
This module is used to create the Tree from the supplied dict file.
The result is then pickled for later use, to be loaded by the Bookworm
Solver module.
"""
import pickle, re, tree

dictpath = "words"
treepath = "tree"

def main():
    """
    This main method checks for any illegal words in the provided dict file,
    then creates the tree encapsulating the relations between each word. 
    """
    pruneBadWords(dictpath)
    createTree(dictpath, treepath)

def pruneBadWords(path):
    """
    Delete all the words that are not legal in a game of Bookworm.
    These words are those which have q's unfollowed by u's, or proper nouns. 
    """
    pattern = re.compile("[Qq][^u]")

    file = open(path, "r")
    words = file.readlines()
    file.close()

    file = open(path, "w")

    for word in words:
        word = word[:-1]
        if word.islower() and (word.isalpha()) and (re.search(pattern, word) == None) and (len(word) >= 3):
            file.write(word + "\n")

    file.close()

def createTree(pathin, pathout):
    """
    Calls its helper method to create the word tree. It is used to supply
    arguments and to process the results. 
    """
    file = open(pathin, "r")
    words = file.readlines()
    file.close()

    root = tree.Tree("", "", None, False)

    createTreeHelper(words, root)

    file = open(pathout, "wb")
    pickle.dump(root, file)
    file.close()

def createTreeHelper(words, root):
    """Upon reading a new word, this method compares it to the one that 
    immediately precedes it. If the new word is entirely contained within
    the old word, a subbranch is created under the latter's branch. 
    Otherwise, the method recursively searches for the part of the tree
    which does contain the new word. """
    prevnode = root

    for word in words:

        char, string, parent, isword = prevnode.getValues()

        while not isWordContained(string, word):

            prevnode = parent
            char, string, parent, isword = prevnode.getValues()

        for letter in word[len(string):len(word) - 2]:

            node = tree.Tree(letter, string + letter, prevnode, False)
            prevnode.addChild(node)
            prevnode = node
            char, string, parent, isword = prevnode.getValues()

        node = tree.Tree(word[-2], string + word[-2], prevnode, True)
        prevnode.addChild(node)
        prevnode = node

def compareWords(word0, word1):
    """Compares two words and returns the substring that is contained in both. """
    match = ""

    for index in range(len(word0)):
        if index >= len(word1) or word0[index] != word1[index]:
            return match
        else:
            match += word0[index]

    return match

def isWordContained(word0, word1):
    """Checks whether word0 is contained within word1. """
    return word0 == compareWords(word0, word1) 

if __name__ == "__main__":
    main()