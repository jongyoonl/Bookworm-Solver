"""
This module implements the Tree class. A Tree really represents a single node,
which contains all relevant data: the character, the string, its parent node, 
the boolean which indicates whether the current string is a word, its children,
and each of its children's chars. 
"""
class Tree:

    def __init__(self, char, string, parent, isword):
        """
        The initializer for the Tree class. char, string, parent, isword should 
        all be immutable, while children and childchars can change. The input
        is not sanity-checked. 
        """
        self.char = char
        self.string = string
        self.parent = parent
        self.isword = isword
        self.children = []
        self.childchars = []

    def addChild(self, child):
        """Adds a child and its character to its parent's properties. """
        self.children.append(child)
        self.childchars.append(child.char)

    def getValues(self):
        """Returns all the relevant properties of the Tree. """
        return self.char, self.string, self.parent, self.isword

    def getChild(self, index):
        """Getter method for a child by its order in the array. """
        return self.children[index]

    def getChildChars(self):
        """Getter method for the array containing children's characters. """
        return self.childchars

    def getChildByChar(self, char):
        """Gets a child by its character. """
        childchars = self.getChildChars()

        if char == "qu":

            tree = None
            newchars = None

            for i in range(len(childchars)):
                if "q" == childchars[i]:
                    tree = self.getChild(i)
                    newchars = tree.getChildChars()

            for j in range(len(newchars)):
                if "u" == newchars[j]:
                    return tree.getChild(j)

        else:

            for i in range(len(childchars)):
                if char == childchars[i]:
                    return self.getChild(i)

        return None