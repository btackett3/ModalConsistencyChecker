#Brian Tackett
#Started: 11/4/2017
#Modal Logic (S5) Calculator
        
#Operator Codes
        #Not N
        #Or A
        #And K
        #Possibly M
        #Necessarily L


'''

For Necessities in the list of Possibilities, add them to each world in their own worldclass, their corresponding branch, and their corresponding list of necessities



'''
        

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


#Crashes all the worldclasses in the range of worlds

def crashall(worlds):
        copy = []
        for a in worlds:
                a = crash(a)
                copy.extend(a)
        return copy

#In a worldclass, if one world is a proper subset of another, get rid of that smaller world

def crash(worldclass):
        small = []
        copy = []
        index = 0
        while(index < len(worldclass)):
                other = 0
                while(other < len(worldclass)):
                        if(index != other):
                                subset = True
                                for string in worldclass[index]:
                                      if string not in worldclass[other]:
                                              subset = False
                                              break
                                if subset:
                                      small.append(index)
                        other = other + 1
                index = index + 1

        i = 0
        while(i < len(worldclass)):
                if i in small:
                        i = i + 1
                else:
                        copy.append(worldclass[i])
                        i = i + 1
        return [copy]        
                                       

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
                elif(a.isupper()):
                        if(not a =="N" and not a == "L" and not a == "M"):
                                return -1
                        else:
                                index = index + 1
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

#For each atomic x in an array, adds "x or not x" to the array

def addatomics(array):
        atomics = []
        for a in array:
                for b in a:
                        if(b.islower()):
                                atomics.append(b)
        for c in atomics:
                disjunct = "AN" + c + c
                array.append(disjunct)
        return

#Removes all closed branches

def removeclosed(array, modals, done, necessities):

        print(array)
        print(modals)
        print(necessities)

        copy = []
        copymodals = []
        copynec = []
        index = 0
        closed = []
        for a in array:
        #check each negated element for its positive
                for b in a:
                        if(b.startswith('N')):
                                if(a.count(b[1:]) > 0):
                                        closed.append(index)
                index = index + 1
        i = 0
        while(i < len(array)):
                if i in closed:
                        i = i + 1
                else:
                        copy.append(array[i])
                        copymodals.append(modals[i])
                        copynec.append(necessities[i])
                        i = i + 1
        return [copy, copymodals, done, copynec]

def closemodals(array, modals, done, necessities):
        copy = []
        copymodals = []
        index = 0
        closed = []
        copynec = []

        for a in modals:
                for c in a:
                        for b in c:
                                if(b.startswith('N')):
                                        if(c.count(b[1:]) > 0):
                                                closed.append(index)
                index = index + 1
        i = 0
        while(i < len(array)):
                if i in closed:
                        i = i + 1
                else:
                        copy.append(array[i])
                        copymodals.append(modals[i])
                        copynec.append(necessities[i])
                        i = i + 1
        return [copy, copymodals, done, copynec]

                

#Remove duplicates

def clean(array):
        i = 0
        while(i < len(array)):
              array[i] = removedupes(array[i])
              i = i + 1
        return array

#Removes duplicates

def removedupes(array):
        copy = []
        i = 0
        while(i < len(array)):
                if array[i] in copy:
                        i = i + 1
                elif array[i] == []:
                        i = i + 1
                else:
                        copy.append(array[i])
        return copy
                        
#Initialize

                
def initialize(array):
        formulas = array

        #print("Starting Formulas:")
        #print(formulas)
        a = 0
        while(a < len(formulas)):
                formulas[a] = clearDN(formulas[a])
                a  = a + 1
        addatomics(formulas)
        formulas = removedupes(formulas)

        branches = [[]]
        modals = [[[]]]
        necessities = [[]]

        return [formulas, branches, modals, necessities]

#process formulas                        
                        
