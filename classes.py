import tkinter as t
from tkinter.constants import DISABLED
from abc import ABC, abstractmethod
import random as r

class Deck:
    '''Deck class; essentially a list that contains random Card objects'''

    def __init__(self, root, row):
        '''The constructor of the Deck class
        Parameters:
            root - The tkinter window in which to place the image of the Deck
            row - The row of the tkinter window in which to place the image of the Deck
        '''

        # Instance variable, a list of Card objects
        self.cards = []

        # Fills the list with pseudo-random Card objects
        self.random_cards()

        # Creates a LabelFrame for the Deck image
        self.frame = t.LabelFrame(root)

        # The image of the Deck, a backside up playing card
        self.image = t.PhotoImage(file="images/backofcard.png")

        # Draws the image of the Deck to the LabelFrame
        self.label = t.Label(self.frame, image=self.image)
        self.label.pack()

        # Draws the LabelFrame to the window
        self.frame.grid(row=row, column=1)
    
    def random_cards(self):
        '''Adds 20 pseudo-random Card objects to the Deck's list of Cards'''

        # Over 20 iterations...
        for i in range(20):

            # Generate a random number from 1 to 100, inclusive
            random_number = r.randint(1, 100)

            # 25% chance that a BabyBird Card is added to the Deck
            if random_number <= 25:
                self.cards.append(BabyBird())
            
            # 25% chance that a PeaceableElephant Card is added to the Deck
            elif random_number <= 50:
                self.cards.append(PeaceableElephant())
            
            # 50% chance that a Rosean Card is added to the Deck
            else:
                self.cards.append(Rosean())

    def pull_card(self):
        '''Simulates pulling a Card from the Deck, removing and returning a Card from the list of Cards'''

        # Removes and returns a Card from the list of Cards
        return self.cards.pop()
    
    def empty(self):
        '''Returns True if the Deck has exhausted its Card objects, False otherwise'''

        # If the Deck has run out of Cards...
        if len(self.cards) == 0:

            # Remove the Deck LabelFrame from the window and return True
            self.frame.grid_remove()
            return True
        
        # If there are still Cards in the Deck...
        else:

            # Return False
            return False

class Card(ABC):
    '''An abstract class for a Card'''

    def __init__(self, image_name, name, HP, attack, cost):
        '''Constructor for the abstract Card class
        Parameters:
            image_name - The name of the image file associated with the Card
            name - The name of the Card
            HP - The HP value of the Card
            attack - The attack value of the Card
            cost - The cost value of the Card
        '''

        # Sets the image instance variable of the Card to the image suggested by the image_name parameter
        self.image = t.PhotoImage(file="images/" + image_name)

        # Sets the selected_image instance variable of the Card to the selected image suggested by the image_name parameter
        self.selected_image = t.PhotoImage(file="images/" + "Selected" + image_name)

        # Sets the name, HP, attack, and cost instance variables of the Card in a straightforward manner
        self.name = name
        self.HP = HP
        self.attack = attack
        self.cost = cost

        # Sets the text instance variable of the Card equal to a string that describes various attributes of the
        # Card
        self.text = (self.name + "\n" + "Cost : " + str(cost) + "\n" "Attack : " + str(attack) + "\n" + 
                    "HP: " + str(HP))
    
    def update_text(self):
        '''Updates the text of the Card according to changes in its instance variables'''

        # Updates the text of the Card
        self.text = (self.name + "\n" + "Cost : " + str(self.cost) + "\n" "Attack : " + str(self.attack) + "\n" + 
                    "HP: " + str(self.HP))

class BabyBird(Card):
    '''A BabyBird class, a child of the Card abstract class'''

    def __init__(self):
        '''Constructor for the BabyBird class'''

        # Calls the constructor of the Card class with parameters specifically appropriate to a BabyBird Card
        super().__init__("BirdInWombEX.png", "Womb-Bound Bird", 1, 2, 2)

    def update_text(self):
        '''Updates the text of the Card according to changes in its instance variables'''
        
        # Calls the parent's update_text method
        super().update_text()

class PeaceableElephant(Card):
    '''A PeaceableElephant class, a child of the Card abstract class'''

    def __init__(self):
        '''Constructor for the PeaceableElephant class'''

        # Calls the constructor of the Card class with parameters specifically appropriate to a PeaceableElephant Card
        super().__init__("peacableelephant.png", "Peaceable Elephant", 6, 1, 4)
    
    def update_text(self):
        '''Updates the text of the Card according to changes in its instance variables'''

        # Calls the parent's update_text method
        super().update_text()

class Rosean(Card):
    '''A Rosean class, a child of the Card abstract class'''

    def __init__(self):
        '''Constructor for the Rosean class'''

        # Calls the constructor of the Card class with parameters specifically appropriate to a Rosean Card
        super().__init__("flower.png", "Rosean", 3, 3, 6)
    
    def update_text(self):
        '''Updates the text of the Card according to changes in its instance variables'''
        
        # Calls the parent's update_text method
        super().update_text()