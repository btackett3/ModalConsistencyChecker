#Brian Tackett
#Started: 11/4/2017
#Modal Logic (S5) Calculator
        
#Operator Codes
        #Not N
        #Or A
        #And K
        #Possibly M
        #Necessarily L
        

#clear double negations
def clearDN(string):
        cleared = False
        while(not cleared):
                cleared = True
                i = 0
                while(i < len(string)):
                        if string[i] == "N" and string[i + 1] == "N":
                                if(i == 0):
                                        string = string[2:]
                                else:
                                        string = string[:i] + string[i+2:]
                                cleared = False
                        i = i + 1
        return string

#collapse modal formulas; LLp is equivalent to Lp in S5; MLp is equivalent to Lp; MMp is equivalent to Mp
def collapse(string):
        cleared = False
        while(not cleared):
                cleared = True
                i = 0
                b = len(string)
                while(i < b):
                        #in S5, Necessarily Necessarily collapses to Necessarily
                        if(string[i] == "L" and string[i + 1] == "L"):
                                string = string[:i] + string[i+1:]
                                i = 0
                                b = len(string)
                        #in S5, Possibly Necessarily collapses to Necessarily; Possibly Possibly collapses to Possibly
                        elif(string[i] == "M"):
                                if(string[i+1] == "M" or string[i+1] == "L"):
                                        string = string[:i] + string[i+1:]
                                        i = 0
                                        b = len(string)
                        i = i + 1
        return string

#pushes negations through to the right of modal operators
def pushthrough(string):
        i = 0
        while(i < len(string)):
                if(string[i] == "N" and string[i+1] == "L"):
                        string = string[:i] + "LN" + string[i+2:]
                        i = 0
                elif(string[i] == "N" and string[i+1] == "M"):
                        string = string[:i] + "MN" + string[i+2:]
                        i = 0
                i = i + 1
        return string

#pushes through and collapses until tidy
def tidy(string):
        copy = ""
        for a in string:
                copy = copy + a
        string = pushthrough(string)
        if(not copy == string):
                return tidy(string)

        copy = ""
        for a in string:
                copy = copy + a        
        string = collapse(string)
        if(not copy == string):
                return tidy(string)
        return string
        
#Split a string, based on major connective
def parse(string):
        index = 0
        need = 1

        while(index < len(string)):
                a = string[index]
                if(a == "A" or a == "K" or a == "C" or a == "E"):
                        index = index + 1
                        need = need + 1
                elif(a.islower()):
                        need = need - 1
                        index = index + 1
                else:
                        index = index + 1
        #failure if not returned by now
        if(need == 0):
                index = index - 1
                while(string[index -1 ] == "N" or string[index - 1] == "L" or string[index-1] == "M"):
                        index = index - 1
                return index
        return -1

#Check that formulas are well-formed formulas (have the correct syntax)

def wff(array):
        i = 0
        while(i < len(array)):
                if(parse(array[i]) < 0):
                         return False
                i = i + 1
        return True

#Check to see if all the members of an array have been fully broken down

def simple(array):
        i = 0
        while(i < len(array)):
                a = array[i]
                if(len(a) > 1):
                        if("A" in a[1:] or "K" in a[1:] or "N" in a[1:] or "M" in a[1:] or "L" in a[1:]):
                                return False
                i = i + 1
        return True

#Storage
        
