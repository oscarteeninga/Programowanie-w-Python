import string

form = input()

var = string.ascii_letters
operators = "|&"
parents_open = "([{"
parents_close = ")]}"

p_o = [0, 0, 0]
p_c = [0, 0, 0]

def isVar(char):
    if char is None:
        return False
    elif (char in var):
        return True
    else:
        return False

def isElement(char):
    return isVar(char) or isOperator(char) or isParent(char)

def isOperator(char):
    if char is None:
        return False
    if (char in operators):
        return True
    else:
        return False
    
def checkParents():
    i = 0
    while (i < 3):
        if p_o[i] < p_c[i]: return False
        i = i + 1
    return True

def checkComp():
    i = 0
    while (i < 3):
        if p_o[i] != p_c[i]: return False
        i = i + 1
    return True

def whichParent(char):
    i = 0
    while(i < 3):
        if parents_open[i] == char:
            p_o[i] += 1
        elif parents_close[i] == char:
            p_c[i] += 1
        i = i + 1
    return checkParents()

def isParent(char):
    if char in parents_open:
        return True
    if char in parents_close:
        return True
    else:
         return False

def checkOperatorNeigberhood(position):
    if isOperator(form[position-1]):
        return False
    if isOperator(form[position+1]):
        return False
    else:
        return True

def checkVarNeigberhood(position):
    if position-1 < 0 and position+1 >= len(form):
        return True
    if position-1 < 0:
        return not(isVar(form[position+1]))
    if position+1 >= len(form): 
        return not(isVar(form[position-1]))
    else: return not(isVar(form[position-1]) or isVar(form[position+1]))

def check(form):
    correct = True
    i = 0
    while i < len(form) and correct:
        if isVar(form[i]): correct = checkVarNeigberhood(i)
        if isOperator(form[i]): correct = checkOperatorNeigberhood(i)
        if isParent(form[i]): correct = whichParent(form[i])
        if not(isElement(form[i])): correct = False
        i = i + 1
    correct = checkComp()
    return correct

print(check(form))
