class Manager:
    #the heap can only have Nodes in it.
    # the first and second words are the first node's data
    # the third and fourth words are the first node's pointers
    # the fifth and sixth words are the second node's data...
    # -1 denotes a null pointer
    def __init__(self, heap_size):
        self.heap_size=heap_size
        self.rba=[-1]*heap_size #really big array
        self.active_roots=[]
        self.allocs=0

    def allocate(self):#only allocates linked list nodes
        self.allocs+=1
        return Node(self,(self.allocs-1)*4,is_alloc=True)

    def count_active_nodes(self):
        active_nodes=[]
        checked_nodes=[]
        nodes_to_check=[]
        nodes_to_check_location=0
        for i in self.active_roots:
            if i not in checked_nodes: #if i has not been checked, make sure it is in active_nodes and add both of its children to the to_check list
                if not i in active_nodes:
                    active_nodes.append(i)
                if not self.rba[i+2]==-1 and self.rba[i+2] not in checked_nodes:
                    if not self.rba[i+2] in active_nodes:
                        active_nodes.append(self.rba[i+2])
                    nodes_to_check.append(self.rba[i+2])
                if not self.rba[i+3]==-1 and self.rba[i+3] not in checked_nodes:
                    if not self.rba[i+3] in active_nodes:
                        active_nodes.append(self.rba[i+3])
                    nodes_to_check.append(self.rba[i+3])
                checked_nodes.append(i)
                while len(nodes_to_check)>0:
                    checking_node=nodes_to_check[0]
                    if not self.rba[checking_node+2]==-1 and self.rba[checking_node+2] not in checked_nodes:
                        if not self.rba[checking_node+2] in active_nodes:
                            active_nodes.append(self.rba[checking_node+2])
                        if self.rba[checking_node+2] not in nodes_to_check:
                            nodes_to_check.append(self.rba[checking_node+2])
                    if not self.rba[checking_node+3]==-1 and self.rba[checking_node+3] not in checked_nodes:
                        if not self.rba[checking_node+3] in active_nodes:
                            active_nodes.append(self.rba[checking_node+3])
                        if self.rba[checking_node+3] not in nodes_to_check:
                            nodes_to_check.append(self.rba[checking_node+3])
                    nodes_to_check.remove(checking_node)
                    checked_nodes.append(checking_node)
        return len(active_nodes)

    def register_root(self,root):
        self.active_roots.append(root)
        #print self.active_roots

    def deregister_root(self,location):
        self.active_roots.remove(location)

    def get_word(self, name, nth_word):
        return self.rba[name+nth_word];

    def set_word(self, name, nth_word, new_val):
        self.rba[name+nth_word]=new_val;

#A node is actually just a method of referencing into memory.
#It has a name which is a pointer to the start of itself
class Node:
    def __init__(self, c, my_location, is_alloc=False):
        self.c=c
        self.my_location=my_location #name is basically a pointer to this in memory
        self.c.register_root(my_location)
        if is_alloc:
            self.set_word(0,self.c.allocs)
            self.set_word(1,self.c.allocs)

    def get_word(self,num): #really only like 2 words kinda
        if num>3:
            raise ValueError("Nodes only have 4 words on each, the first 2 are atoms and the second 2 are pointers")
        return self.c.get_word(self.my_location,num)

    def set_word(self,num,new_word):
        if num>3:
            raise ValueError("Nodes only have 4 words on each, the first 2 are atoms and the second 2 are pointers")
        self.c.set_word(self.my_location,num,new_word)

    def set_previous_node(self,num):
        self.set_word(2,num)

    def set_next_node(self,num):
        self.set_word(3,num)

    def get_previous_node(self):
        return self.get_word(2)

    def get_next_node(self):
        return self.get_word(3)

    def __del__(self):
        #print "killing "+str(self.my_location)
        try:
            self.c.deregister_root(self.my_location)
        except Exception as e:
            print e

