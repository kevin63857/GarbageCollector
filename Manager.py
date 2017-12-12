from ListNode import *

class Manager:
    def __init__(self, heap_size, garbage_collector):
        self.heap_size=heap_size
        self.data=[-1]*heap_size #really big array
        self.active_roots=[]
        self.allocs=0
        self.garbage_collector=garbage_collector

    def allocate(self):#only allocates linked list nodes
        self.allocs+=1
        return Node(self,self.garbage_collector.allocate(self.data,self.active_roots),is_alloc=True)

    def count_active_nodes(self):
        active_nodes=[]
        checked_nodes=[]
        nodes_to_check=[]
        nodes_to_check_location=0
        for i in self.active_roots:
            if i not in checked_nodes: #if i has not been checked, make sure it is in active_nodes and add both of its children to the to_check list
                if not i in active_nodes:
                    active_nodes.append(i)
                if not self.data[i+2]==-1 and self.data[i+2] not in checked_nodes:
                    if not self.data[i+2] in active_nodes:
                        active_nodes.append(self.data[i+2])
                    nodes_to_check.append(self.data[i+2])
                if not self.data[i+3]==-1 and self.data[i+3] not in checked_nodes:
                    if not self.data[i+3] in active_nodes:
                        active_nodes.append(self.data[i+3])
                    nodes_to_check.append(self.data[i+3])
                checked_nodes.append(i)
                while len(nodes_to_check)>0:
                    checking_node=nodes_to_check[0]
                    if not self.data[checking_node+2]==-1 and self.data[checking_node+2] not in checked_nodes:
                        if not self.data[checking_node+2] in active_nodes:
                            active_nodes.append(self.data[checking_node+2])
                        if self.data[checking_node+2] not in nodes_to_check:
                            nodes_to_check.append(self.data[checking_node+2])
                    if not self.data[checking_node+3]==-1 and self.data[checking_node+3] not in checked_nodes:
                        if not self.data[checking_node+3] in active_nodes:
                            active_nodes.append(self.data[checking_node+3])
                        if self.data[checking_node+3] not in nodes_to_check:
                            nodes_to_check.append(self.data[checking_node+3])
                    nodes_to_check.remove(checking_node)
                    checked_nodes.append(checking_node)
        return len(active_nodes)

    def register_root(self,root):
        self.active_roots.append(root)
        #print self.active_roots

    def deregister_root(self,location):
        self.active_roots.remove(location)

    def get_word(self, name, nth_word):
        return self.data[name+nth_word];

    def set_word(self, name, nth_word, new_val):
        self.data[name+nth_word]=new_val;
