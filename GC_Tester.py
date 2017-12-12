from Manager import *
from GC_Utilities import *
from ListNode import *

def test(garbage_collector_class,heap_size=100):
    first_node=None
    last_node=None
    #heap_size=200
    num_nodes=24
    print "\n\n\nInitializing a manager with a heap of size", heap_size, "...\n"
    garbage_collector=garbage_collector_class()
    c=Manager(heap_size,garbage_collector) #give me 100 words in my heap
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
