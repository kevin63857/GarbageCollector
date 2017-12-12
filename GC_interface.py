#This is an abstract class for your garbage collector

#Manager has the following fields...
# heap_size -> how big is the heap
# data -> array of ints with size of heap_size
# active_roots -> array of ints listing the active root pointers

#data should be treated in 4 byte chunks
# data can only have Nodes in it.
# the first and second words are the first node's data
# the third and fourth words are the first node's pointers
# the fifth and sixth words are the second node's data...
# -1 denotes a null pointer

class GarbageCollector:
    def __init__(self):
        pass
    # Here is where garbage collection happens.  This method will be called every time that a new node is being allocated
    # This method should return a pointer to an available node if there is an available node
    # If all nodes are active, it should raise an OverflowError procing a heap overflow
    def allocate(self,data,active_roots):
        raise NotImplementedError("This method is to be implemented by subclasses.")
