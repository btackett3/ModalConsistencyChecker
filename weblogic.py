# Brian Tackett
# Started: 11/4/2017
# Modal Logic (S5) Calculator

#This program tells you whether a set of formalized sentences of modal logic are consistent
#There are several helper functions used in processing the sentences

#Changes a string in Polish (prefix) notation to a more conventional (infix) notation
#Calls these functions:  infix

def unpolish(string):
    index = 0
    copy = ''
    while index < len(string):
        a = string[index]
        if a == "K":
            a = "&"
        elif a == "N":
            a = "~"
        elif a == "A":
            a = "V"
        elif a == "C":
            a = ">"
        elif a == "M":
            a = "P"
        elif a == "L":
            a = "N"
        copy = copy + a
        index = index + 1
    copy = infix(copy)
    return copy

#Converts a string from prefix to infix notation
#Calls: infix

def infix(copy):
    index = 0
    answer = ''
    if len(copy) == 1:
        return copy
    while index < len(copy):
        c = copy[index]
        if c == "&" or c == "V":
            need = 1
            jump = 1
            while need > 0:
                if copy[index + jump].islower():
                    need = need - 1
                    if need > 0:
                        jump = jump + 1
                elif copy[index + jump] == "&" or copy[index + jump] == "V":
                    need = need + 1
                    jump = jump + 1
                else:
                    jump = jump + 1
            left = copy[index+1:index+jump+1]
            right = copy[index+jump+1:]
            answer = answer + "(" + infix(left) + c + infix(right) + ")"
            return answer
        else:
            answer = answer + c
            index = index + 1
    return answer

#Changes a string from infix to prefix notation
#Calls: makeprefix, findmajor

def makeprefix(string):
    if string == '':
        return ''

    #find the major connective
    major = findmajor(string)
    
    #print("Major is")
    #print(major)

    #make the left polish
    left = ''
    if major > 0:
        left = makeprefix(string[:major])
        
    #print("Left is")
    #print(left)

    #make the right polish
    right = ''
    if major < len(string):
        right = makeprefix(string[major + 1:])

    #print("Right is")
    #print(right)

    #major + left + right
    answer = string[major] + left + right
    return answer

#Converts a string into Polish notation
#Calls: makeprefix

def makepolish(string):
    answer = makeprefix(string)
    index = 0
    
    #convert symbols
    copy = ''
    while index < len(answer):
        a = answer[index]
        if a == "&":
            a = "K"
        elif a == "~":
            a = "N"
        elif a == "V":
            a = "A"
        elif a == ">":
            a = "C"
        elif a == "P":
            a = "M"
        elif a == "N":
            a = "L"
        copy = copy + a
        index = index + 1

    #get rid of parentheses
    polish = ''
    for l in copy:
        if l == "(" or l == ")":
            pass
        else:
            polish = polish + l
    return polish

#Finds the major connective of a formula

def findmajor(string):
    major = 0
    depth = 0
    index = 0
    
    while index < len(string):
        b = string[index]
        if b == "(":
            depth = depth + 1
        elif b == ")":
            depth = depth -1
        elif depth == 0:
            if b == "&" or b == "V" or b == ">":
                major = index
        index = index + 1
    return major

# Check to see if all the worlds are empty

def empty(worlds):
    answer = True
    for a in worlds:
        if (a != []):
            answer = False
    return answer


# clear double negations

def clearDN(string):
    cleared = False
    while (not cleared):
        cleared = True
        i = 0
        while (i < len(string)):
            if string[i] == "N" and string[i + 1] == "N":
                if (i == 0):
                    string = string[2:]
                else:
                    string = string[:i] + string[i + 2:]
                cleared = False
            if string[i] == 'C':
                string = string[:i] + "AN" + string[i:]
            i = i + 1
    return string


# collapse modal formulas; LLp is equivalent to Lp in S5; MLp is equivalent to Lp; MMp is equivalent to Mp

def collapse(string):
    cleared = False
    while (not cleared):
        cleared = True
        i = 0
        b = len(string)
        while (i < b):
            # in S5, Necessarily Necessarily collapses to Necessarily
            if (string[i] == "L" and string[i + 1] == "L"):
                string = string[:i] + string[i + 1:]
                i = 0
                b = len(string)
            # in S5, Possibly Necessarily collapses to Necessarily; Possibly Possibly collapses to Possibly
            elif (string[i] == "M"):
                if (string[i + 1] == "M" or string[i + 1] == "L"):
                    string = string[:i] + string[i + 1:]
                    i = 0
                    b = len(string)
            i = i + 1
    return string

