
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
