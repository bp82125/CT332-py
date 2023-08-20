class Stack:
    def __init__(self, items=None):
        self.items = items if items is not None else []

    def isEmpty(self):
        return len(self.items) == 0

    def push(self, item):
        return Stack(self.items + [item])

    def pop(self):
        if self.isEmpty():
            raise ValueError("Stack is empty")
        return Stack(self.items[:-1])

    def size(self):
        return len(self.items)

    def peek(self):
        if self.isEmpty():
            raise ValueError("Stack is empty")
        return self.items[-1]

    def inStack(self, item):
        return item in self.items

    def pushAll(self, items: list):
        return Stack(self.items + items)