#This method is necessary to prevent python from just passing around references to the same object.  We want to keep track of everything as roots, so we will force objects to be constructed and destructed when passed around
def copy_node(node):
    return Node(node.c,node.my_location)

def print_linked_list_forwards(node):
    i=0
    printed=[]
    while not node.my_location==-1 and node.my_location not in printed:
        printed.append(node.my_location)
        print "Node", i ,"at memory location", node.my_location,"has values("+ str(node.get_word(0)) +","+ str(node.get_word(1)) +") and pointers ("+ str(node.get_previous_node()) +","+ str(node.get_next_node()) +")"
        node=Node(node.c,node.get_word(3))
        i+=1
        #print printed

def print_linked_list_backwards(node):
    i=0
    printed=[]
    while not node.my_location==-1 and node.my_location not in printed:
        printed.append(node.my_location)
        print "Node", i ,"at memory location", node.my_location,"has values("+ str(node.get_word(0)) +","+ str(node.get_word(1)) +") and pointers ("+ str(node.get_previous_node()) +","+ str(node.get_next_node()) +")"
        node=Node(node.c,node.get_word(2))
        i+=1

def get_reference_to_node_forwards(first_node,n):
    node=copy_node(first_node)
    while n>0:
        node=Node(node.c,node.get_word(3))
        n-=1
        if node.my_location==-1:
            raise IndexError("Node out of range")
    return copy_node(node)

def get_reference_to_node_backwards(last_node,n):
    node=copy_node(last_node)
    while n>0:
        node=Node(node.c,node.get_word(2))
        n-=1
        if node.my_location==-1:
            raise IndexError("Node out of range")
    return copy_node(node)

def remove_nth_node_forwards(first_node, n):
    if n==0:
        print "Can not delete the passed node"
    prev_node=get_reference_to_node_forwards(first_node,n-1)
    next_node=get_reference_to_node_forwards(first_node,n+1)
    prev_node.set_word(3,next_node.my_location)
    next_node.set_word(2,prev_node.my_location)

def remove_nth_node_backwards(last_node, n):
    if n==0:
        print "Can not delete the passed node"
    prev_node=get_reference_to_node_backwards(last_node,n-1)
    next_node=get_reference_to_node_backwards(last_node,n+1)
    prev_node.set_word(2,next_node.my_location)
    next_node.set_word(3,prev_node.my_location)

def add_nth_node_forwards(first_node, n):
    prev_node=get_reference_to_node_forwards(first_node,n)
    next_node=get_reference_to_node_forwards(first_node,n+1)
    new_node=first_node.c.allocate()
    prev_node.set_next_node(new_node.my_location)
    next_node.set_previous_node(new_node.my_location)
    new_node.set_previous_node(prev_node.my_location)
    new_node.set_next_node(next_node.my_location)

def add_nth_node_backwards(last_node, n):
    prev_node=get_reference_to_node_forwards(last_node,n+1)
    next_node=get_reference_to_node_forwards(last_node,n)
    new_node=first_node.c.allocate()
    prev_node.set_next_node(new_node.my_location)
    next_node.set_previous_node(new_node.my_location)
    new_node.set_previous_node(prev_node.my_location)
    new_node.set_next_node(next_node.my_location)

def force_garbage_collect(c):
    for i in range(0,3):
        spare_node=c.allocate()
        del spare_node

def print_memory_status(c):
    print "Max heap size: ",c.heap_size
    print "Lifetime memory allocated: ",c.allocs
    print "Current memory used: ",c.count_active_nodes()