def processFormulas(formulas, branches, modals, necessities):
        #Loop through the formulas, simplifying each in turn
        #print("Processing formulas")
        #print(formulas)
        f = 0
        while(f < len(formulas)):
                     
                current = formulas[f]
                                
                #And/Conjunction
                if(current.startswith('K')):
                        split = parse(current)
                        for i in branches:
                                i.append(current[1:split])
                                i.append(current[split:])

                #Basic Not
                if(current.startswith('N')):
                        if(current[1].islower()):
                                for i in branches:
                                        i.append(current)
                        elif(current[1] == 'A'):
                                split = parse(current)
                                for i in branches:
                                        i.append("N" + current[2:split])
                                        i.append("N" + current[split:])
                        elif(current[1] == 'K'):
                                split = parse(current)
                                copies = []
                                for i in branches:
                                        j = i[:]
                                        i.append("N" + current[2:split])
                                        j.append("N" + current[split:])
                                        copies.append(j)
                                branches.extend(copies)    
                                        

                #Or
                if(current.startswith('A')):
                        split = parse(current)
                        copies = []
                        for i in branches:
                                j = i[:]
                                i.append(current[1:split])
                                j.append(current[split:])
                                copies.append(j)
                        branches.extend(copies)

                #Atomic, Necessarily, and Possibly all get passed to branches unchanegd
                if(current.islower() or current.startswith('L') or current.startswith('M')):
                        for i in branches:
                                i.append(current)  
                f = f + 1

        #print("Branches")
        #print(branches)

        modals = [[[]]] * len(branches)
        necessities = [[]] * len(modals)
        
        #print("Modals")
        #print(modals)
        return [branches, modals, True, necessities]

                                
                        
#Break down each branch to atomics and modals
def processBranches(branches, modals, done, necessities):

        open = removeclosed(branches, modals, done, necessities)

        branches = open[0]
        modals = open[1]
        necessities = open[3]
        
        branches = clean(branches)

        '''
        
        print("Branches")
        print(branches)
        print("Modals")
        print(modals)
        '''

        done = True
        if not branches:
                return [branches, modals]
        needed = 1
        while(needed > 0):
                for c in branches:
                        #print("Branch")
                        #print(c)
                        needed = len(c)
                                
                        for d in c:

                                #print("String")
                                #print(d)

                                #And - add both conjuncts to the branch
                                if(d.startswith('K')):
                                        done = False
                                        split = parse(d)
                                        c.append(d[1:split])
                                        c.append(d[split:])
                                        c.pop(c.index(d))
                                        needed = len(c)

                                #Or - make 2 copies of the branch, one with each disjunct
                                elif(d.startswith('A')):
                                        done = False
                                        split = parse(d)
                                        right = []
                                        for i in c:
                                                right.append(i)
                                        
                                        c.append(d[1:split])
                                        right.append(d[split:])
                                        right.pop(c.index(d))
                                        c.pop(c.index(d))
                                        branches.append(right)
                                        
                                        rightmodals = []
                                        for a in modals[branches.index(c)]:
                                                rightmodals.append(a)
                                        modals.append(rightmodals)

                                        rightnec = []
                                        for a in necessities[branches.index(c)]:
                                                rightnec.append(a)
                                        necessities.append(rightnec)
                                        
                                        needed = len(c)

                                #Not
                                elif(d.startswith('N')):
                                        #print(d)
                                        if(d[1] == 'A'):
                                                done = False
                                                split = parse(d)
                                                c.append("N" + d[2:split])
                                                c.append("N" + d[split:])
                                                c.pop(c.index(d))
                                                needed = len(c)
     
                                        elif(d[1] == 'K'):
                                                #print(d)
                                                done = False
                                                split = parse(d)
                                                right = []
                                                for i in c:
                                                        right.append(i)
                                                c.append("N" + d[2:split])
                                                right.append("N" + d[split:])
 
                                                right.pop(c.index(d))
                                                c.pop(c.index(d))
                                                branches.append(right)
                                                #print(branches)


                                                rightmodals = []
                                                for a in modals[branches.index(c)]:
                                                        rightmodals.append(a)
                                                modals.append(rightmodals)

                                                rightnec = []
                                                for a in necessities:
                                                        rightnec.append(a)
                                                necessities.append(rightnec)
                                                
                                                needed = len(c)
                                        else:
                                                needed = needed - 1
                                                
                                else:
                                        needed = needed - 1
                                           

        open = removeclosed(branches, modals, done, necessities)
        #print(branches)

        branches = open[0]
        modals = open[1]
        necessities = open[3]
        #print(branches)

        for m in branches:
                if "L" in m or "M" in m:
                           tidy(m)
        return [branches, modals, done, necessities]

