from ListNode import *

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