# Pushes negations through to the right of modal operators
# Not Necessarily is equivalent to Possibly Not
# Not Possibly is equivalent to Necessarily Not

def pushthrough(string):
    i = 0
    while (i < len(string)):
        if (string[i] == "N" and string[i + 1] == "L"):
            string = string[:i] + "MN" + string[i + 2:]
            i = 0
        elif (string[i] == "N" and string[i + 1] == "M"):
            string = string[:i] + "LN" + string[i + 2:]
            i = 0
        i = i + 1
    return string

# Pushes through and collapses until all negations are fartherst right and all redundant modal operators are gone
# Calls: pushthrough, collapse, tidy

def tidy(string):
    copy = ""
    for a in string:
        copy = copy + a
    string = pushthrough(string)
    if (not copy == string):
        return tidy(string)

    copy = ""
    for a in string:
        copy = copy + a
    string = collapse(string)
    if (not copy == string):
        return tidy(string)
    return string

# Check whether a string is a well-formed formula

def wellformed(string):
    index = 0
    need = 1

    if len(string) == 1 and string.islower():
        return 0
    if len(string) == 1 and string.isupper():
        return -1

    #check whether it is well-formed
    while (index < len(string)):
        a = string[index]
        if need == 0:
            return -1
        elif (a == "A" or a == "K" or a == "C" or a == "E"):
            index = index + 1
            need = need + 1
        elif (a.isupper()):
            if (not a == "N" and not a == "L" and not a == "M"):
                return -1
            else:
                index = index + 1
        elif (a.islower()):
            need = need - 1
            index = index + 1
        else:
            index = index + 1
    if need > 0:
        return - 1
    return index

# Split a string, based on major connective
# Calls: wellformed

def parse(string):
    if len(string) == 1 and string.islower():
        return 0
    if "A" not in string and "K" not in string and "C" not in string and "E" not in string:
        return len(string)

    '''
    To handle things like    'NAMNANpqAMNpLq' ...
    After the first splitter, find the next smallest segment that is a wff
    '''

    #find the first splitter

    need = 1
    index = 0
    while need > 0:
        if string[index] == "A" or string[index] == "K" or string[index] == "C" or string[index] == "E":
            index = index + 1
            need = need - 1
        else:
            index = index + 1
    splitter = index
    end = splitter + 1

    #test each proceeding segment of the string, until you find a wff

    while(end < len(string)):
        if wellformed(string[splitter:end]) > -1:
            return end
        else:
            end = end + 1
    return -1


# Check that formulas in an array are all well-formed formulas (have the correct syntax)
# Calls: wellformed

def wff(array):
    i = 0
    while (i < len(array)):
        if (wellformed(array[i]) < 0):
            return False
        i = i + 1
    return True


# Check to see if all the members of an array have been fully broken down

def simple(array):
    i = 0
    while (i < len(array)):
        a = array[i]
        if (len(a) > 1):
            if ("A" in a[1:] or "K" in a[1:] or "N" in a[1:] or "M" in a[1:] or "L" in a[1:]):
                return False
        i = i + 1
    return True


# For each atomic x in an array, adds "x or not x" to the array

def addatomics(array):
    atomics = []
    necessities = []
    for a in array:
        for b in a:
            if (b.islower()):
                atomics.append(b)
    for c in atomics:
        disjunct = "AN" + c + c
        array.append(disjunct)
        necessities.append(disjunct)
    return [array, necessities]


# Removes all closed branches

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
        # check each negated element for its positive
        for string in model:
            if (string.startswith('N')):
                if (model.count(string[1:]) > 0):
                    closed.append(index)
        index = index + 1

    # check to make sure no worlds are impossible
    index = 0
    for worldclass in worlds:
        for world in worldclass:
            for string in world:
                if (string.startswith('N')):
                    if (world.count(string[1:]) > 0):
                        closed.append(index)
        index = index + 1

    i = 0
    while (i < len(models)):
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

# Remove branches that contain worlds that are inconsistent with each other

def closemodals(array, modals, done, necessities):
    copy = []
    copymodals = []
    index = 0
    closed = []
    copynec = []

    for a in modals:
        for c in a:
            for b in c:
                if (b.startswith('N')):
                    if (c.count(b[1:]) > 0):
                        closed.append(index)
        index = index + 1
    i = 0
    while (i < len(array)):
        if i in closed:
            i = i + 1
        else:
            copy.append(array[i])
            copymodals.append(modals[i])
            copynec.append(necessities[i])
            i = i + 1
    return [copy, copymodals, done, copynec]


