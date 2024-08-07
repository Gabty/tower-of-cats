class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    def __init__(self):
        self.head = None
    
    def insert(self, data):
        if self.head == None:
            self.head = Node(data)
            return
        current = self.head
        while current.next != None:
            current = current.next
        
        current.next = Node(data)
    
    def get(self):
        if self.head == None:
            return
        if self.head.next == None:
            data = self.head.data
            self.head = None
            return data
        current = self.head
        while current.next.next != None:
            current = current.next
        
        data = current.next.data
        current.next = current.next.next
        return data
    
    def popleft(self):
        if self.head == None:
            return

        data = self.head.data
        self.head = self.head.next
        return data
    
    def show(self):
        if self.head == None:
            return
        string = ''
        current = self.head
        while current != None:
            string += str(current.data)+'->'
            current = current.next
        return string

    def getIndex(self, data):
        if self.head == None:
            return

        current = self.head
        i=0
        while current and current.data != data:
            current = current.next
            i+=1
        if current is None: raise IndexError("Out of bounds")
        return i

    def get_by_index(self, index):
        if index < 0 or index >= len(self):
            raise IndexError("Index out of bounds")
        current = self.head
        for _ in range(index):
            current = current.next
        return current.data

    def index(self, index):
        if self.head == None:
            return

        current = self.head
        i=0
        while i != index and current:
            current = current.next
            i+=1
        if current == None: raise IndexError("Not found")

        return current.data
    def copy(self):
        if self.head == None:
            return
        new_stack = Stack()
        current = self.head
        while current:
            new_stack.insert(current.data)
            current = current.next
        return new_stack
    
    def getLast(self):
        if self.head == None:
            return
        current = self.head
        if current.next == None:
            return current.data
        
        while current.next:
            current = current.next
        
        return current.data
    
    def __eq__(self, other):
        if not isinstance(other, Stack):
            return False
        if self.head == None and other.head == None:
            return True
        current = self.head
        other_current = other.head
        while current and other_current:
            if current.data != other_current.data:
                return False
            current = current.next
            other_current = other_current.next
        return current == None and other_current == None
    
    def __str__(self):
        if self.head == None:
            return 'None'
        return self.show()

    def __bool__(self):
        if self.head:
            return True
        return False
    
    def __iter__(self):
        if self.head == None:
            return
        
        current = self.head
        while current:
            yield current.data
            current = current.next
    
    def __len__(self):
        i = 0
        current = self.head
        while current:
            current = current.next
            i+=1
        
        return i
    
    def inverse(self):
        if self.head == None:
            return
        
        beta = Stack()
        current = self.head
        while current:
            beta.insert(current.data)
            current = current.next
        while beta:
            yield beta.get()
        

if __name__ == '__main__':
    a = Stack()

    a.insert(5)
    a.insert(3)
    a.insert(7)
    print(a.getLast())