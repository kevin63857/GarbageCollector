class Collector:
    #the heap can only have Nodes in it.
    # the first and second words are the first node's data
    # the third and fourth words are the first node's pointers
    # the fifth and sixth words are the second node's data...
    # -1 denotes a null pointer
    def __init__(self, heap_size):
        self.heap_size=heap_size
        self.rba=[-1]*heap_size
        self.active_roots=[]

    def allocate(self):#only allocates linked list nodes
        return Node(self,0)

    def register_root(self,root):
        active_roots.append(root)

    def deregister_root(self,node):
        active_roots.remove(node.my_location)

    def get_word(self, name, nth_word):
        return rba[name+nth_word];

    def set_word(self, name, nth_word, new_val):
        rba[name+nth_word]=new_val;

#A node is actually just a method of referencing into memory.
#It has a name which is a pointer to the start of itself
class Node:
    def __init__(self, c, my_location):
        self.c=c
        self.my_location=my_location #name is basically a pointer to this in memory
        self.is_alive=True
        self.c.register_root(my_location)
        return;
    def get_word(self,num): #really only like 2 words kinda
        if not is_alive:
            raise
        if num>3:
            raise ValueError("Nodes only have 4 words on each, the first 2 are atoms and the second 2 are pointers")
        return self.c.get_word(my_location,num)
    def set_word(self,num,new_word):
        if num>3:
            raise ValueError("Nodes only have 4 words on each, the first 2 are atoms and the second 2 are pointers")
        self.c.set_word(my_location,num,new_word)
    def die(self):
        self.is_alive=False
        self.c.deregister_root(my_location)

def copy_node(node):
    return Node(node.c,node.my_location)

if __name__ == '__main__':
    c=Collector(100) #give me 100 words in my heap
    first_node=c.allocate()
    previous_node=copy_node(first_node);
    last_node=None
    for i in range(0,20):
        new_node=c.allocate()
        new_node.set_word(2,previous_node.my_location)
        previous_node.setWord(3,new_node.my_location)
        previous_node.die() #check to see if this can be run automatically when re-referencing previous_node
        previous_node=copy_node(new_node)
        new_node.die()
        if i==19:
            last_node=copy_node(new_node)
    #do some more cool stuff after this to test the GC