# Remove duplicates from everything, removes models that are the same as others but in a different order

def cleanall(model, worlds, necessities):
    model = clean(model)
    for world in worlds:
        world = clean(world)
    necessities = clean(necessities)

    for branch in model:
        branch.sort()
    for worldclass in worlds:
        for world in worldclass:
            world.sort()
        worldclass = removedupes(worldclass)
    for n in necessities:
        n.sort()

    copies = []

    index = 0

    while (index < len(model)):
        j = index + 1
        while (j < len(model)):
            if (model[index] == model[j]):
                if (worlds[index] == worlds[j]):
                    if (necessities[index] == necessities[j]):
                        copies.append(index)
            j = j + 1
        index = index + 1

    sparse = []
    i = 0
    while (i < len(model)):
        if i in copies:
            i = i + 1
        else:
            sparse.append(model[i])
            i = i + 1
    model = sparse

    sparse = []
    i = 0
    while (i < len(worlds)):
        if i in copies:
            i = i + 1
        else:
            sparse.append(worlds[i])
            i = i + 1
    worlds = sparse

    sparse = []
    i = 0
    while (i < len(necessities)):
        if i in copies:
            i = i + 1
        else:
            sparse.append(necessities[i])
            i = i + 1
    necessities = sparse

    return (model, worlds, necessities)


# For an array of arrays, remove duplicates from each array in the larger array

def clean(array):
    i = 0
    while (i < len(array)):
        array[i] = removedupes(array[i])
        i = i + 1
    return array


# Removes duplicates

def removedupes(array):
    copy = []
    i = 0
    while (i < len(array)):
        if array[i] in copy:
            i = i + 1
        elif array[i] == []:
            i = i + 1
        else:
            copy.append(array[i])
    return copy


#Convert C to AN, i.e. "if p then q" to "not p or q"

def changeC(string):
    index = 0
    while index < len(string):
        if string[index] == 'C':
            string = string[:index] + "AN" + string[index+1:]
            index = 0
        else:
            index = index + 1
    return string

# Initialize

def initialize(array):
    formulas = array
    a = 0
    while (a < len(formulas)):
        formulas[a] = changeC(formulas[a])
        formulas[a] = clearDN(formulas[a])
        formulas[a] = tidy(formulas[a])
        formulas[a] = clearDN(formulas[a])
        a = a + 1
    atomized = addatomics(formulas)
    formulas = atomized[0]
    necessities = atomized[1]
    formulas = removedupes(formulas)
    necessities = removedupes(necessities)

    branches = [[]]
    modals = [[[]]]

    return [formulas, branches, modals, necessities]


# process formulas

def processFormulas(formulas, branches, modals, necessities):
    # Loop through the formulas, simplifying each in turn

    f = 0
    while (f < len(formulas)):
        current = formulas[f]
        
        # And/Conjunction
        if (current.startswith('K')):
            split = parse(current)
            for i in branches:
                i.append(current[1:split])
                i.append(current[split:])

        # Basic Not
        if (current.startswith('N')):
            if (current[1].islower()):
                for i in branches:
                    i.append(current)
            elif (current[1] == 'A'):
                split = parse(current)
                for i in branches:
                    i.append("N" + current[2:split])
                    i.append("N" + current[split:])
            elif (current[1] == 'K'):
                split = parse(current)
                copies = []
                for i in branches:
                    j = i[:]
                    i.append("N" + current[2:split])
                    j.append("N" + current[split:])
                    copies.append(j)
                branches.extend(copies)

        # Or
        if (current.startswith('A')):
            split = parse(current)
            copies = []
            for i in branches:
                j = i[:]
                i.append(current[1:split])
                j.append(current[split:])
                copies.append(j)
            branches.extend(copies)

        # Atomic, Necessarily, and Possibly all get passed to branches unchanegd
        if (current.islower() or current.startswith('L') or current.startswith('M')):
            for i in branches:
                i.append(current)
        f = f + 1

    modals = [[[]]] * len(branches)
    nec = necessities
    necessities = [necessities]
    p = 1
    while (p < len(branches)):
        necessities = necessities + [nec]
        p = p + 1

    i = 0

    return [branches, modals, True, necessities]


