from GC_interface import GarbageCollector
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

class GC_simple(GarbageCollector):
    def __init__(self):
        self.alloc_count=-1

    # This is the ideal garbade collector.  Every request for memory is fulfilled by just giving memory.
    # If your peak memory usage exceeds your heap size, you die (not really, you just heap overflow)
    def allocate(self,data,active_roots):
        self.alloc_count+=1
        return self.alloc_count*4
