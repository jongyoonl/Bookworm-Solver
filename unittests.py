"""
The testing suite for the Bookworm Solver package. 
It checks the validity of each of the modules used to create the tree 
and to solve the board.
"""
import unittest, tree, pickle, sys
from wordtree_maker import *
from bookworm_solver import *

class TestTreeMethods(unittest.TestCase):
    """Tests the Tree creation and its getter methods."""
    t0 = tree.Tree("e", "fire", None, True)
    t1 = tree.Tree("t", "firet", t0, False)
    t2 = tree.Tree("b", "fireb", t0, False)
    t0.addChild(t1)
    t0.addChild(t2)

    s0 = tree.Tree("e", "e", None, False)
    s1 = tree.Tree("q", "eq", s0, False)
    s2 = tree.Tree("u", "equ", s1, False)
    s3 = tree.Tree("a", "equa", s2, False)
    s0.addChild(s1)
    s1.addChild(s2)
    s2.addChild(s3)
    
    def testGetValues(self):

        t0, t1, t2 , s0, s1, s2, s3 = self.getTrees()

        self.assertEqual(t0.getValues(), ("e", "fire", None, True))
        self.assertEqual(t1.getValues(), ("t", "firet", t0, False))
        self.assertEqual(t2.getValues(), ("b", "fireb", t0, False))

        self.assertEqual(s0.getValues(), ("e", "e", None, False))
        self.assertEqual(s1.getValues(), ("q", "eq", s0, False))
        self.assertEqual(s2.getValues(), ("u", "equ", s1, False))
        self.assertEqual(s3.getValues(), ("a", "equa", s2, False))

    def testGetChild(self):

        t0, t1, t2 , s0, s1, s2, s3 = self.getTrees()

        self.assertEqual(t0.getChild(0), t1)
        self.assertEqual(t0.getChild(1), t2)

        self.assertEqual(s0.getChild(0), s1)
        self.assertEqual(s1.getChild(0), s2)
        self.assertEqual(s2.getChild(0), s3)

    def testGetChildChars(self):

        t0, t1, t2 , s0, s1, s2, s3 = self.getTrees()

        self.assertEqual(t0.getChildChars(), ["t", "b"])
        self.assertEqual(t1.getChildChars(), [])
        self.assertEqual(t2.getChildChars(), [])

        self.assertEqual(s0.getChildChars(), ["q"])
        self.assertEqual(s1.getChildChars(), ["u"])
        self.assertEqual(s2.getChildChars(), ["a"])
        self.assertEqual(s3.getChildChars(), [])

    def testGetChildByChar(self): 

        t0, t1, t2 , s0, s1, s2, s3 = self.getTrees()

        self.assertEqual(t0.getChildByChar("t"), t1)
        self.assertEqual(t0.getChildByChar("b"), t2)
        self.assertEqual(t0.getChildByChar("k"), None)

        self.assertEqual(s0.getChildByChar("q"), s1)
        self.assertEqual(s0.getChildByChar("qu"), s2)
        self.assertEqual(s1.getChildByChar("u"), s2)
        self.assertEqual(s2.getChildByChar("a"), s3)

    def getTrees(self):

        return TestTreeMethods.t0, TestTreeMethods.t1, TestTreeMethods.t2,\
        TestTreeMethods.s0, TestTreeMethods.s1, TestTreeMethods.s2, TestTreeMethods.s3

class TestTreeMaker(unittest.TestCase):
    """Unit tests for the wordtree maker. """
    def testCompareWords(self):

        self.assertEqual(compareWords("", "hello"), "")
        self.assertEqual(compareWords("good", "goodbye"), "good")
        self.assertEqual(compareWords("good", "gorilla"), "go")
        self.assertEqual(compareWords("cinder", "tinder"), "")
        self.assertEqual(compareWords("aid", "plaid"), "")

    def testIsContained(self):

        self.assertTrue(isWordContained("", "hello"))
        self.assertTrue(isWordContained("good", "goodbye"))
        self.assertFalse(isWordContained("good", "gorilla"))
        self.assertFalse(isWordContained("cinder", "tinder"))
        self.assertFalse(isWordContained("aid", "plaid"))

    def testPruneWords(self):

        def checkAnswer(testpath, anspath):

            pruneBadWords(testpath)

            testfile = open(testpath, "r")
            testlines = testfile.readlines()
            testfile.close()

            ansfile = open(anspath, "r")
            anslines = ansfile.readlines()
            ansfile.close()

            for i in range(len(testlines)):
                if testlines[i] != anslines[i]:
                    return False

            return True

        testpath = "tests/uttest0"
        anspath = "tests/utanswer0"
        file = open(testpath, "r")
        original = file.readlines()
        file.close()

        self.assertTrue(checkAnswer(testpath, anspath))

        file = open(testpath, "w")
        for line in original:
            file.write(line)
        file.close()

    def testCreateTree(self):

        pathin = "tests/uttest1"
        pathout = "tests/utoutput1"

        createTree(pathin, pathout)

        ansfile = open(pathout, "rb")
        root = pickle.load(ansfile)
        ansfile.close()

        a = root.getChildByChar("a")
        b = root.getChildByChar("b")
        aa = a.getChildByChar("a")
        ab = a.getChildByChar("b")
        ac = a.getChildByChar("c")
        ba = b.getChildByChar("a")
        aar = aa.getChildByChar("r")
        aba = ab.getChildByChar("a")
        baa = ba.getChildByChar("a")
        aard = aar.getChildByChar("d")
        baal = baa.getChildByChar("l")

        self.assertEqual(root.getValues(), ("","", None, False))
        self.assertEqual(a.getValues(), ("a", "a", root, False))
        self.assertEqual(b.getValues(), ("b", "b", root, False))
        self.assertEqual(aa.getValues(), ("a", "aa", a, False))
        self.assertEqual(ab.getValues(), ("b", "ab", a, False))
        self.assertEqual(ac.getValues(), ("c", "ac", a, False))
        self.assertEqual(ba.getValues(), ("a", "ba", b, False))
        self.assertEqual(aar.getValues(), ("r", "aar", aa, False))
        self.assertEqual(aba.getValues(), ("a", "aba", ab, True))
        self.assertEqual(baa.getValues(), ("a", "baa", ba, True))
        self.assertEqual(aard.getValues(), ("d", "aard", aar, False))
        self.assertEqual(baal.getValues(), ("l", "baal", baa, True))

class TestSolver(unittest.TestCase):
    """Unit tests for the solver module. """
    def testReducer(self):

        self.assertEqual(reducer((1, 2, 3), (4, 5, 6)), (4, 5, 6))
        self.assertEqual(reducer((1, 2, 3), (1, 5, 6)), (1, 2, 3))

    def testGetSurroundingIndices(self):

        board = [["qu", "r", "s", "t"], ["u", "v", "w"], ["x", "y"]]
        self.assertEqual(list(getSurroundingIndices(board, (0, 0))), [(0, 1), (1, 0)])
        self.assertEqual(list(getSurroundingIndices(board, (0, 3))), [(0, 2), (1, 2)])
        self.assertEqual(list(getSurroundingIndices(board, (1, 1))), [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)])


if __name__ == '__main__':
    unittest.main()