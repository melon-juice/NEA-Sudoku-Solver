
class Stack:
    """ Stack class used to stack up attempts.
    If a conflict is found in main(), then the stack is popped to restore the previous commit"""

    def __init__(self):
        self.maxSize=1000
        self.s=[None]*self.maxSize
        self.tosp=-1 #initialised as empty
        self.size=0

    def isEmpty(self):
        if self.size==0:
            return True
        return False

    def isFull(self):
        if self.size>=self.maxSize:
            return True
        return False

    def push(self,data):
        if self.isFull:
            self.tosp+=1
            self.s[self.tosp]=data
            self.size+=1
        else:
            print("Stack full- cannot add anything")

    def pop(self):
        if not self.isEmpty:
            data=self.s[self.tosp]
            del(data)
            self.tosp-=1
            self.size-=1
            return data
        else:
            print("Stack empty- nothing to pop")

    def find_size(self):
        return self.size

    def peek(self):
        return self.s[self.tosp]
