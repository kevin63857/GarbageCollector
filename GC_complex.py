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

class GC_complex(GarbageCollector):
    def __init__(self):
        self.alloc_count=-1

    # This is the ideal garbade collector.  Every request for memory is fulfilled by just giving memory.
    # If your peak memory usage exceeds your heap size, you die (not really, you just heap overflow)
    def allocate(self,data,active_roots):
        self.alloc_count+=1
        active_nodes=[]
        checked_nodes=[]
        nodes_to_check=[]
        nodes_to_check_location=0
        for i in active_roots:
            if i not in checked_nodes: #if i has not been checked, make sure it is in active_nodes and add both of its children to the to_check list
                if not i in active_nodes:
                    active_nodes.append(i)
                if not data[i+2]==-1 and data[i+2] not in checked_nodes:
                    if not data[i+2] in active_nodes:
                        active_nodes.append(data[i+2])
                    nodes_to_check.append(data[i+2])
                if not data[i+3]==-1 and data[i+3] not in checked_nodes:
                    if not data[i+3] in active_nodes:
                        active_nodes.append(data[i+3])
                    nodes_to_check.append(data[i+3])
                checked_nodes.append(i)
                while len(nodes_to_check)>0:
                    checking_node=nodes_to_check[0]
                    if not data[checking_node+2]==-1 and data[checking_node+2] not in checked_nodes:
                        if not data[checking_node+2] in active_nodes:
                            active_nodes.append(data[checking_node+2])
                        if data[checking_node+2] not in nodes_to_check:
                            nodes_to_check.append(data[checking_node+2])
                    if not data[checking_node+3]==-1 and data[checking_node+3] not in checked_nodes:
                        if not data[checking_node+3] in active_nodes:
                            active_nodes.append(data[checking_node+3])
                        if data[checking_node+3] not in nodes_to_check:
                            nodes_to_check.append(data[checking_node+3])
                    nodes_to_check.remove(checking_node)
                    checked_nodes.append(checking_node)
        #print active_nodes
        i=0
        to_ret=-1
        while i<len(data):
            if i not in active_nodes:
                to_ret=i
                for i2 in range(i,i+4):
                    data[i2]=-1
            i+=4
        #print to_ret
        return to_ret #This would indicate that every node is active and return a null pointer, aka heap overflow