#breaks down modals
def processPos(branches, modals, done, necessities):

        '''
        print("Branches")
        print(branches)
        print("Possibilities")
        print(modals)
        '''

        done = True

        clean(branches)
        if not branches:
                return [branches, modals, done]

        #If modals is empty, make an array of the same length as branches
        if not modals:
                modals = [[]] * len(branches)

        #need one atomic
        needed = 1
                
        #Possibly - For any leaf, add the possibilities to its list of possibilities
        while(needed > 0):
                for c in branches:
                        needed = len(c)

                        start = 0
                        while(start < len(c)):
                                d = c[start]
                                d = tidy(d)

                                #Possibly - For leaf c, put its possibility in its corresponding list of possibilities
                                if(d.startswith('M')):
                                        done = False
                                        o = tidy(d[1:])
                                        print(modals[branches.index(c)])
                                        if modals[branches.index(c)] == [[]]:
                                                modals[branches.index(c)] = [[o]]
                                        else:
                                                modals[branches.index(c)].append([o])
                                                #necessities.append([])
                                        print(modals[branches.index(c)])
                                        
                                        c.pop(c.index(d))
                                        start = 0
                                        needed = len(c)
                                else:
                                        needed = needed - 1
                                        start = start + 1
        print("modals")
        print(modals)
        print("necessities")
        print(necessities)
 
        branches = clean(branches)
        for a in modals:
                a = clean(a)
        modals = crashall(modals)
        necessities = clean(necessities)

        return [branches, modals, done, necessities]

#Necessarily - for any leaf, if it has Necessarily p, add p to its branch, and check for Possibly not p
#If Necessarily p clashes with Possibly not p, close the branch with a contradiction (z and Nz)

def processNec(branches, modals, done, necessities):

              
        print("Branches")
        print(branches)
        print("Necessities - Modals")
        print(modals)
        

        done = True

        if not necessities:
                necessities = [[]] * len(modals)
        print("Necessities")
        print(necessities)
        
        needed = 1
        while(needed > 0):
                for c in branches:
                        needed = len(c)

                        k = 0
                        while(k < len(c)):
                                c[k] = tidy(c[k])
                                k = k + 1

                        start = 0
                        while(start < len(c)):
                                d = c[start]
                                d = tidy(d)

                                #For necessities, add them to the branch and the possibilities
                                if(d.startswith('L')):

                                        
                                        done = False
                                        c.append(d[1:])
                                        
                                                        
                                        c.pop(c.index(d))

                                        f = necessities[branches.index(c)]
                                        f.append(d[1:])

                                        e = modals[branches.index(c)]
                                              
                                        for p in e:
                                                p.append(d[1:])

                                        start = 0
                                        needed = len(c)                                         
                                                
                                else:
                                        needed = needed - 1
                                        start = start + 1

        #print(modals)

        modals = clean(modals)
        for a in modals:
                a = clean(a)
        modals = crashall(modals)
        necessities = clean(necessities)

        #print(modals)

        temp = closemodals(branches, modals, done, necessities)
        branches = temp[0]
        modals = temp[1]
        done = temp[2]
        necessities = temp[3]

        return(branches, modals, done, necessities)                                                            
                        
#check each branch to see whether one is open (tree is consistent)
def check(array, modals, done, necessities):             
        model = removeclosed(array, modals, True, necessities)
        model = model[0]
        if not model:
                return None
        else:
                return [model, modals, necessities]
                                                

#Test Function - Tells you whether a set is consistent

