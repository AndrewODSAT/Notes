class Video:
    def __init__(self, name):
        # __variable_name makes a variable private in python
        self.__name = name
        self.__views = 0
        self.__stars = 3

    def update_views(self):
        self.__views += 1

class Worker:
    def get_name(self):
        return self.__name

    def get_attendance(self):
        return self.__attendance

    def set_name(self, name):
        self.__name = name

    def set_attendance(self, attendance):
        if attendance >= 0 and attendance <=100:
            self.__attendance = attendance
            return True
        return False

class ItemForSale:
    def __init__(self, item_name, price):
        # don't start with __ so these are public in python
        self.item_name = item_name
        self.price = price
        self.discount = 0

    def calculatePrice(self):
        return price - (self.discount/100) * price

mushypeas = ItemForSale("mushy peas", 0.89)
