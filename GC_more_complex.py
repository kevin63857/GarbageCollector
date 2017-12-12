from GC_interface import GarbageCollector

#This is a WAYYYY better garbage collector!  It does not require a garbage
# collector of its own and it functions solely in statically allocated memory.
# It works quite similarly to mark and sweep in that the 'marking' is done in
# the bits left over between how large a word is and how large a pointer is.
# Here, it assumes that pointers will be less than 22 bits long, which I think
# is a pretty fair assumption for this simulator.

#This one takes MUCH less memory and even runs way faster than it's predecessor,
# although, it could still be improved on.

#data should be treated in 4 byte chunks
# data can only have Nodes in it.
# the first and second words are the first node's data
# the third and fourth words are the first node's pointers
# the fifth and sixth words are the second node's data...
# -1 denotes a null pointer

class GC_more_complex(GarbageCollector):
    def __init__(self):
        self.alloc_count=-1
        self.active_mask=(2**26)
        self.checked_mask=(2**27)
        self.toCheck_mask=(2**28)

    def is_marked_active(self,data_copy,i):
        return data_copy[i+2]&self.active_mask
    def is_marked_checked(self,data_copy,i):
        return data_copy[i+2]&self.checked_mask
    def is_marked_toCheck(self,data_copy,i):
        return data_copy[i+2]&self.toCheck_mask
    def mark_active(self,data_copy,i):
        if not self.is_marked_active(data_copy,i):
            data_copy[i+2]=data_copy[i+2]|self.active_mask
    def mark_checked(self,data_copy,i):
        if not self.is_marked_checked(data_copy,i):
            data_copy[i+2]=data_copy[i+2]|self.checked_mask
    def mark_toCheck(self,data_copy,i):
        if not self.is_marked_toCheck(data_copy,i):
            data_copy[i+2]=data_copy[i+2]|self.toCheck_mask
    def unmark_toCheck(self,data_copy,i):
        if self.is_marked_toCheck(data_copy,i):
            data_copy[i+2]=data_copy[i+2]&(~self.toCheck_mask)
    def get_next_node_to_check(self,data_copy):
        i=0
        while i<len(data_copy) and not self.is_marked_toCheck(data_copy,i):
            i+=4
        return i if i<len(data_copy) else -1


    def allocate(self,data,active_roots):
        self.alloc_count+=1
        mask=(2**25)-1
        data_copy=[i if i>=0 else 2**23 for i in data]
        for i in active_roots:
            if not self.is_marked_checked(data_copy,i): #if i has not been checked, make sure it is in active_nodes and add both of its children to the to_check list
                self.mark_active(data_copy,i)
                if not data_copy[i+2]&mask==2**23 and not self.is_marked_checked(data_copy,data_copy[i+2]&mask):
                    self.mark_active(data_copy,data_copy[i+2]&mask)
                    self.mark_toCheck(data_copy,data_copy[i+2]&mask)
                if not data_copy[i+3]&mask==2**23 and not self.is_marked_checked(data_copy,data_copy[i+3]&mask):
                    self.mark_active(data_copy,data_copy[i+3]&mask)
                    self.mark_toCheck(data_copy,data_copy[i+3]&mask)
                self.mark_checked(data_copy,i)
                while not self.get_next_node_to_check(data_copy)==-1:
                    checking_node=self.get_next_node_to_check(data_copy)
                    if not data_copy[checking_node+2]&mask==2**23 and not self.is_marked_checked(data_copy,data_copy[checking_node+2]&mask):
                        self.mark_active(data_copy,data_copy[checking_node+2]&mask)
                        self.mark_toCheck(data_copy,data_copy[checking_node+2]&mask)
                    if not data_copy[checking_node+3]&mask==2**23 and not self.is_marked_checked(data_copy,data_copy[checking_node+3]&mask):
                        self.mark_active(data_copy,data_copy[checking_node+3]&mask)
                        self.mark_toCheck(data_copy,data_copy[checking_node+3]&mask)
                    self.unmark_toCheck(data_copy,checking_node)
                    self.mark_checked(data_copy,checking_node)
        i=0
        while i<len(data_copy):
            if not self.is_marked_active(data_copy,i):
                return i
            i+=4
        return -1 #This would indicate that every node is active and return a null pointer, aka heap overflow
