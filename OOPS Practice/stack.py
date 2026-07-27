class Stack:

    def __init__(self, stack=None):
        if stack is None:
            self.stack = []
        else:
            self.stack = stack

    def push(self, element):
        self.stack.append(element)

    def top(self):
        return self.stack[-1]

    def pop(self):
        return self.stack.pop()

    def __repr__(self):
        return str(self.stack)