from weblogic import testshell
from weblogic import parse

# Create your tests here.
# Test Cases


fin = False

while (not fin):
    var = input("\n[1] See non-modal sample tests [2] See modal tests [3] Unsolved [4] Parsing [5] Quit. Enter the number as a string, e.g. "1": ")
    # Sample Nonmodal Tests
    if (var == "1"):
        test = ["a", "b"]
        testshell(test)
        print("Expected: Consistent")

        test = ["a", "Na"]
        testshell(test)
        print("Expected: Not Consistent")

        test = ["KKcab", "ANNNbNf", "AKefNc"]
        testshell(test)
        print("Expected: Not Consistent")

        test = ["NKab", "NAab"]
        testshell(test)
        print("Expected: Consistent")

        test = ["Aab", "Na"]
        testshell(test)
        print("Expected: Consistent")

        test = ["Aab", "Na", "Nb"]
        testshell(test)
        print("Expected: Not Consistent")

        test = ['NCKpCpqq']
        testshell(test)
        print("Expected: Inconsistent")

        test = ['CKpCpqq']
        testshell(test)
        print("Expected: Consistent")

    # Sample Modal Tests
    elif (var == "2"):

        test = ["Ma"]
        testshell(test)
        print("Expected: Consistent")

        test = ["La", "b"]
        testshell(test)
        print("Expected: Consistent")

        test = ["La", "MNa"]
        testshell(test)
        print("Expected: Not Consistent")

        test = ["Ma", "Na"]
        testshell(test)
        print("Expected: Consistent")

        test = ["Mp", "Mq", "Np", "Nq", "LNKpq"]
        testshell(test)
        print("Expected: Consistent")

        test = ["ALpMq", "LNq", "Np"]
        testshell(test)
        print("Expected: Not Consistent")

        test = ['LKaMb', 'ANbNa']
        testshell(test)
        print("Expected: Consistent")

        test = ["LALoLp", "Np"]
        testshell(test)
        print("Expected: Consistent")

        test = ["LAMpLi", "KMpMNLq", "NKaMp"]
        testshell(test)
        print("Expected:  Consistent")

        test = ['Mp', 'MNp', 'LANpLp']
        testshell(test)
        print("Expected: Inconsistent")

        test = ['Mp', 'q']
        testshell(test)
        print("Expected: Consistent")

        test = ["NCLCpqCLpLq"]
        testshell(test)
        print("Expected: Inconsistent")

    elif var == "3":

        #needs work - infinite loop

        test = ['Mp', 'MLq', 'NLCpLq']
        testshell(test)


    elif var == "4":

        print("Parsing")
        print('NAMNANpqAMNpLq')
        print(parse('NAMNANpqAMNpLq'))
        print("Expected: 8")

    else:
        fin = True

