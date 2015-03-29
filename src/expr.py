import re
import enum
import operator

class Parser:
    maxLevel = 2
    ops = {'+' : (0,  True,     operator.add),
           '-' : (0,  True,     operator.sub),
           '*' : (1,  True,     operator.mul),
           '/' : (1,  True, operator.truediv),
           '%' : (1,  True,     operator.mod),
           '^' : (2, False,     operator.pow)}

    def __init__(self, s):
        self.s = s
        self.l = re.compile('\w+|\d+|[-+*/%^]').findall(s) + ['\0']
        self.i = 0
        self.x = self.l[0]

    def isLevel(self, lv):
        op = self.x
        return (op in self.ops) and (self.ops[op][0] == lv)

    def next(self):
        self.i += 1
        self.x = self.l[self.i]
        return self.l[self.i - 1]

    def parseOperator(self, lv):
        if lv > self.maxLevel:
            return self.parseTerm()
        e = self.parseOperator(lv + 1)
        while self.isLevel(lv):
            op = self.next()
            if self.ops[op][1]:
                e = (self.ops[op][2], [e, self.parseOperator(lv + 1)])
            else:
                e = (self.ops[op][2], [e, self.parseOperator(lv)])
                break
        return e

    def parseTerm(self):
        if self.x == '(':
            self.next()
            r = self.parseOperator(0)
            self.next()
            return r
        elif self.x == '+':
            self.next()
            return self.parseTerm()
        elif self.x == '-':
            self.next()
            return (operator.neg, [self.parseTerm()])
        elif self.x.isdigit():
            return int(self.next())
        else:
            return self.next()

def evm(e, m):
    def ev(e):
        if type(e) is int:
            return e
        return e[0](*map(ev, e[1]))
    return ev(e)

def evsm(s, m):
    return evm(Parser(s).parseOperator(0), m)

def evs(s):
    return evsm(s, {})

print(evs("2+2"))
