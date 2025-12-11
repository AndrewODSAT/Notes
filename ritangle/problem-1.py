'''
This is very inefficient but is the most accurate model of the problem I could think of.
Glso this is good practice for datastructures for the exams.
'''

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Linked_List:
    def __init__(self, name, head_node):
        self.name = name
        self.head = head_node
        self.tail = head_node

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

# Note: range(inclusive, exclusive)
cog_1 = Linked_List("Cog_1", None)
cog_1.append_list([])

cog_2 = Linked_List("Cog_2", None)
cog_2.append_list(list(range(10,21)))

cog_3 = Linked_List("Cog_3", None)
cog_3.append_list(list(range(1,10)))

cog_1_node = cog_1.head
cog_2_node = cog_2.head
cog_3_node = cog_3.head

cog_1.output()
cog_2.output()
cog_3.output()

S = 0
T = 0



for _ in range(792):
    val_1 = cog_1_node.value
    val_2 = cog_2_node.value
    val_3 = cog_3_node.value
    num = int(str(val_1) + str(val_2) + str(val_3))
    S += num

    T += val_1 * val_2 * val_3

    cog_1_node = cog_1_node.next
    cog_2_node = cog_2_node.next
    cog_3_node = cog_3_node.next

    print(f"Current string: {num}\nCurrent product: {val_1 * val_2 * val_3}\n")

print(f"T: {T}\nS: {S}\nS/T: {S/T}")

cog_1.output()
cog_2.output()
cog_3.output()