class Argument:
                
        def __init__(self, array, var, h):
                self.formulas = array
                self.branches = [[]]
                self.copy = [[]]
                self.var = var
                self.history = h
                #print("Starting Formulas:")
                #print(self.formulas)
                a = 0
                while(a < len(self.formulas)):
                        self.formulas[a] = clearDN(self.formulas[a])
                        a  = a + 1
                        

                        
        def processFormulas(self):
                #Loop through the formulas, simplifying each in turn
                f = 0
                while(f < len(self.formulas)):
                     
                        current = self.formulas[f]
                                
                        #And/Conjunction
                        if(current.startswith('K')):
                                split = parse(current)
                                for i in self.branches:
                                        i.append(current[1:split])
                                        i.append(current[split:])

                        #Basic Not
                        if(current.startswith('N')):
                                if(current[1].islower()):
                                        for i in self.branches:
                                                i.append(current)
                                elif(current[1] == 'A'):
                                        split = parse(current)
                                        for i in self.branches:
                                                i.append("N" + current[2:split])
                                                i.append("N" + current[split:])
                                elif(current[1] == 'K'):
                                        split = parse(current)
                                        copies = []
                                        for i in self.branches:
                                                j = i[:]
                                                i.append("N" + current[2:split])
                                                j.append("N" + current[split:])
                                                copies.append(j)
                                        self.branches.extend(copies)    
                                        

                        #Or
                        if(current.startswith('A')):
                                split = parse(current)
                                copies = []
                                for i in self.branches:
                                        j = i[:]
                                        i.append(current[1:split])
                                        j.append(current[split:])
                                        copies.append(j)
                                self.branches.extend(copies)

                        #Atomic, Necessarily, and Possibly all get passed to branches unchanegd
                        if(current.islower() or current.startswith('L') or current.startswith('M')):
                                for i in self.branches:
                                        i.append(current)  

                        f = f + 1
                        

                                
                        
        #Break down each branch to atomics and modals
        def processBranches(self):
                copy = []
                self.history = self.history + "Non-Modal Branching: \n"
                self.history = self.history + str(self.branches) + "\n"
                needed = 1
                while(needed > 0):
                        for c in self.branches:
                                needed = len(c)
                                
                                for d in c:

                                        #And
                                        if(d.startswith('K')):
                                                split = parse(d)
                                                c.append(d[1:split])
                                                c.append(d[split:])
                                                c.pop(c.index(d))
                                                needed = len(c)

                                        #Or
                                        if(d.startswith('A')):
                                                split = parse(d)
                                                copies = []
                                                for i in c:
                                                        j = i[:]
                                                        i.append(d[1:split])
                                                        j.append(d[split:])
                                                        copies.append(j)
                                                c.extend(copies)
                                                needed = len(c)
                                                
                                        else:
                                                needed = needed - 1
                                           
                self.history = self.history + "Leaves + Modals:\n"
                self.history = self.history + str(self.branches) + "\n"

                for m in self.branches:
                        if "L" in m or "M" in m:
                                tidy(m)
                

        #breaks down modals
        def processModals(self):
                #make an array of empty arrays for each leaf; these will hold possibilities for that leaf
                copy = [[]] * len(self.branches)
                needed = 1
                
                #Possibly - For any leaf, add the possibilities to its list of possibilities
                while(needed > 0):
                        for c in self.branches:
                                needed = len(c)
                                #print("C is:")
                                #print(c)

                                k = 0
                                while(k < len(c)):
                                        c[k] = tidy(c[k])
                                        k = k + 1
  
                                #print(c)

                                start = 0
                                while(start < len(c)):
                                        #print("D is:")
                                        d = c[start]
                                        #print(d)
                                        d = tidy(d)
                                        #print("D is:")
                                        #print(d)
                                        #Possibly - For leaf c, put its possibility in its corresponding list of possibilities
                                        if(d.startswith('M')):
                                                copy[self.branches.index(c)].append(tidy(d[1:]))
                                                #print("Copy is:")
                                                #print(copy)
                                                copy[self.branches.index(c)] = testing(copy[self.branches.index(c)], self.var, self.history)
                                                if(copy[self.branches.index(c)] == None):
                                                        copy[self.branches.index(c)] = []
                                                c.pop(c.index(d))
                                                start = 0
                                                needed = len(c)
                                        else:
                                                needed = needed - 1
                                                start = start + 1
                        #print(needed)

                self.history = self.history + "Leaves without Processed Possibilities:\n"
                self.history = self.history + str(self.branches)+ "\n"
                self.history = self.history + "Corresponding Possibilities\n"
                self.history = self.history + str(copy) + "\n"

                needed = 1

                #Necessarily - for any leaf, if it has Necessarily p, add p to its branch, and check for Possibly not p
                #If Necessarily p clashes with Possibly not p, close the branch with a contradiction (z and Nz)

                while(needed > 0):
                        for c in self.branches:
                                needed = len(c)

                                #print("A is")
                                #print(c)

                                k = 0
                                while(k < len(c)):
                                        c[k] = tidy(c[k])
                                        k = k + 1
  
                                #print(c)

                                start = 0
                                while(start < len(c)):

                                        #print("D is:")
                                        d = c[start]
                                        #print(d)
                                        d = tidy(d)
                                        #print("D is")
                                        #print(d)
                                        if(d.startswith('L')):
                             
                                                c.append(d[1:])
                                                complex = False
                                                if(len(d) > 0 and not d[1].islower()):
                                                        complex = True
                                                        
                                                c.pop(c.index(d))

                                                #Check the Necessity against all the Possibilities

                                                e = copy[self.branches.index(c)]
                                              
                                                for p in e:
           
                                                        if(testing([d[1:], p], self.var, self.history) == None):
                                                                c.append("z")
                                                                c.append("Nz")
                                                #If the Necessity modified a compound statement, check c again for consistency
                                                #If c is consistent, c will be the simplified model where c is consistent
                                                #otherwise, c is set to a contradiction
                                                if(complex):
                                                        c = testing(c, self.var, self.history)
                                                        if(c == None):
                                                                c = ["y", "Ny"]
                                                start = 0
                                                needed = len(c)
                                                        
                                                
                                        else:
                                                needed = needed - 1
                                                start = start + 1

                self.history = self.history + "Leaves after Necessities that conflict with Possibilities have been processed\n"
                self.history = self.history + str(self.branches) + "\n"
                                                        
                        
        #check each branch to see whether one is open (tree is consistent)
        #def check(self):        
                q = []
                for a in self.branches:
                        #check each negated element for its positive
                        open = True
                        for b in a:
                                if(b.startswith('N')):
                                        if(a.count(b[1:]) > 0):
                                                open = False
                        if(open):
                                self.history = self.history + "Leaf " + str(self.branches.index(a)) + " is open\n"
                                model = []
                                model.append(a)
                                q = copy[self.branches.index(a)]
                                ps = []
                                for t in q:
                                        ps.append("M" + t)
                                ps.extend(a)

                                if(self.var == "1"):
                                        print(self.history)
                                return ps
                if(self.var == "1"):
                        print(self.history)
                return None
                                                

