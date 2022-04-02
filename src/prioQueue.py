# prioQueue.py
# Contains PriorityQueue class

class PriorityQueue:
    # Constructor
    def __init__(self, priority_function):
        self.queue = []
        self.func = priority_function
    
    # Check if PQ is empty
    def is_empty(self):
        return len(self.queue) == 0

    # Peek function
    def front(self):
        return self.queue[0]

    # Insert item with corresponding function; O(n)
    def push(self, item):
        pos = 0
        found = False

        while(not found and pos < len(self.queue)):
            if(self.func(item, self.queue[pos])):
                found = True
            else:
                pos+=1
        
        self.queue.insert(pos, item)

    # Remove front item; O(1)
    def pop(self):
        self.queue.pop(0)