# Break down each branch to atomics and modals

def processBranches(branches, modals, done, necessities):
    open = removeclosed(branches, modals, done, necessities)
    branches = open[0]
    modals = open[1]
    necessities = open[3]
    
    branches = clean(branches)

    done = True
    if not branches:
        return [branches, modals, done, necessities]
    needed = 1
    while (needed > 0):
        for c in branches:
            needed = len(c)
            for d in c:
                # And - add both conjuncts to the branch
                if (d.startswith('K')):
                    done = False
                    split = parse(d)
                    c.append(d[1:split])
                    c.append(d[split:])
                    c.pop(c.index(d))
                    needed = len(c)

                # Or - make 2 copies of the branch, one with each disjunct
                elif (d.startswith('A')):
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

                # Not
                elif (d.startswith('N')):
                    if (d[1] == 'A'):
                        done = False
                        split = parse(d[1:])+1
                        c.append("N" + d[2:split])
                        c.append("N" + d[split:])
                        c.pop(c.index(d))
                        needed = len(c)

                    elif (d[1] == 'K'):
                        done = False
                        split = parse(d[1:])+1
                        right = []
                        for i in c:
                            right.append(i)
                        c.append("N" + d[2:split])
                        right.append("N" + d[split:])

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
                        # print(necessities)

                        needed = len(c)
                    else:
                        needed = needed - 1

                else:
                    needed = needed - 1

    open = removeclosed(branches, modals, done, necessities)

    branches = open[0]
    modals = open[1]
    necessities = open[3]

    for m in branches:
        if "L" in m or "M" in m:
            tidy(m)
    return [branches, modals, done, necessities]


# breaks down modals within a branch
def processPos(branches, modals, done, necessities):
    #print("Processing possibilities")
    done = True
    
    clean(branches)
    if not branches:
        return [branches, modals, done, necessities]

    # If modals is empty, make an array of the same length as branches
    if not modals:
        modals = [[]] * len(branches)

    if not necessities:
        necessities = [] * len(branches)

    # Possibly - For any leaf, add the possibilities to its list of possibilities
    # while(needed > 0):

    done = True
    index = 0

    finished = False

    while (not finished):

        branch = branches[index]
        finished = True

        for string in branch:

            # Possibly - For string in branch, put its possibility in its corresponding list of possibilities
            if (string.startswith("M")):
                finished = False
                done = False
                complete = False
                found = False

                # check if there is a world that satisifies it
                for world in modals[index]:
                    for b in world:
                        if (b == string[1:]):
                            found = True

                # if there is not already a world that satisfies it, create a world with that + the necessities

                if not found:
                    newworld = [string[1:]] + necessities[index]

                    if modals[index] == [[]]:
                        modals[index] = [newworld]

                    else:
                        modals[index].append(newworld)

                branch.pop(branch.index(string))
        if finished:
            index = index + 1
            if index < len(branches):
                finished = False

    branches = clean(branches)
    for a in modals:
        a = clean(a)
    necessities = clean(necessities)

    return [branches, modals, done, necessities]


# Necessarily - for any leaf, if it has Necessarily p, add p to its branch, and check for Possibly not p
# If Necessarily p clashes with Possibly not p, close the branch with a contradiction (z and Nz)

def processNec(branches, modals, done, necessities):
    #print("Processing necessities")

    done = True

    if not necessities:
        necessities = [[]] * len(modals)

    if branches:
        needed = 1
        while (needed > 0):
            for c in branches:
                needed = len(c)
                
                k = 0
                while (k < len(c)):
                    c[k] = tidy(c[k])
                    k = k + 1

                start = 0
                while (start < len(c)):
                    d = c[start]
                    d = tidy(d)

                    # For necessities, add them to the branch and the possibilities
                    if (d.startswith('L')):
                        done = False
                        c.append(d[1:])
                        c.pop(c.index(d))

                        f = necessities[branches.index(c)]
                        f.append(d[1:])

                        e = modals[branches.index(c)]
                        for p in e:
                            if p:
                                p.append(d[1:])

                        start = 0
                        needed = len(c)

                    else:
                        needed = needed - 1
                        start = start + 1

    modals = clean(modals)
    for a in modals:
        a = clean(a)
    necessities = clean(necessities)

    temp = closemodals(branches, modals, done, necessities)
    branches = temp[0]
    modals = temp[1]
    done = temp[2]
    necessities = temp[3]

    return (branches, modals, done, necessities)


