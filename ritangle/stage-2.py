import math



def calc_area(a, b, c):
    try:
        angle = math.acos((b**2 + c**2 - a**2) / (2*b*c))
    except:
        return -1.5
    return 0.5*b*c*math.sin(angle)

def is_int_area(num):
    a = int(str(num)[0:3])
    b = int(str(num)[3:6])
    c = int(str(num)[6:9])

    try:
        angle = math.acos((b**2 + c**2 - a**2) / (2*b*c))
        area = 0.5*b*c*math.sin(angle)
        if area%1==0:
            return True
    except:
        ...
    return False

def is_fibonacci(num):
    fib_nums = [102334155, 165580141, 267914296,433494437,701408733]
    return num in fib_nums

def contains_60_angle(num):
    a = int(str(num)[0:3])
    b = int(str(num)[3:6])
    c = int(str(num)[6:9])

    cos_angles =[
            ((b**2 + c**2 - a**2) / (2*b*c)),
            ((a**2 + c**2 - b**2) / (2*a*c)),
            ((a**2 + b**2 - c**2) / (2*a*b)),
                 ]
    return cos_angles[0]>=0.4999990 and cos_angles[0]<=0.50000001\
           or cos_angles[1]>=0.4999990 and cos_angles[1]<=0.50000001\
           or cos_angles[2]>=0.4999990 and cos_angles[2]<=0.50000001\

def is_prim_pythag_trip(num):
    a = int(str(num)[0:3])
    b = int(str(num)[3:6])
    c = int(str(num)[6:9])
    nums = [a,b,c]
    nums.sort()

    if math.gcd(a,b,c) != 1:
        return False

    return nums[0]**2 + nums[1]**2 == nums[2]**2

class CogSet:
    def __init__(self, cog_1_node, cog_2_node, cog_3_node):
        self.cog_1 = cog_1_node
        self.cog_2 = cog_2_node
        self.cog_3 = cog_3_node
        self.num = 0
        self.update_num()
        self.turns = 0
        self.max_turns = 1000

    def reset_turns(self):
        self.turns = 0

    def get_turns(self):
        return self.turns

    def update_num(self):
        val_1 = self.cog_1.value
        val_2 = self.cog_2.value
        val_3 = self.cog_3.value

        self.num = int(str(val_1) + str(val_2) + str(val_3))

    def rotate_once(self):
        self.cog_1 = self.cog_1.next
        self.cog_2 = self.cog_2.next
        self.cog_3 = self.cog_3.next

        self.update_num()
        self.turns += 2

    def rotate_to_value(self, value):
        self.start_turns = self.turns
        while (self.num != value):
            self.rotate_once()

            if self.turns > self.max_turns:
                print(f"Warning: turns exceeded max ({self.max_turns}): {self.turns}")
            if self.turns - self.start_turns > self.max_turns:
                print(f"Couldn't find val")
                return -1
        return 1

    def rotate_to_truth(self, func):
        self.start_turns = self.turns
        while (not func(self.num)):
            self.rotate_once()

            if self.turns > self.max_turns:
                print(f"Warning: turns exceeded max ({self.max_turns}): {self.turns}")
            if self.turns - self.start_turns > self.max_turns:
                print(f"Couldn't find val")
                return -1
        return 1

    def output(self):
        print(f"Current Cog Set (turns={self.turns}): {self.num}")

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def output(self):
        print(f"Node Value: {self.value}")

class Linked_List:
    def __init__(self, name, head_node):
        self.name = name
        self.head = head_node
        self.tail = head_node
        self.current = head_node

    def append_list(self, list_of_values):
        # if list provided empty
        if not list_of_values:
            print("List provided empty")
            return -1
            
        # if empty
        if self.head is None:
            self.head = Node(list_of_values[0])
            prev_node = self.head

        # if not empty
        else:
            self.tail.next = Node(list_of_values[0])
            prev_node = self.tail.next

        # append each node
        for value in list_of_values[1:]:
            new_node = Node(value)
            prev_node.next = new_node
            prev_node = prev_node.next

        # make circular
        self.tail = new_node
        self.tail.next = self.head

        return 1

    def output(self):
        print(f"Linked List: {self.name}")
        # if empty
        if not self.head:
            print(f"    Empty")
            return
            
        # if not empty
        current_node = self.head
        while current_node != self.tail:
            print(f"    Node: {current_node.value}")
            current_node = current_node.next
        print(f"    Node: {current_node.value}")
        return

cog_1 = Linked_List("Cog_1", None)
cog_1.append_list([267,851,259,433,493,165,701,102])

cog_2 = Linked_List("Cog_2", None)
cog_2.append_list([914,494,468,460,143,150,832,580,299,334,408])

cog_3 = Linked_List("Cog_3", None)
cog_3.append_list([296,763,155,145,168,437,733,154,141])

cog_set = CogSet(cog_1.head, cog_2.head, cog_3.head)

fib_nums = [102334155, 165580141, 267914296,433494437,701408733]

#for i in range(20):
#    cog_set.rotate_to_truth(is_int_area)
#    cog_set.output()
#    cog_set.rotate_once()
#    cog_set.reset_turns()

for fib in fib_nums:
    print(f"Testing from fib: {fib}")
    cog_set.rotate_to_value(fib)
    cog_set.reset_turns()

    cog_set.rotate_to_truth(is_prim_pythag_trip)
    p = cog_set.get_turns()
    cog_set.output()
    cog_set.reset_turns()

    cog_set.rotate_to_truth(contains_60_angle)
    q = cog_set.get_turns()
    cog_set.output()
    cog_set.reset_turns()

    cog_set.rotate_to_truth(is_int_area)
    r = cog_set.get_turns()
    cog_set.output()
    cog_set.reset_turns()

    cog_set.rotate_to_truth(is_fibonacci)
    s = cog_set.get_turns()
    cog_set.output()
    cog_set.reset_turns()

    print(f"p:{p}, q:{q}, r:{r}, s:{s} \np*q*r*s = {p*q*r*s} \n")

