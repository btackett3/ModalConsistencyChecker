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

 When creating a world, make sure to add all necessities to it. FROM A MODEL BRANCH, OR FROM A WORLD

 When splitting a branch, make sure you are copying over modals and necessities

 Remove models that are duplicates of other models, but in a different order

 For worlds, add p or not p, for each atomic in the starting formulas

'''

#check to see if all the worlds are empty
def empty(worlds):
        answer = True
        for a in worlds:
                if(a != []):
                        answer = False
        return answer

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
                        if string[i] == 'C':
                                string = string[:i] + "AN" + string[i:]
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

def removeclosed(models, worlds, done, necessities):

        '''
        print(models)
        print(worlds)
        print(necessities)
        '''

        copy = []
        copyworlds = []
        copynec = []
        index = 0
        closed = []
        for model in models:
        #check each negated element for its positive
                for string in model:
                        if(string.startswith('N')):
                                if(model.count(string[1:]) > 0):
                                        closed.append(index)
                index = index + 1

        #check to make sure no worlds are impossible

        index = 0

        for worldclass in worlds:
                for world in worldclass:
                        for string in world:
                                if(string.startswith('N')):
                                        if(world.count(string[1:]) >0):
                                                closed.append(index)
                index = index + 1

                
        i = 0
        while(i < len(models)):
                if i in closed:
                        i = i + 1
                else:
                        copy.append(models[i])
                        copyworlds.append(worlds[i])
                        copynec.append(necessities[i])
                        i = i + 1

        '''
        print(copy)
        print(copyworlds)
        print(copynec)
        '''

        return [copy, copyworlds, done, copynec]

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


#Remove duplicates from everything

def cleanall(model, worlds, necessities):
        model = clean(model)
        for world in worlds:
                world = clean(world)
        necessities = clean(necessities)
        return(model, worlds, necessities)
      

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
                return [branches, modals, done, necessities]
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

#breaks down modals within a branch
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
                return [branches, modals, done, necessities]

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
                                        #print(modals[branches.index(c)])
                                        if modals[branches.index(c)] == [[]]:
                                                modals[branches.index(c)] = [[o]]
                                        else:
                                                modals[branches.index(c)].append([o])
                                                #necessities.append([])
                                        #print(modals[branches.index(c)])
                                        
                                        c.pop(c.index(d))
                                        start = 0
                                        needed = len(c)
                                else:
                                        needed = needed - 1
                                        start = start + 1
                                        '''
        print("modals")
        print(modals)
        print("necessities")
        print(necessities)
        '''
 
        branches = clean(branches)
        for a in modals:
                a = clean(a)
        modals = crashall(modals)
        necessities = clean(necessities)

        return [branches, modals, done, necessities]

#Necessarily - for any leaf, if it has Necessarily p, add p to its branch, and check for Possibly not p
#If Necessarily p clashes with Possibly not p, close the branch with a contradiction (z and Nz)

def processNec(branches, modals, done, necessities):

        '''
        print("Branches")
        print(branches)
        print("Necessities - Modals")
        print(modals)
        '''

        done = True

        if not necessities:
                necessities = [[]] * len(modals)
        #print("Necessities")
        #print(necessities)

       
                
        if branches:
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




#Simplify worlds - for each world, break down all the non-modal complexity

def simplifyworlds(branches, modals, done, necessities):

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
                return [branches, modals, done, necessities]
        needed = 1
        while(needed > 0):
                for worldclass in modals:
                        for world in worldclass:
                                needed = len(world)
                                
                                for d in world:

                                        #And - add both conjuncts to the world
                                        if(d.startswith('K')):
                                                done = False
                                                split = parse(d)
                                                world.append(d[1:split])
                                                world.append(d[split:])
                                                world.pop(world.index(d))
                                                needed = len(world)

                                        #Or - if there is a branch in a world, create a new branch and copy over the actual world and necessities - add one disjunct+world to that and one disjunct+world to current.
                                        elif(d.startswith('A')):
                                                done = False
                                                split = parse(d)

                                                #make a copy of the worldclass, except for the current world
                                                newworldclass = []
                                                for w in worldclass:
                                                        if w != world:
                                                                newworldclass.append(w)
                                                
                                                #create a new world
                                                right = []
                                                for formula in world:
                                                        right.append(formula)

                                                #split the disjuncts between current and new world
                                                world.append(d[1:split])
                                                right.append(d[split:])
                                                right.pop(world.index(d))
                                                world.pop(world.index(d))


                                                #Copy the branch and necessities 

                                                index = modals.index(worldclass)

                                                copybranch = branches[index]
                                                copynec = necessities[index]
                                                branches.append(copybranch)
                                                necessities.append(copynec)

                                                #Add the new world to the new worldclass

                                                newworldclass.append(right)

                                                #Add the new worldclass to the set of worldclasses

                                                modals.append(newworldclass)
                                                
                                                needed = len(world)

                                        #Not
                                        elif(d.startswith('N')):
                                                #print(d)
                                                if(d[1] == 'A'):
                                                        done = False
                                                        split = parse(d)
                                                        world.append("N" + d[2:split])
                                                        world.append("N" + d[split:])
                                                        world.pop(world.index(d))
                                                        needed = len(world)
             
                                                elif(d[1] == 'K'):

                                                        done = False
                                                        split = parse(d)

                                                        #make a copy of the worldclass, except for the current world
                                                        newworldclass = []
                                                        for w in worldclass:
                                                                if w != world:
                                                                        newworldclass.append(w)
                                                        
                                                        #create a new world
                                                        right = []
                                                        for formula in world:
                                                                right.append(formula)

                                                        #split the disjuncts between current and new world
                                                        world.append("N" + d[2:split])
                                                        right.append("N" + d[split:])
                                                        right.pop(world.index(d))
                                                        world.pop(world.index(d))


                                                        #Copy the branch and necessities 

                                                        index = modals.index(worldclass)

                                                        copybranch = branches[index]
                                                        copynec = necessities[index]
                                                        branches.append(copybranch)
                                                        necessities.append(copynec)

                                                        #Add the new world to the new worldclass

                                                        newworldclass.append(right)

                                                        #Add the new worldclass to the set of worldclasses

                                                        modals.append(newworldclass)
                                                        
                                                        needed = len(world)
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


'''
Change return parameters and eliminate this function.  Just use removeclosed, instead.
'''

#check each branch to see whether one is open (tree is consistent)
def check(array, modals, done, necessities):             
        result = removeclosed(array, modals, True, necessities)
        model = result[0]
        modals = result[1]
        necessities = result[3]
        return [model, modals, necessities]
                                                

#Test Function - Tells you whether a set is consistent

def testshell(array):
        print("\nStarting Formulas:")
        print(array)

        if(not wff(array)):
                print("It is False that the set contains all wffs\n")
                return

        
        val = testing(array)
        if(val[0] == [] or val == None):
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

        case = initialize(array)

        case = processFormulas(case[0], case[1], case[2], case[3])
        
        nonmodal = False
        pos = False
        nec = False

        done = nonmodal and pos and nec

        '''
        Start a loop here.
        '''

        complete = False
        while(not complete):

        #break down all the original branches
                complete = True
                didstuff = False
                while not done:
                        didstuff = True
                        #print("Processing Branches")
                        case = processBranches(case[0], case[1], case[2], case[3])

                        
                
                        nonmodal = case[2]

                        case = processPos(case[0], case[1], case[2], case[3])
                        

                        pos = case[2]
                        necessities = case[3]

                        case = processNec(case[0], case[1], case[2], case[3])
                        nec = case[2]
                        
                        necessities = case[3]

                        done = nonmodal and pos and nec
                        complete = done
       

                if didstuff:
                        result = check(case[0], case[1], True, necessities)
                        model = result[0]
                        worlds = result[1]
                        worlds = crashall(worlds)
                        necessities = result[2]
                model = clean(model)

                '''
                print("Model")
                print(model)
                print("Worlds")
                print(worlds)
                print("Necessities")
                print(necessities)
                '''

        #break down all the worlds that still contain non-modal connectives

                done = False

                while not done:

                        done = True
                        index = 0

                        if(empty(worlds)):
                                pass
                
                        else:
                                case = simplifyworlds(model, worlds, done, necessities)

                                model = case[0]
                                worlds = case[1]

                                done = done and case[2]
                                complete = complete and done
                                necessities = case[3]
                                        
                '''
                print("Model")
                print(model)
                print("Worlds")
                print(worlds)
                print("Necessities")
                print(necessities)
                '''

                result = check(model, worlds, True, necessities)
                model = result[0]
                worlds = result[1]
                worlds = crashall(worlds)
                necessities = result[2]
                model = clean(model)

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
                                                        complete = False
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

                '''
                print("Model")
                print(model)
                print("Worlds")
                print(worlds)
                print("Necessities")
                print(necessities)
                '''
                
                result = check(model, worlds, True, necessities)
                model = result[0]
                worlds = result[1]
                #worlds = crashall(worlds)
                necessities = result[2]
                #model = clean(model)
                
        
        #break down worlds that still contain L

        
                done = False

                while not done:

                        done = True
                        index = 0

                        while(index < len(worlds)):
                                worldclass = worlds[index]

                                for world in worldclass:
                                        for string in world:

                                        #For Necessities in the list of Possibilities, add them to each world in their own worldclass, their corresponding branch, and their corresponding list of necessities.
                                                if(string.startswith("L")):
                                                        done = False
                                                        complete = False

                                                #Add it to each world in its worldclass
                                                        for w in worldclass:   
                                                                w.append(string[1:])
                                                                        
                                                #Add it to the branch
                                                        model[index].append(string[1:])

                                                #Add it to the list of necessities
                                                        necessities[index] = necessities[index] + [string[1:]]

                                                #Remove the operator from the original string
                                                        world.pop(world.index(string))
                                worlds[index] = worldclass
                                index = index + 1
               

                worlds = crashall(worlds)
                '''
                print("Model")
                print(model)
                print("Worlds")
                print(worlds)
                print("Necessities")
                print(necessities)
                '''
                result = check(model, worlds, True, necessities)
                model = result[0]
                worlds = result[1]
                worlds = crashall(worlds)
                necessities = result[2]
                model = clean(model)

                
                squeaky = cleanall(model, worlds, necessities)
                model = squeaky[0]
                worlds = squeaky[1]
                necessities = squeaky[2]

                '''
                print("Model")
                print(model)
                print("Worlds")
                print(worlds)
                print("Necessities")
                print(necessities)
                '''
                
        
        #Check for inconsistencies.  If a model contains an inconsistency, throw it, its worlds, and its necessities out.  If a world contains an inconsistency, throw its worldclass, its model, and its necessities out.

        '''
        All models and all worlds need to only contain atomics.  If not, loop.
        
        End the loop here.
        '''
        
        return [model, worlds, necessities]
                                
#Test Cases

test = ["LALoLp", "Np"]
testshell(test)
print("Expected: Consistent")

fin = False

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
                
        else:
                fin = True