# Simplify worlds - for each world, break down all the non-modal complexity

def simplifyworlds(branches, modals, done, necessities):

    open = removeclosed(branches, modals, done, necessities)
    branches = open[0]
    modals = open[1]
    necessities = open[3]

    branches = clean(branches)

    done = True
    if not branches:
        return [branches, modals, done, necessities]

    index = 0
    string = 0

    index = 0
    fin = False
    while not fin:

        fin = True
        a = 0
        modallength = len(modals)
        while a < modallength:
            b = 0
            worldclass = modals[a]
            worldclasslength = len(worldclass)

            while b < worldclasslength:
                c = 0
                world = worldclass[b]
                fork = False

                worldlength = len(world)
                while c < worldlength:
                    formula = world[c]

                    # And - add both conjuncts to the world
                    if (formula.startswith('K')):
                        done = False
                        split = parse(formula)
                        world.append(formula[1:split])
                        world.append(formula[split:])
                        world.pop(c)
                        worldlength = worldlength + 1
                        fin = False
                        c = 0

                    # Or - if there is a branch in a world, create a new branch and copy over the actual world and necessities - add one disjunct+world to that and one disjunct+world to current.
                    elif (formula.startswith('A')):

                        done = False
                        split = parse(formula)
                        fork = True

                        # make a copy of the worldclass, except for the current world

                        newworldclass = []
                        for w in worldclass:
                            newworldclass.append(w[:])
                        newworldclass.pop(b)

                        # create a new world
                        right = []
                        for f in world:
                            if f != formula:
                                right.append(f[:])

                        # split the disjuncts between current and new world

                        right.append(formula[split:])
                        world.append(formula[1:split])
                        world.pop(c)

                        # Copy the branch and necessities

                        copybranch = branches[a]
                        copynec = necessities[a]
                        branches.append(copybranch)
                        necessities.append(copynec)

                        # Add the new world to the new worldclass

                        newworldclass.append(right[:])

                        # Add the new worldclass to the set of worldclasses

                        modals.append(newworldclass)
                        modallength = modallength + 1

                        fin = False
                        c = 0

                    # Not
                    elif (formula.startswith('N')):

                        if (formula[1] == 'A'):
                            done = False
                            split = parse(formula[1:])+1
                            world.append("N" + formula[2:split])
                            world.append("N" + formula[split:])
                            world.pop(c)
                            fin = False
                            c = 0

                        elif (formula[1] == 'K'):

                            done = False
                            fork = True
                            split = parse(formula[1:])+1

                            # make a copy of the worldclass, except for the current world
                            newworldclass = []
                            for w in worldclass:
                                newworldclass.append(w[:])
                            newworldclass.pop(b)

                            # create a new world
                            right = []
                            for f in world:
                                if f != formula:
                                    right.append(f[:])

                            # split the disjuncts between current and new world

                            world.append("N" + formula[2:split])
                            right.append("N" + formula[split:])
                            right.pop(c)
                            world.pop(c)


                            # Copy the branch and necessities

                            copybranch = branches[a]
                            copynec = necessities[a]
                            branches.append(copybranch)
                            necessities.append(copynec)

                            # Add the new world to the new worldclass

                            newworldclass.append(right[:])

                            # Add the new worldclass to the set of worldclasses

                            modals.append(newworldclass)
                            modallength = modallength + 1

                            fin = False
                            c = 0
                    c = c + 1
                b = b + 1
            a = a + 1

    open = removeclosed(branches, modals, done, necessities)

    branches = open[0]
    modals = open[1]
    necessities = open[3]

    for m in branches:
        if "L" in m or "M" in m:
            tidy(m)
    return [branches, modals, done, necessities]

'''
Change return parameters and eliminate this function.  Just use removeclosed, instead.
'''

# check each branch to see whether one is open (tree is consistent)
def check(array, modals, done, necessities):
    result = removeclosed(array, modals, True, necessities)
    model = result[0]
    modals = result[1]
    necessities = result[3]
    return [model, modals, necessities]

# Test Function - Tells you whether a set is consistent

def testshell(array):
    '''
    print("\nStarting Formulas:")
    print(array)
    '''
    '''
    if (not wff(array)):
        print("It is False that the set contains all wffs\n")
        return
    '''

    val = testing(array)
    if (val[0] == [] or val == None):
        print("No open leaves")
        print("The set is inconsistent")
        return []
    else:
        model = val[0]
        worlds = val[1]
        nec = val[2]

        print("Consistent/Invalid")
        print(model[0])
        print(worlds[0])
        print(nec[0])

        return [model, worlds, nec]


