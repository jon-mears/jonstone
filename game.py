import tkinter as t
from tkinter.constants import ACTIVE, CENTER, DISABLED
import random as r
import classes as c
from functools import *

class Application:
    '''Class in which all "states" are encapsulated'''

    # Creates a global variable for the tkinter window
    root = t.Tk()

    def __init__(self):
        '''Constructor of the Application Class'''

        # Sets the background of the tkinter window to a dark green color
        Application.root.configure(bg="#556B2F")

        # Sets the tkinter window to full screen
        Application.root.attributes("-fullscreen", True)

        # Binds F11 to activating full screen
        Application.root.bind("<F11>", self.toggle_full_screen)

        # Binds Escape to deactivating full screen
        Application.root.bind("<Escape>", self.quit_full_screen)

        # Instantiates a Menu, taking the user to the Menu "screen"
        Application.Menu()
    
    def toggle_full_screen(self, event):
        '''Makes the tkinter window full screen'''

        # Sets the tkinter window to full screen
        Application.root.attributes("-fullscreen", True)
    
    def quit_full_screen(self, event):
        '''Makes the tkinter window not full screen'''

        # Deactivates full screen
        Application.root.attributes("-fullscreen", False)

    class Menu:
        '''Class for the Menu "state"'''
        
        def __init__(self):
            '''Constructor for the Menu class'''

            # Sets up the Menu
            self.setup()
        
        def setup(self):
            '''Initializes the various tkinter widgets that constitute a Menu'''

            # Removes every widget currently drawn to the tkinter window
            for widget in Application.root.winfo_children():
                widget.destroy()
            
            # Adds a play button to the Menu
            play_button = t.Button(Application.root, text="Play!", command=self.play, bg="black", fg="white", font=("Times New Roman", 30))
            play_button.pack()

            # Adds an exit button to the Menu, which closes the entire program
            exit_button = t.Button(Application.root, text="Exit", command=Application.root.destroy, bg="black", fg="white", font=("Times New Roman", 30))
            exit_button.pack()

            # Runs the mainloop of the tkinter window
            Application.root.mainloop()
            
        def play(self):
            '''Begins gameplay from the Menu'''

            # Instantiates a Game, taking the user to the Game "screen"
            Application.Game()

    class Game:
        '''Class for the Game "state"'''

        def __init__(self):
            '''Constructor for the Game class'''

            # Sets up the Game
            self.setup()

            # Begins the first turn of the player
            self.player_turn()
        
        def setup(self):
            '''Initializes the various tkinter widgets that constitute a Game'''

            # Removes every widget currently drawn to the tkinter window
            for widget in Application.root.winfo_children():
                widget.destroy()
            
            # Initializes an empty list that will contain the cards in the computer-controlled opponent's hand
            self.opponent_hand = []

            # Initializes the mana that the player/opponent starts a turn with to 0
            self.start_mana = 0

            # Initializes the current mana to 0
            self.mana = 0

            # Sets the update text at the side of the screen to write "Begin!" and places it on the screen
            self.text = "Begin!"
            self.text_label = t.Label(Application.root, text=self.text, bg="black", fg="white")
            self.text_label.grid(row=1, column=3)

            # Initializes various images
            self.empty_image = t.PhotoImage(file="images/empty.png")
            self.place_image = t.PhotoImage(file="images/place.png")
            self.eye_image = t.PhotoImage(file="images/eye.png")
            self.bunny_image = t.PhotoImage(file="images/bunny.png")

            # Creates and fills a dictionary for attributes of the opponent, including a LabelFrame, text that 
            # writes their HP, text that writes their name (hard-coded to "Eye"), and a button that will eventually
            # allow the player to attack the opponent with cards placed on the table 
            self.opponent = {}

            self.opponent["frame"] = t.LabelFrame(Application.root, bg="brown", fg="white")
            self.opponent["HP"] = t.Label(self.opponent["frame"], text="20", bg="brown", fg="white", font=("Times New Roman", 8))
            self.opponent["name"] = t.Label(self.opponent["frame"], text="Eye", bg="brown", fg="white", font=("Times New Roman", 8))
            self.opponent["button"] = t.Button(self.opponent["frame"], image=self.eye_image, state=DISABLED, command=None)

            # Places the various attributes of the opponent contained within the dictionary at the top of the screen 
            self.opponent["frame"].grid(row=0, column=0)
            self.opponent["HP"].grid(row=1, column=0, pady=0)
            self.opponent["name"].grid(row=2, column=0, pady=0)
            self.opponent["button"].grid(row=0, column=0, pady=0)

            # Creates and fills a dictionary for attributes of the player, including a LabelFrame, text that 
            # writes their HP, text that writes their name (hard-coded to "Bunny"), and a button that will eventually
            # allow the player to attack themselves with cards placed on the table 
            self.player = {}
            self.player["frame"] = t.LabelFrame(Application.root, bg="black", fg="white")
            self.player["HP"] = t.Label(self.player["frame"], text="20", bg="black", fg="white", font=("Times New Roman", 8))
            self.player["name"] = t.Label(self.player["frame"], text="Bunny", bg="black", fg="white", font=("Times New Roman", 8))
            self.player["button"] = t.Button(self.player["frame"], image=self.bunny_image, state=DISABLED, command=None)

            # Places the various attributes of the opponent contained within the dictionary at the top of the screen 
            self.player["frame"].grid(row=4, column=0)
            self.player["HP"].grid(row=1, column=0)
            self.player["name"].grid(row=2, column=0)
            self.player["button"].grid(row=0, column=0)

            # Creates and places a button that ends the player's current turn
            self.end_turn_button = t.Button(Application.root, text="End Turn", command=self.opponent_turn, state=DISABLED, bg="black", fg="white", font=("Times New Roman", 8))
            self.end_turn_button.grid(row=2, column=1)

            # Creates and places a button that exits the entire program
            self.exit_button = t.Button(Application.root, text="Exit", command=Application.root.destroy, state=ACTIVE, bg="black", fg="white", font=("Times New Roman", 8))
            self.exit_button.grid(row=3, column=4)
            
            # Creates and places a LabelFrame for the opponent's cards on the table
            self.opponent_table_frame = t.LabelFrame(Application.root, bg="brown", fg="white")
            self.opponent_table_frame.grid(row=1, column=0)

            # Instantiates a Deck object for the opponent, placed at the 0th row
            self.opponent_deck = c.Deck(Application.root, 0)

            # Creates and places a LabelFrame for the player's cards on the table
            self.player_table_frame = t.LabelFrame(Application.root, bg="black", fg="white")
            self.player_table_frame.grid(row=2, column=0)

            # Instantiates a Deck object for the player, placed at the 1st row
            self.player_deck = c.Deck(Application.root, 1)

            # Creates and places a LabelFrame for the player's cards in their hand
            self.player_hand_frame = t.LabelFrame(Application.root, bg="black", fg="white")
            self.player_hand_frame.grid(row=3, column=0)

            # Instantiates a list of dictionaries for the 5 spaces for cards on the player's side of the table
            self.player_table_containers = [{}, {}, {}, {}, {}]

            # Instantiates a list of dictionaries for the 5 spaces for cards on the opponent's side of the table
            self.opponent_table_containers = [{}, {}, {}, {}, {}]

            # Instantiates a list of dictionaries for the 5 spaces for cards in the player's hand
            self.player_hand_containers = [{}, {}, {}, {}, {}]

            # Creates and places a Label that shows the mana the player has available out of the total mana they
            # started the turn with (current mana/start mana)
            self.mana_text = t.Label(Application.root, text="Mana: " + str(self.mana) + "/" + str(self.start_mana), bg="black", fg="white", font=("Times New Roman", 8))
            self.mana_text.grid(row=2, column=2)

            # Sets up the keys and values for the 5 container dictionaries in each container list
            for i in range(5):

                # Sets up the keys and values for the 5 dictionaries denoting the containers on the player's side of the 
                # table
                # These attributes include the LabelFrame for the container, a boolean that tells whether the container
                # is empty or not, a button with a command that changes according to the "selection state," a 
                # Card object, a Label that displays the attributes of the Card in text, and a boolean that states 
                # whether the Card in the container (assuming there is one) can currently attack or not
                self.player_table_containers[i]["frame"] = t.LabelFrame(self.player_table_frame, bg="black", fg="white")
                self.player_table_containers[i]["empty"] = True
                self.player_table_containers[i]["button"] = t.Button(self.player_table_containers[i]["frame"], image=self.place_image, command=None, state=DISABLED, height=100)
                self.player_table_containers[i]["card"] = None
                self.player_table_containers[i]["card text"] = t.Label(self.player_table_containers[i]["frame"], text="", bg="black", fg="white", font=("Times New Roman", 8))
                self.player_table_containers[i]["cannot attack"] = True

                # Places the various attributes of each container on the player's side of the table to the screen
                self.player_table_containers[i]["frame"].grid(row=0, column=i)
                self.player_table_containers[i]["button"].grid(row=0, column=0)
                self.player_table_containers[i]["card text"].grid(row=1, column=0)

                # Sets up the keys and values for the 5 dictionaries denoting the containers on the opponent's side of the 
                # table
                # These attributes include the LabelFrame for the container, a boolean that tells whether the container
                # is empty or not, a button with a command that changes according to the "selection state," a 
                # Card object, and a Label that displays the attributes of the Card in text
                self.opponent_table_containers[i]["frame"] = t.LabelFrame(self.opponent_table_frame, bg="brown", fg="white")
                self.opponent_table_containers[i]["empty"] = True
                self.opponent_table_containers[i]["button"] = t.Button(self.opponent_table_containers[i]["frame"], image=self.empty_image, command=None, state=DISABLED, bg="brown", fg="white", height=100)
                self.opponent_table_containers[i]["card"] = None
                self.opponent_table_containers[i]["card text"] = t.Label(self.opponent_table_containers[i]["frame"], text="", bg="brown", fg="white", font=("Times New Roman", 8))

                # Places the various attributes of each container on the opponent's side of the table to the screen
                self.opponent_table_containers[i]["frame"].grid(row=0, column=i)
                self.opponent_table_containers[i]["button"].grid(row=0, column=0)
                self.opponent_table_containers[i]["card text"].grid(row=1, column=0)

                # Sets up the keys and values for the 5 dictionaries denoting the containers in the player's hand
                # These attributes include the LabelFrame for the container, a boolean that tells whether the container
                # is empty or not, a button with a command that changes according to the "selection state," a 
                # Card object, and a Label that displays the attributes of the Card in text
                self.player_hand_containers[i]["frame"] = t.LabelFrame(self.player_hand_frame, bg="black", fg="white")
                self.player_hand_containers[i]["empty"] = True
                self.player_hand_containers[i]["button"] = t.Button(self.player_hand_containers[i]["frame"], image=self.empty_image, command=None, state=DISABLED, bg="black", fg="white", height=100)
                self.player_hand_containers[i]["card"] = None
                self.player_hand_containers[i]["card text"] = t.Label(self.player_hand_containers[i]["frame"], text="", bg="black", fg="white", font=("Times New Roman", 8))

                # Places the various attributes of each container in the player's hand to the screen
                self.player_hand_containers[i]["frame"].grid(row=0, column=i)
                self.player_hand_containers[i]["button"].grid(row=0, column=0)
                self.player_hand_containers[i]["card text"].grid(row=1, column=0)

        def player_turn(self):
            '''Runs through the various operations to coincide with the beginning of the player's turn'''

            # Increments the mana at the start of a turn only if the players do not yet begin with 10 mana
            if self.start_mana < 10:
                self.start_mana += 1

            # Sets the available mana to be the mana offered at the start of a turn
            self.set_start_mana()

            # Iterates through every container in the player's hand and...
            for container in self.player_hand_containers:

                # If the current container is empty and there are still Cards in the player's Deck...
                if container["empty"] and not self.player_deck.empty():

                    # Pull a Card from the Deck
                    card = self.player_deck.pull_card()

                    # Add the Card to the current container
                    self.add_card_to_container(card, container)

                    # Add a line that describes the Card acquisition to the update text
                    self.text += "\nPlayer pulls a " + card.name + "!"

                    # Break from the loop; a single card has now been pulled
                    break
            
            # Remove the blank line at the start of the update text
            self.text = self.text.removeprefix("\n")

            # If the text is now empty, replace it with "..."
            if self.text == "":
                self.text = "..."

            # Set the appropriate Label to display the adjusted update text
            self.text_label["text"] = self.text

            # For all the containers on the player's side of the table, set the boolean to reflect that the 
            # card currently placed there (assuming there is one) can attack
            for container in self.player_table_containers:
                container["cannot attack"] = False
            
            # Enter the "nothing selected" state
            self.nothing_selected()
        
        def add_card_to_container(self, card, container):
            '''Adds a Card object to any container
            
            Parameters:
                card: the Card object to be placed
                container: the container into which the Card will be placed
            '''

            # Sets the container to indicate that it is not empty
            container["empty"] = False

            # Sets the image of the button to the image of the Card
            container["button"]["image"] = card.image

            # Sets the card key to point to the Card object
            container["card"] = card

            # Sets the card text to reflect the text of the Card
            container["card text"]["text"] = card.text

        def add_card_to_table(self, card, container):
            '''Adds a Card object specifically to a table container.
            
            Parameters:
                card: the Card object to be placed
                container: the container into which the Card will be placed
                '''

            # If the player is placing a Card on their side of the table...
            if container in self.player_table_containers:

                # Add a new line to the update text that indicates what Card the player is placing
                self.text += "\nPlayer plays " + card.name + "!"
            
            # If the opponent is placing a Card on their side of the table...
            else:

                # Add a new line to the update text that indicates what Card the opponent is placing
                self.text += "\nOpponent plays " + card.name + "!"
            
            # Show the new update text in the appropriate Label on the screen
            self.text_label["text"] = self.text
            
            # Add the card to the container
            self.add_card_to_container(card, container)
            
            # Reduce the available mana (not the mana the player begins their turn with) by the cost of the 
            # placed Card
            self.change_mana(-1 * card.cost)
        
        def player_add_card_to_table(self, from_container, to_container):
            '''Adds a Card object specifically from a container in the player's hand to a container 
            on the player's side of the table
            
            Parameters:
                from_container: the container in the player's hand from which to take the Card object
                to_container: the container on the player's side of the table in which to place the 
                              Card object
            '''

            # Adds the Card object to the specified table container
            self.add_card_to_table(from_container["card"], to_container)

            # Set the container into which the Card was just placed to be unable to attack
            to_container["cannot attack"] = True

            # Empty the container in the player's hand from which the Card was taken
            self.empty_player_hand_container(from_container)
            
            # Enter the "nothing selected" state
            self.nothing_selected()

        def empty_player_hand_container(self, container):
            '''Empties the specified container in the player's hand'''

            # Sets the keys of the container dictionary to point to values appropriate for 
            # an empty container within the player's hand
            container["empty"] = True
            container["button"]["image"] = self.empty_image
            container["button"]["state"] = "disabled"
            container["card"] = None
            container["card text"]["text"] = ""
        
        def empty_player_table_container(self, container):
            '''Empties the specified container on the player's side of the table'''

            # Sets the keys of the container dictionary to point to values appropriate for 
            # an empty container on the player's side of the table 
            container["empty"] = True
            container["button"]["image"] = self.place_image
            container["button"]["state"] = "disabled"
            container["card"] = None
            container["card text"]["text"] = ""
        
        def empty_opponent_table_container(self, container):
            '''Empties the specified container on the opponent's side of the table'''

            # Sets the keys of the container dictionary to point to values appropriate for 
            # an empty container on the opponent's side of the table
            container["empty"] = True
            container["button"]["image"] = self.empty_image
            container["button"]["state"] = "disabled"
            container["card"] = None
            container["card text"]["text"] = ""

        def attack_card(self, attacking_container, defending_container):
            '''Has the Card contained in the 'attacking_container' attack the Card contained in
               the 'defending_container'
            '''

            # Stores whether it is the player making the attack
            player_is_attacking = None
            if attacking_container in self.player_table_containers:
                player_is_attacking = True
            else:
                player_is_attacking = False

            # Obtains the Card that will be defending and the one that will be attacking
            defending_card = defending_container["card"]
            attacking_card = attacking_container["card"]
            
            # Lowers the HP of both Cards by the attack value of the other
            defending_card.HP -= attacking_card.attack
            attacking_card.HP -= defending_card.attack

            # Sets the attacking container to be unable to attack; it has already attacked this turn
            attacking_container["cannot attack"] = True

            # If one of the player's Cards was attacking...
            if attacking_container in self.player_table_containers:

                # Add a new line to the update text specifying which Card was attacked with which Card and display it to the screen
                self.text += "\nPlayer attacks " + defending_card.name + " with " + attacking_card.name + "!"
                self.text_label["text"] = self.text
            
            # If one of the opponent's Cards was attacking...
            else:

                # Add a new line to the update text specifying which Card was attacked with which Card
                self.text += "\nOpponent attacks " + defending_container["card"].name + " with " + attacking_container["card"].name + "!"

            # Appropriately update both containers involved in the attack
            self.update_table_container(attacking_container)
            self.update_table_container(defending_container)

            # If it was the player attacking...
            if player_is_attacking:

            # Return to the "nothing selected" state
                self.nothing_selected()

        def least_expensive(self, list_of_cards):
            '''Returns the cost of the least expensive Card in 'list_of_cards' '''

            # Iterate through the list of Cards, finding the cheapest one
            cheapest = list_of_cards[0].cost
            for card in list_of_cards:
                if card.cost < cheapest:
                    cheapest = card.cost
            
            # Return the cost of the cheapest Card in list_of_cards
            return cheapest

        def update_table_container(self, container):
            '''Update the values associated with 'container' '''

            # If the Card in container has lost all HP...
            if container["card"].HP <= 0:

                # If the container is on the opponent's side of the table...
                if container in self.opponent_table_containers:

                    # Remove the Card from the opponent's table container
                    self.empty_opponent_table_container(container)
                
                # If the container is on the player's side of the table...
                else:

                    # Remove the Card from the player's container
                    self.empty_player_table_container(container)
            
            # If the Card in the container has not lost all HP...
            else:

                # Update the text displayed with the Card (i.e. the Card's reduced HP)
                container["card"].update_text()
                container["card text"]["text"] = container["card"].text

        def change_mana(self, dx):
            '''Changes the available mana by 'dx' '''

            # Changes the value of the available mana in the current turn
            self.mana += dx

            # Updates the mana text accordingly
            self.mana_text["text"] = "Mana: " + str(self.mana) + "/" + str(self.start_mana)
        
        def nothing_selected(self):
            '''A state in which no Card/container is selected; adjusts the function and appearance of 
               every container accordingly
            '''

            # For the containers on the player's side of the table...
            for container in self.player_table_containers:

                # If there is no Card in the container on the player's side of the table...
                if container["empty"]:

                    # Set the container to display the 'place_image', to have its button disabled,
                    # to not contain a Card, and to display no text
                    container["button"]["image"] = self.place_image
                    container["button"]["state"] = "disabled"
                    container["button"]["command"] = None
                    container["card"] = None
                    container["card text"]["text"] = ""
                
                # If there is a Card in the container on the player's side of the table, but it cannot attack...
                elif not container["empty"] and container["cannot attack"]:

                    # Set the container to display the image of its Card, to have its button disabled,
                    # to contain its own Card, and to display its Card's text
                    container["button"]["image"] = container["card"].image
                    container["button"]["state"] = "disabled"
                    container["button"]["command"] = None
                    container["card"] = container["card"]
                    container["card text"]["text"] = container["card"].text
                
                # If there is a Card in the container on the player's side of the table, and it can attack...
                else:

                    # Set the container to display the image of its Card, to have its button enter into the 
                    # card_on_table_selected state, to contain its own Card, and to display its Card's text
                    container["button"]["image"] = container["card"].image
                    container["button"]["state"] = "active"
                    container["button"]["command"] = partial(self.card_on_table_selected, container)
                    container["card"] = container["card"]
                    container["card text"]["text"] = container["card"].text
            
            # For the containers on the opponent's side of the table...
            for container in self.opponent_table_containers:

                # If there is no Card in the container on the opponent's side of the table...
                if container["empty"]:

                    # Set the container to display the 'empty_image', to have its button disabled,
                    # to not contain a Card, and to display no text
                    container["button"]["image"] = self.empty_image
                    container["button"]["state"] = "disabled"
                    container["button"]["command"] = None
                    container["card"] = None
                    container["card text"]["text"] = ""
                
                # If there is a Card in the container on the opponent's side of the table...
                else:

                    # Set the container to display the image of its Card, to have its button disabled,
                    # to contain its own Card, and to display the text of its Card
                    container["button"]["image"] = container["card"].image
                    container["button"]["state"] = "disabled"
                    container["button"]["command"] = None
                    container["card"] = container["card"]
                    container["card text"]["text"] = container["card"].text
            
            # For the containers in the player's hand...
            for container in self.player_hand_containers:

                # If there is no Card in the container in the player's hand...
                if container["empty"]:

                    # Set the container to display the 'empty_image', to have its button disabled,
                    # to not contain a Card, and to display no text
                    container["button"]["image"] = self.empty_image
                    container["button"]["state"] = "disabled"
                    container["button"]["command"] = None
                    container["card"] = None
                    container["card text"]["text"] = ""
                
                # If there is a Card in the container in the player's hand, and the player can afford to place it...
                elif not container["empty"] and self.mana >= container["card"].cost:

                    # Set the container to display the image of its Card, to have its button enter into the 
                    # 'card_in_hand_selected' state, to contain its own Card, and to display the text of its Card
                    container["button"]["image"] = container["card"].image
                    container["button"]["state"] = "active"
                    container["button"]["command"] = partial(self.card_in_hand_selected, container)
                    container["card"] = container["card"]
                    container["card text"]["text"] = container["card"].text
                
                # If there is a Card in the container in the player's hand, but the player cannot afford to place it...
                else:

                    # Set the container to display the image of its Card, to have its button disabled,
                    # to contain its own Card, and to display the text of its Card
                    container["button"]["image"] = container["card"].image
                    container["button"]["state"] = "disabled"
                    container["button"]["command"] = None
                    container["card"] = container["card"]
                    container["card text"]["text"] = container["card"].text

            # Set the opponent's portrait (the picture of the eye) to be disabled, not performing any functions
            self.opponent["button"]["command"] = None
            self.opponent["button"]["state"] = DISABLED

            # Set the player's portrait (the picture of the bunny) to be disabled, not performing any functions
            self.player["button"]["command"] = None
            self.player["button"]["state"] = DISABLED

            # Activate the button to end the turn
            self.end_turn_button["state"] = "active"

        def card_in_hand_selected(self, selected_container):
            '''A state in which a Card/container in the player's hand is selected; adjusts the function and 
               appearance of every container accordingly

               Parameters:
                    selected_container - The container in the player's hand that has been selected
            '''

            # For the containers on the player's side of the table
            for container in self.player_table_containers:

                # If there is no Card in the container on the player's side of the table...
                if container["empty"]:

                    # Set the container to display the 'place_image', to have its button place the card of the selected container
                    # in the player's hand into the selected container on the player's side of the table, to not contain a Card,
                    # and to display no text
                    container["button"]["image"] = self.place_image
                    container["button"]["state"] = "active"
                    container["button"]["command"] = partial(self.player_add_card_to_table, selected_container, container)
                    container["card"] = None
                    container["card text"]["text"] = ""
                
                # If there is a Card in the container on the player's side of the table...
                else:

                    # Set the container to display the image of its Card, to have its button disabled,
                    # to contain its own Card, and to display the text of its Card
                    container["button"]["image"] = container["card"].image
                    container["button"]["state"] = "disabled"
                    container["button"]["command"] = None
                    container["card"] = container["card"]
                    container["card text"]["text"] = container["card"].text
            
            # For the containers on the opponent's side of the table...
            for container in self.opponent_table_containers:

                # If there is no Card in the container on the opponent's side of the table...
                if container["empty"]:

                    # Set the container to display the 'empty_image', to have its button disabled,
                    # to not contain a Card, and to display no text
                    container["button"]["image"] = self.empty_image
                    container["button"]["state"] = "disabled"
                    container["button"]["command"] = None
                    container["card"] = None
                    container["card text"]["text"] = ""
                
                # If there is a Card in the container on the opponent's side of the table...
                else:

                    # Set the container to display image of its Card, to have its button disabled,
                    # to contain its own Card, and to display the text of its Card
                    container["button"]["image"] = container["card"].image
                    container["button"]["state"] = "disabled"
                    container["button"]["command"] = None
                    container["card"] = container["card"]
                    container["card text"]["text"] = container["card"].text
            
            # For the containers in the player's hand...
            for container in self.player_hand_containers:

                # If there is no Card in the container in the player's hand...
                if container["empty"]:

                    # Set the container to display the 'empty_image', to have its button disabled,
                    # to not contain a Card, and to display no text
                    container["button"]["image"] = self.empty_image
                    container["button"]["state"] = "disabled"
                    container["button"]["command"] = None
                    container["card"] = None
                    container["card text"]["text"] = ""
                
                # If there is a Card in the container in the player's hand and it is not the selected container...
                elif not container["empty"] and container != selected_container:

                    # Set the container to display the image of its Card, to have its button disabled,
                    # to contain its own Card, and to display the text of its Card
                    container["button"]["image"] = container["card"].image
                    container["button"]["state"] = "disabled"
                    container["button"]["command"] = None
                    container["card"] = container["card"]
                    container["card text"]["text"] = container["card"].text

                # If the container in the player's hand is the selected container...
                else:

                    # Set the container to display the image of its Card, to have its button enter into the 
                    # 'nothing_selected' state, to contain its own Card, and to display the text of its Card
                    container["button"]["image"] = container["card"].selected_image
                    container["button"]["state"] = "active"
                    container["button"]["command"] = self.nothing_selected
                    container["card"] = container["card"]
                    container["card text"]["text"] = container["card"].text

            # Disable the button that ends the turn
            self.end_turn_button["state"] = "disabled"
        
        def card_on_table_selected(self, selected_container):
            '''A state in which a Card/container on the player's side of the table is selected; adjusts the function
               and appearance of every container accordingly

               Parameters:
                    selected_container - The container on the player's side of the table that has been selected
            '''

            # For the containers on the player's side of the table...
            for container in self.player_table_containers:

                # If there is no Card in the container on the player's side of the table...
                if container["empty"]:

                    # Set the container to display the 'place_image', to have its button disabled,
                    # to not contain a Card, and to display no text
                    container["button"]["image"] = self.place_image
                    container["button"]["state"] = "disabled"
                    container["button"]["command"] = None
                    container["card"] = None
                    container["card text"]["text"] = ""
                
                # If there is a Card in the container on the player's side of the table and it is not the selected 
                # container...
                elif not container["empty"] and container != selected_container:

                    # Set the container to display the image of its Card, to have its button attack the second-selected
                    # container with the first-selected, to contain its own Card, and to display the text of its Card
                    container["button"]["image"] = container["card"].image
                    container["button"]["state"] = "active"
                    container["button"]["command"] = partial(self.attack_card, selected_container, container)
                    container["card"] = container["card"]
                    container["card text"]["text"] = container["card"].text

                # If the container on the player's side of the table is the selected container...
                else:

                    # Set the container to display the image of its Card, to have its button enter into the 
                    # 'nothing_selected' state, to contain its own Card, and to display the text of its Card
                    container["button"]["image"] = container["card"].selected_image
                    container["button"]["state"] = "active"
                    container["button"]["command"] = self.nothing_selected
                    container["card"] = container["card"]
                    container["card text"]["text"] = container["card"].text
            
            # For the containers on the opponent's side of the table...
            for container in self.opponent_table_containers:

                # If there is no Card in the container on the opponent's side of the table...
                if container["empty"]:

                    # Set the container to display the 'empty_image', to have its button disabled,
                    # to not contain a Card, and to display no text
                    container["button"]["image"] = self.empty_image
                    container["button"]["state"] = "disabled"
                    container["button"]["command"] = None
                    container["card"] = None
                    container["card text"]["text"] = ""
                
                # If there is a Card in the container on the opponent's side of the table...
                else:

                    # Set the container to display the image of its Card, to have its button attack the second-selected
                    # container with the first-selected, to contain its own Card, and to display the text of its Card
                    container["button"]["image"] = container["card"].image
                    container["button"]["state"] = "active"
                    container["button"]["command"] = partial(self.attack_card, selected_container, container)
                    container["card"] = container["card"]
                    container["card text"]["text"] = container["card"].text
            
            # For the containers in the player's hand...
            for container in self.player_hand_containers:

                # If there is no Card in the container in the player's hand...
                if container["empty"]:

                    # Set the container to display the 'empty_image', to have its button disabled,
                    # to not contain a Card, and to display no text
                    container["button"]["image"] = self.empty_image
                    container["button"]["state"] = "disabled"
                    container["button"]["command"] = None
                    container["card"] = None
                    container["card text"]["text"] = ""
                
                # If there is a Card in the container in the player's hand...
                else:

                    # Set the container to display the image of its Card, to have its button disabled,
                    # to contain its own Card, and to display the text of its Card
                    container["button"]["image"] = container["card"].image
                    container["button"]["state"] = "disabled"
                    container["button"]["command"] = None
                    container["card"] = container["card"]
                    container["card text"]["text"] = container["card"].text

            # Activate the portrait of the opponent (the image of the eye) to have the selected container attack
            # the opponent
            self.opponent["button"]["state"] = ACTIVE
            self.opponent["button"]["command"] = partial(self.attack_person, selected_container, self.opponent)

            # Activate the portrait of the player (the image of the bunny) to have the selected container attack
            # the player
            self.player["button"]["state"] = ACTIVE
            self.player["button"]["command"] = partial(self.attack_person, selected_container, self.player)

            # Disable the button that ends the turn
            self.end_turn_button["state"] = "disabled"

        def set_start_mana(self):
            '''Sets the available mana to the mana offered at the start of the turn'''

            # Sets the available mana to the mana offered at the start of the turn
            self.mana = self.start_mana

            # Updates the mana text accordingly
            self.mana_text["text"] = "Mana " + str(self.mana) + "/" + str(self.start_mana)

        def opponent_turn(self):
            '''Outlines the automated processes for the computer-controlled opponent during their turn'''

            # Resets the update text
            self.text = ""

            # If there is room in the opponent's hand for Cards and their Deck is not empty...
            if len(self.opponent_hand) < 5 and not self.opponent_deck.empty():

                # Pull a Card from the opponent's Deck and add it to their hand
                self.opponent_hand.append(self.opponent_deck.pull_card())
            
            # Iterates through the containers on the opponent's side of the table and attacks pseudo-randomly
            self.opponent_iterate_through_table()

            # Pseudo-randomly plays Cards from the opponent's hand
            self.opponent_play_cards()
            
            # Start another player turn at the end of the opponent's turn
            self.player_turn()
        
        def opponent_iterate_through_table(self):
            '''Iterates through the containers on the opponent's side of the table and attacks player figures 
               pseudo-randomly
            '''

            # For the containers on the opponent's side of the table...
            for container in self.opponent_table_containers:

                # If there is a Card in the container...
                if not container["empty"]:

                    # Creates a list of the figures that the container could potentially attack
                    defenders = self.get_list_of_defenders()

                    # Randomly selectes a figure to attack from the list of potential defenders
                    defender = r.choice(defenders)

                    # If one of the containers on the player's side of the table was randomly chosen to attack...
                    if defender != self.player:

                        # Attack the player's container with the opponent's container
                        self.attack_card(container, defender)

                    # If the player themselves was randomly chosen to attack...
                    else:

                        # Attack the player with the container on the opponent's side of the table                        
                        self.attack_person(container, defender)

        def opponent_play_cards(self):
            '''Pseudo-randomly plays Cards from the opponent's hand'''

            # Sets the mana available to the opponent to the value of mana at the start of a turn
            self.mana = self.start_mana

            # While the mana available to the opponent is greater than or equal to the cheapest Card in their hand
            # and there is still space left on the opponent's side of the table...
            while self.mana >= self.least_expensive(self.opponent_hand) and self.space_left(self.opponent_table_containers):

                # Randomly select a Card in the opponent's hand
                card = r.choice(self.opponent_hand)

                # Randomly select a container on the opponent's side of the table
                container = r.choice(self.opponent_table_containers)

                # If the opponent can afford the Card and the container on their side of the table is empty...
                if card.cost <= self.mana and container["empty"]:

                    # Add the Card from the opponent's hand to the empty container on their side of the table
                    self.add_card_to_table(card, container)
        
        def space_left(self, list_of_containers):
            '''Returns True if there is at least one empty container in 'list_of_containers', False otherwise'''

            # For the containers in the provided list of containers...
            for container in list_of_containers:

                # If the container is empty, return True
                if container["empty"]:
                    return True

            # Return False if there are no empty containers
            return False

        def get_list_of_defenders(self):
            '''Returns a list of the figures that the opponent could potentially attack'''

            # Instantiates an empty list
            list = []

            # For the containers on the player's side of the table...
            for container in self.player_table_containers:

                # If the container has a Card...
                if not container["empty"]:

                    # Append the container on the player's side of the table to the list of potential defenders
                    list.append(container)
            
            # Append the player themselves to the list of potential defenders
            list.append(self.player)

            # Return the list of potential defenders
            return list
        
        def attack_person(self, attacking_container, defending_person):
            '''Attacks either the player or the opponent themselves (the 'defending_person') with 
               the 'attacking_container' 
            '''

            # Stores whether or not it is the player that is attacking
            player_is_attacking = None
            if attacking_container in self.player_table_containers:
                player_is_attacking = True
            else:
                player_is_attacking = False

            # Obtains the Card that is attacking
            attacking_card = attacking_container["card"]

            # Finds the new HP of the entity being attacked (either the player or the opponent themselves) 
            # following the attack and updates the text accordingly
            new_HP = int(defending_person["HP"]["text"]) - attacking_card.attack
            defending_person["HP"]["text"] = str(new_HP)

            # Sets the container that attacked to be unable to attack for the rest of the turn
            attacking_container["cannot attack"] = True

            # If it was the player that attacked...
            if attacking_container in self.player_table_containers:

                # Adds a new line to the update text reflecting the player's attack, and displays the text
                self.text += "\nPlayer attacks the opponent with " + attacking_card.name + "!"
                self.text_label["text"] = self.text
            
            # If it was the opponent that attacked...
            else:
                # Adds a new line to the update text reflecting the opponent's attack
                self.text += "\nOpponent attacks the player with " + attacking_card.name + "!"
            
            # Checks if the attacked entity's HP has been reduced to or below 0 and proceeds accordingly
            self.update_person(defending_person)

            # If the player was attacking, return to the 'nothing_selected' state
            if player_is_attacking:
                self.nothing_selected()

        def update_person(self, person):
            '''Check if the HP of 'person' (the player or the opponent) has been reduced to 0 and display
               the correct screen if so
            '''

            # If the HP of the player or opponent has been reduced to or below 0...
            if int(person["HP"]["text"]) <= 0:

                # If the checked entity is the opponent...
                if person == self.opponent:

                    # Display the victory screen
                    Application.Win()
                
                # If the checked entity is the player...
                else:

                    # Display the loss screen
                    Application.Lose()

    class Win:
        '''Class for the Win "state"'''

        def __init__(self):
            '''The constructor of the Win class'''
            
            # Sets up the Win screen
            self.setup()
        
        def setup(self):
            '''Initializes the various tkinter widgets that constitute a Win screen'''

            # Removes every widget currently drawn to the tkinter window
            for widget in Application.root.winfo_children():
                widget.destroy()
            
            # Places a Label with text "You Win!" in the window
            t.Label(Application.root, text="You Win!").pack()

            # Places a button that allows the user to play again in the window
            play_button = t.Button(Application.root, text="Play Again!", command=self.play, bg="black", fg="white")
            play_button.pack()

            # Places a button that allows the user to exit the entire program to the window
            exit_button = t.Button(Application.root, text="Exit", command=Application.root.destroy, bg="black", fg="white")
            exit_button.pack()

        def play(self):
            '''Begins another Game from the Win screen'''

            # Instantiates a Game, taking the user to the Game "screen"
            Application.Game()

    class Lose:
        '''Class for the Lose "state"'''

        def __init__(self):
            '''The constructor of the Lose class'''

            # Sets up the Lose screen
            self.setup()
        
        def setup(self):
            '''Initializes the various tkinter widgets that constitute a Lose screen'''

            # Removes every widget currently drawn to the tkinter window
            for widget in Application.root.winfo_children():
                widget.destroy()
            
            # Places a Label with text "You Lose..." in the window
            t.Label(Application.root, text="You Lose...").pack()

            # Places a button that allows the user to play again in the window
            play_button = t.Button(Application.root, text="Try Again?", command=self.play, bg="black", fg="white")
            play_button.pack()

            # Places a button that allows the user to exit the entire program in the window
            exit_button = t.Button(Application.root, text="Exit", command=Application.root.destroy, bg="black", fg="white")
            exit_button.pack()

        def play(self):
            '''Begins another Game from the Lose screen'''

            # Instantiates a Game, taking the user to the Game "screen"
            Application.Game()

# If game.py is executed directly...
if __name__ == "__main__":
    
    # Instantiate the Application
    Application()