if __name__ == '__main__':
    first_node=None
    last_node=None
    heap_size=200
    num_nodes=24
    print "\n\n\nInitializing a manager with a heap of size", heap_size, "...\n"
    c=Manager(heap_size) #give me 100 words in my heap
    print "Creating a doubly linked list with",num_nodes,"nodes in it", "...\n"
    first_node=c.allocate()
    previous_node=copy_node(first_node)
    #Creating the linked list with num_nodes nodes
    for i in range(0,num_nodes-1):
        previous_node.set_word(0,i)
        previous_node.set_word(1,i)
        new_node=c.allocate()
        new_node.set_word(2,previous_node.my_location)
        previous_node.set_word(3,new_node.my_location)
        previous_node=copy_node(new_node)
        if i==num_nodes-2:
            last_node=copy_node(new_node)
            last_node.set_word(0,i+1)
            last_node.set_word(1,i+1)
    del previous_node
    del new_node

    print "The doubly linked list has been created", "...\n"
    print "Now, the only active roots should be to the first_node and the last_node"
    print "active_roots: ",c.active_roots
    print "The linked list, looking forwards:"
    print_linked_list_forwards(copy_node(first_node))
    print_memory_status(c)
    #print_linked_list_backwards(copy_node(last_node))
    #print "The memory array: ", c.rba

    print "\nNow let's dereference three nodes from somewhere in the middle", "...\n"
    remove_nth_node_forwards(first_node,3)
    remove_nth_node_forwards(first_node,5)
    remove_nth_node_forwards(first_node,9)
    print_memory_status(c)

    print "\nNow let's add three new nodes", "...\n"
    add_nth_node_forwards(first_node,10)

    print "\nactive_roots: ",c.active_roots
    print "The linked list, looking forwards:"
    print_linked_list_forwards(copy_node(first_node))
    print "\nThe linked list, looking backwards:"
    print_linked_list_backwards(copy_node(last_node))

    add_nth_node_forwards(first_node,10)
    add_nth_node_forwards(first_node,10)
    print_memory_status(c)

    print "\nNow let's make the linked list circular", "...\n"
    first_node.set_word(2,last_node.my_location)
    last_node.set_word(3,first_node.my_location)
    print_memory_status(c)

    print "\nNow let's force a garbage collect with these circular references", "...\n"
    force_garbage_collect(c)
    print_memory_status(c)

    print "\nNow let's change up the order of some nodes and force a garbage collect", "...\n"
    node_5=get_reference_to_node_forwards(first_node,5)
    node_9=get_reference_to_node_forwards(first_node,9)
    Node(c,node_5.get_previous_node()).set_next_node(node_9.my_location)
    Node(c,node_5.get_next_node()).set_previous_node(node_9.my_location)
    node_9_next=node_9.get_next_node()
    node_9_prev=node_9.get_previous_node()
    node_9.set_previous_node(node_5.get_previous_node())
    node_9.set_next_node(node_5.get_next_node())
    Node(c,node_9_prev).set_next_node(node_5.my_location)
    Node(c,node_9_next).set_previous_node(node_5.my_location)
    node_5.set_previous_node(node_9_prev)
    node_5.set_next_node(node_9_next)
    del node_5
    del node_9
    force_garbage_collect(c)
    print_memory_status(c)

    print "\nNow let's change the roots and force a garbage collect", "...\n"
    new_first_node=c.allocate()
    new_last_node=c.allocate()
    new_first_node.set_next_node(first_node.my_location)
    new_first_node.set_previous_node(new_last_node.my_location)
    new_last_node.set_previous_node(last_node.my_location)
    new_last_node.set_next_node(new_first_node.my_location)
    first_node=copy_node(new_first_node)
    last_node=copy_node(new_last_node)
    del new_last_node
    del new_first_node
    force_garbage_collect(c)
    print_memory_status(c)

    print "\nactive_roots: ",c.active_roots
    print "The linked list, looking forwards:"
    print_linked_list_forwards(copy_node(first_node))
    print "\nThe linked list, looking backwards:"
    print_linked_list_backwards(copy_node(last_node))

    print "\n\nCongratulations, your garbage collector has passed all of the tests that I have thought of for it.\nI should probably test it with a binary tree, but I didn't, so yay!\n\n\n"