#Test Function - Tells you whether a set is consistent

def testshell(array):
        print("\nStarting Formulas:")
        print(array)
        var = input("[1] Show Branching History [2] Skip to Results")
        if(not wff(array)):
                print("It is False that the set contains all wffs\n")
                return
        val = testing(array, var, "")
        if(val == None):
                print("No open leaves")
                print("The set is inconsistent")
        else:
                print("The formulas are consistent in a model where these are assigned True:")
                print(val)
        
        
def testing(array, var, history):
        model = []
        if(not wff(array)):
                print("It is False that the set contains all well-formed formulas\n")
                return
        case = Argument(array, var, history)
        case.processFormulas()
        case.processBranches()
        
        if(var == "1"):
                print(case.history)
        result = case.processModals()
        if(result == None):
                return result
        if(not simple(result)):
                for f in result:
                        if "L" in f or "M" in f:
                                tidy(f)
                result = testing(result, var, history)
        answer = []
        i = 0
        while(i < len(result)):
                if(not result[i] in answer):
                        answer.append(result[i])
                i = i + 1
        return answer
                                
#Test Cases

#print(collapse("KMpLNq"))
#print("Done Collapsing")
#print(tidy("KMpMNLq"))
#print("Done tidying")
#print(pushthrough("NLLa"))
#print(pushthrough("MaNMMa"))
#print(pushthrough("MaLNMLa"))


fin = False

print("This program takes arrays of formalized sentences and tells you whether they are consistent in Propositional Modal Logic (S5 Axiom System)")
print("Tableau (truth tree) style inference is used to check consistency.")
print("\t\t\tAuthor: Brian Tackett, University at Buffalo")
print("\t\t\tCoded in Python for UB Hackathon 2017")
print("Syntax: Formulas are in Polish (prefix) notation.\nSymbols: A - or; K - and; N - not; M - Possibly; L - Necessarily; a through x - Atomic\nExample: p and (q or r) == KpAqr\n")



while(not fin):
        var = input("\n[1] See non-modal sample tests [2] See modal tests [3] Enter custom tests [4] Exit: ")
        #Sample Nonmodal Tests
        if(var == "1"):
                test = ["a", "b"]
                testshell(test)
                print("Expected: Consistent")

                test = ["a", "Na"]
                testshell(test)
                print("Expected: Not Consistent")

                test = ["Ab"]
                testshell(test)
                print("Expected: Not WFF") 

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

        #Sample Modal Tests
        elif(var == "2"):

                
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
                print("[HINT]Since Modal Logic is not Truth Functional, p can be False while Possibly p is True!")
                
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
                print("Expected:  Pretty complicated, huh?  (Actually, it is expected to be consistent, after some pen and paper proof)")
                
        #User Inputted Tests
        elif(var == "3"):
                done = False
                test = []
                while(not done):
                        a = input("Enter any formula in Polish notation.\nSymbols: A - or; K - and; N - not; M - Possibly; L - Necessarily; a through x - Atomic\nExample: p and (q or r) == KpAqr\n")
                        test.append(a)
                        b = input("Check for consistency? [1] yes [2] no")
                        if(b == "1"):
                                testshell(test)
                        c = input("[a] Add more formulas [b] Clear formulas [c] Exit program:")
                        if(c == "b" or c == "B"):
                                while(len(test)>0):
                                        test.pop(0)
                        elif(c == "c" or c == "C"):
                                done = True
                                fin = True
        else:
                fin = True