def testing(array):
    if not array:
        return None

    print(array)
    model = []
    if (not wff(array)):
        print("It is False that the set contains all well-formed formulas\n")
        return

    case = initialize(array)
    #print("Initialized")
    #print(case)

    case = processFormulas(case[0], case[1], case[2], case[3])

    nonmodal = False
    pos = False
    nec = False

    done = nonmodal and pos and nec

    '''
    Start a loop here.
    '''

    complete = False
    while (not complete):

        # break down all the original branches
        complete = True
        didstuff = False
        done = False
        while not done:
            didstuff = True

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
            necessities = result[2]
        model = clean(model)

        # break down all the worlds that still contain non-modal connectives

        done = False
        while not done:
            done = True
            index = 0
            if (empty(worlds)):
                pass
            else:
                case = simplifyworlds(model, worlds, done, necessities)
                
                model = case[0]
                worlds = case[1]
                done = done and case[2]
                complete = complete and done
                necessities = case[3]
                
        result = check(model, worlds, True, necessities)
        model = result[0]
        worlds = result[1]
        necessities = result[2]
        model = clean(model)

        # break down worlds that still contain M

        done = False
        
        while not done:
            done = True
            index = 0

            while (index < len(worlds)):
                worldclass = worlds[index]

                for world in worldclass:
                    for string in world:
                        if (string.startswith("M")):
                            done = False
                            complete = False
                            found = False
                            # check if there is a world that satisifies it
                            for a in worldclass:
                                for b in a:
                                    if (b == string[1:]):
                                        found = True

                            # if not, create a world with that + the necessities

                            if not found:
                                newworld = [string[1:]] + necessities[index]
                                worldclass.append(newworld)

                            world.pop(world.index(string))
                worlds[index] = worldclass
                index = index + 1

        result = check(model, worlds, True, necessities)
        model = result[0]
        worlds = result[1]
        necessities = result[2]

        # break down worlds that still contain L

        done = False

        while not done:

            done = True
            index = 0

            while (index < len(worlds)):
                worldclass = worlds[index]

                for world in worldclass:
                    for string in world:

                        # For Necessities in the list of Possibilities, add them to each world in their own worldclass, their corresponding branch, and their corresponding list of necessities.
                        if (string.startswith("L")):
                            done = False
                            complete = False

                            # Add it to each world in its worldclass
                            for w in worldclass:
                                w.append(string[1:])

                            # Add it to the branch
                            model[index].append(string[1:])

                            # Add it to the list of necessities
                            necessities[index] = necessities[index] + [string[1:]]

                            # Remove the operator from the original string
                            world.pop(world.index(string))
                worlds[index] = worldclass
                index = index + 1

        result = check(model, worlds, True, necessities)
        model = result[0]
        worlds = result[1]
        necessities = result[2]
        model = clean(model)

        squeaky = cleanall(model, worlds, necessities)
        model = squeaky[0]
        worlds = squeaky[1]
        necessities = squeaky[2]

        cut = removeclosed(model, worlds, done, necessities)
        model = cut[0]
        worlds = cut[1]
        done = cut[2]
        necessities = cut[3]

    # Check for inconsistencies.  If a model contains an inconsistency, throw it, its worlds, and its necessities out.  If a world contains an inconsistency, throw its worldclass, its model, and its necessities out.

        '''
        All models and all worlds need to only contain atomics.  If not, loop.

        '''

        i = 0
        j = 0
        while i < len(model):
            while j < len(model[i]):
                model[i][j] = clearDN(model[i][j])
                j = j + 1
            i = i + 1

        i = 0
        j = 0
        k = 0
        while i < len(worlds):
            while j < len(worlds[i]):
                while k < len(worlds[i][j]):
                    worlds[i][j][k] = clearDN(worlds[i][j][k])
                    k = k + 1
                j = j + 1
            i = i + 1

        print("Complete is " + str(complete))
        for w in model:
            for m in w:
                if "L" in m or "K" in m or "A" in m or "L" in m or "C" in m:
                    complete = False

        for w in worlds:
            for a in w:
                for m in a:
                    if "L" in m or "K" in m or "A" in m or "L" in m or "C" in m:
                        complete = False

        case = [model, worlds, True, necessities]

    '''
    End the loop here.
    '''

    return [model, worlds, necessities]
