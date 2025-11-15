import random

class Person:
    def __init__(self):

        self.charisma = random.randint(3, 18)
        self.dexterity = random.randint(3, 18)
        self.intelligence = random.randint(3, 18)
        
        self.hp = 10 + (self.dexterity - 10) // 2