def testshell(array):
        print("\nStarting Formulas:")
        print(array)

        if(not wff(array)):
                print("It is False that the set contains all wffs\n")
                return

        
        val = testing(array)
        if(val == None):
                print("No open leaves")
                print("The set is inconsistent")
        else:
                model = val[0]
                worlds = val[1]
                nec = val[2]

                print("The formulas are consistent in each of these models. Each array is a model:")
                print(model)
                print("With these associated possibilities.")
                print(worlds)
                print("With these necessities over the world-classes")
                print(nec)
                
        
        
def testing(array):
        if not array:
                return None
        model = []
        if(not wff(array)):
                print("It is False that the set contains all well-formed formulas\n")
                return

        #print("Initializing")
        case = initialize(array)

        #print("Processing Formulas")
        case = processFormulas(case[0], case[1], case[2], case[3])

        #print("Case is")
        #print(case)

        nonmodal = False
        pos = False
        nec = False

        done = nonmodal and pos and nec

        #break down all the original branches

        while not done:

                #print("Processing Branches")
                case = processBranches(case[0], case[1], case[2], case[3])
                if not case[0]:
                        return None
                
                #print("Processing Pos")
                nonmodal = case[2]
                #print("Nonmodal Done?")
                #print(nonmodal)
                case = processPos(case[0], case[1], case[2], case[3])
                #print("Processing Nec")
                #print("Pos done?")
                pos = case[2]
                necessities = case[3]
                #print(pos)
                case = processNec(case[0], case[1], case[2], case[3])
                nec = case[2]

                necessities = case[3]
                #print("Nec Done?")
                #print(nec)
                done = nonmodal and pos and nec
       
        result = check(case[0], case[1], True, necessities)
        model = result[0]
        worlds = result[1]
        worlds = crashall(worlds)
        necessities = result[2]
        model = clean(model)

        #break down all the worlds that still contain non-modal connectives

        done = False

        while not done:

                done = True
                index = 0
                while(index < len(worlds)):
                        worldclass = worlds[index]
                        print("Worldclass is:")
                        print(worldclass)
                        temp = [[[]]] * len(worldclass)
                        t = [[]] * len(temp)
                        case = processBranches(worldclass, temp, True, t)
                        worldclass = case[0]
                        print("Worldclass has become:")
                        print(worldclass)
                        done = done and case[2]
                        worlds[index] = worldclass
                        index = index + 1

        #break down worlds that still contain M
        
        done = False

        while not done:

                done = True
                index = 0

                while(index < len(worlds)):
                        worldclass = worlds[index]

                        for world in worldclass:
                                for string in world:
                                        if(string.startswith("M")):
                                                done = False
                                                found = False
                                                #check if there is a world that satisifies it
                                                for a in worldclass:
                                                        for b in a:
                                                                if(b == string[1:]):
                                                                        found = True
                                                                        
                                                #if not, create a world with that + the necessities

                                                if not found:
                                                        newworld = [string[1:]] + necessities[index]
                                                        worldclass.append(newworld)
                                                        
                                                world.pop(world.index(string))
                        worlds[index] = worldclass
                        index = index + 1
               

        worlds = crashall(worlds)
        return [model, worlds, necessities]
                                
#Test Cases

fin = False


test = [[['p', 'Nq'], ['p'], ['p', 'Nq', 'Li']], [['p', 'Nq'], ['p'], ['p', 'Nq', 'Li']], [['p', 'Nq'], ['p'], ['p', 'Nq', 'Li']], [['p', 'Nq'], ['p'], ['p', 'Nq', 'Li']], [['p', 'Nq', 'i'], ['p', 'Nq', 'i', 'Li']], [['p', 'Nq', 'i'], ['p', 'Nq', 'i', 'Li']]]
print(test)
index = 0
test = crashall(test)
print(test)

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
                        iswff = False
                        while(not iswff):
                                a = input("Enter any formula in Polish notation.\nSymbols: A - or; K - and; N - not; M - Possibly; L - Necessarily; a through x - Atomic\nExample: p and (q or r) == KpAqr\n")
                                temp = [a]
                                iswff = wff(temp)
                                if(not iswff):
                                        print("SYNTAX ERROR: String entered is not a well-formed formula. Try again")
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

