import random

class Tamagotchi:
    def __init__(self, name):
        self.name = name
        self.hunger = 0
        self.health = 10
        self.boredom = 0
        self.exhaustion = 0

    def is_alive(self):
        return self.health > 0

    def can_act(self):
        if not self.is_alive():
            print(f"{self.name} is dead and cannot perform actions.")
            return False
        return True

    def feed(self):
        if not self.can_act():
            return
        self.hunger -= 1

    def play(self):
        if not self.can_act():
            return
        self.boredom -= 1
        self.hunger += 1
        self.exhaustion += 1

    def sleep(self):
        if not self.can_act():
            return
        self.exhaustion -= 1

    def heal(self):
        if not self.can_act():
            return
        self.health += 1

    def random_event(self):
        if not self.is_alive() or random.random() >= 0.2:
            return

        health_change = random.choice((-1, 1))
        self.health = max(0, self.health + health_change)
        if self.health == 0:
            print(f"{self.name} had a health setback and died.")
        elif health_change > 0:
            print(f"{self.name} got a health bonus. Health: {self.health}")
        else:
            print(f"{self.name} had a health setback. Health: {self.health}")

    def stats(self):
        print(f"Name: {self.name}\nHunger: {self.hunger}\nHealth: {self.health}\nBoredom: {self.boredom}\nExhaustion: {self.exhaustion}\n")