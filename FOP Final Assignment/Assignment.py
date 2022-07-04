import random
import numpy
import math
import csv
import pygame

def gencoordinates(fieldsize): #generating a random x and y value between 0 and the max x and y fieldsize
    x = random.randint(0, fieldsize[0]-1)
    y = random.randint(0, fieldsize[1]-1)
    return x, y
def genfood(n_food, location_array, fieldsize): #generates the location of food for omnivores and herbivores
    c = 0
    #making sure that all food is generated
    while c != n_food:
        x, y = gencoordinates(fieldsize)
        #checking to that the x y coordinates in the location array is empty
        if location_array[y][x] is None:
            location = [y, x]
            #Generating food at empty location
            location_array[y][x] = food(location)
            c += 1
def genanimal(n_animal, location_array, fieldsize, animal, subtype, hunger): #generates animal(1,2,3) randomly in location array
    c = 0
    #making sure all animals are generated using while loop
    while c != n_animal:
        x, y = gencoordinates(fieldsize)
        #checking to see if the x y coordinates generated is empty
        if location_array[y][x] is None:
            location = [y, x]
            #Generating animal at empty location
            location_array[y][x] = animal(location, hunger, subtype)
            c += 1
def objar2numar(location_array, fieldsize):
    '''
    converts location array (the array holding the objects) to a list of numbers representing each of the animal
    This allows for data to be stored in a csv file

    Animal 1 = 1
    Animal 2 = 2
    Animal 3 = 3
    Food = 4
    '''
    printscrn = numpy.zeros((fieldsize[0], fieldsize[1]), dtype=int)
    #creating a array of integers

    for y in location_array:
        for x in y:
            if x is None:
                pass
            elif x.type == 'animal':
                if x.subtype == 'animal_1':
                    printscrn[x.current[0]][x.current[1]] = 1
                elif x.subtype == 'animal_2':
                    printscrn[x.current[0]][x.current[1]] = 2
                elif x.subtype == 'animal_3':
                    printscrn[x.current[0]][x.current[1]] = 3
            elif x.type == 'food':
                printscrn[x.location[0]][x.location[1]] = 4

    return(printscrn)
def getancount(location_array):
    '''
    creates a easier way to tell how many of each animal and food is still 'alive'
    does this by iterating through the location array and for each animal/food it sees, adds 1 to the corresponding
    animal key in the dictionary
    '''
    animal_count = {'Animal_1': 0, 'Animal_2': 0, 'Animal_3':0, 'Food': 0}
    for y in location_array:
        #for line in location array
        for x in y:
            #for individual index in line
            if x is None:
                pass
            elif x.type == 'animal':
                if x.subtype == 'animal_1':
                    animal_count['Animal_1'] += 1
                if x.subtype == 'animal_2':
                    animal_count['Animal_2'] += 1
                if x.subtype == 'animal_3':
                    animal_count['Animal_3'] += 1
            elif x.type == 'food':
                animal_count['Food'] += 1
    return animal_count
def savework(filename, content, counter):
    file = csv.writer(filename)
    file.writerows(content)
    file.writerow([counter])
def display(width, height, fieldsize, x, background):
    division_y = int(height/fieldsize[0])
    division_x = int(width/fieldsize[1])
    if x.type == 'animal':
        if x.subtype == 'animal_1':
            pygame.draw.rect(background,(242,193,78), (division_x * x.current[1], division_y * x.current[0], division_x, division_y))
        elif x.subtype == 'animal_2':
            pygame.draw.rect(background,(247, 129, 84), (division_x * x.current[1], division_y * x.current[0], division_x, division_y))
        elif x.subtype == 'animal_3':
            pygame.draw.rect(background, (180, 67, 108),(division_x * x.current[1], division_y * x.current[0], division_x, division_y))
    elif x.type == 'food':
        pygame.draw.rect(background, (95, 173, 86), (division_x * x.location[1], division_y * x.location[0], division_x, division_y))

class food():
    #Food in reality is just plants substance for omnivores and herbivores to eat
    def __init__(self, location):
        self.location = location
        self.value = 4
        self.type = 'food'
        self.subtype = 'food'
        #have subtype and type being food so it doesn't raise an error if other code accidently thinks its type is food
        self.turn = 0
        #Turn makes sure that in each timestep, the food/animal is only iterated over once
    def spread(self, location_array, chance_spread):
        '''
        has a chance to generate another food around itself
        first finds empty tiles surrounding itself
        '''
        y = self.location[0]
        x = self.location[1]
        empty_tile = []
        for j in range(y-1, y+2):
            for i in range(x-1, x+2):
                if [j,i] == [y, x]:
                    pass
                elif i in range(0, len(location_array)-1) and j in range(0, len(location_array)-1) and location_array[j][i] is None:
                    empty_tile.append([j, i])
        #uses randrange to generate a number and if that number is within a certain bounds, it generates food (and does other checks)
        if random.randrange(0, 101) < chance_spread and len(empty_tile) > 0 and self.value >= 2:
            choice = random.choice(empty_tile)
            location_array[choice[0]][choice[1]] = food(choice)
            location_array[choice[0]][choice[1]].turn = self.turn
    def increase_value(self):
        '''
        value is how much it replenishes the animals hunger when eaten
        increases by 1 every turn
        '''
        if self.value <= 7:
            self.value += 1
    def update_turn(self):
        '''
        makes sure that it doesn't do multiple actions in 1 timestep
        '''
        self.turn += 1
class animal_master():
    def __init__(self, position, hunger, subtype):
        self.current = position
        self.hunger = hunger
        self.type = 'animal'
        self.subtype = subtype
        self.turn = 0
        self.t_since_last_xxx = 1
        self.no_move = 0
    def update_self(self, location_array):
        '''
        updates timestep based variables like time_since_last_xxx (last procreation) and hunger
        '''
        if self.t_since_last_xxx != 0:
            self.t_since_last_xxx += 1
        self.hunger -= 1
        if self.hunger <= 0 or self.no_move == 2:
            location_array[self.current[0]][self.current[1]] = None
    def procreate(self, location_array, chance_xxx): #can only procreate once per x turns
        nearbye = []
        empty = []

        #splits and converts the current location of the object to shorter and easier to type variables
        x = self.current[1]
        y = self.current[0]

        #Checks to see if hunger is greater than a certain point and that it hasn't procreated in a certain time frame
        if self.hunger >= 5 and self.t_since_last_xxx >= 5:
            #iterates through the location array and appends empty tiles around the objects current location
            for j in range(y-1, y+2):
                for i in range(x-1, x+2):
                    if [j, i] == [y, x]:
                        pass
                    elif i in range(0, len(location_array[0])) and j in range(0, len(location_array)):
                        if location_array[j][i] is None:
                            empty.append([j, i])
                        elif location_array[j][i].type == 'animal':
                            if location_array[j][i].subtype == self.subtype and location_array[j][i].hunger >= 5:
                                nearbye.append([j, i])


            '''checks chance to procreate and then checks if required parameters are met(nearbye animals of same type
            and empty tiles nearbye)
            '''
            if len(nearbye) >= 1 and random.randint(0,100) <= chance_xxx and len(empty) > 0:
                choice_xxx = random.choice(nearbye)
                location_array[choice_xxx[0]][choice_xxx[1]].t_since_last_xxx = 0
                location_array[choice_xxx[0]][choice_xxx[1]].hunger -= 3
                self.hunger -= 3
                self.t_since_last_xxx = 0
                '''updates hunger of parent animals(when procreate, subtracts some hunger) and also resets the counter 
                for time_since_last_xxx
                '''
                location_baby = random.choice(empty)
                #Checks which type of animal is procreating and then creates a 'baby' of that type near the parent
                if self.subtype == 'animal_1':
                    location_array[location_baby[0]][location_baby[1]] = animal_1(location_baby, 5, 'animal_1')
                    location_array[location_baby[0]][location_baby[1]].turn = self.turn
                if self.subtype == 'animal_2':
                    location_array[location_baby[0]][location_baby[1]] = animal_2(location_baby, 5, 'animal_2')
                    location_array[location_baby[0]][location_baby[1]].turn = self.turn
                if self.subtype == 'animal_3':
                    location_array[location_baby[0]][location_baby[1]] = animal_3(location_baby, 5, 'animal_3')
                    location_array[location_baby[0]][location_baby[1]].turn = self.turn
class animal_1(animal_master):
    # herbivore animal (only eats 'food')
    def movement(self, location_array, when_eat):
        '''
        Movement of animal_1 encompasses both moving and eating
        Priorities of moving and eating are as follow:
        1. If hunger is below a certain threshold, look for and eat food
        2. Move to a random tile in a 1 block radius around its current position
        '''

        # splits object's current location to easier to type variables
        x = self.current[1]
        y = self.current[0]
        movement = []

        # adds tiles in a 1 block radius around the current location to a list (also checking if in bounds of 'arena'
        for j in range(y-1, y+2):
            for i in range(x-1, x+2):
                if [j,i] == [y, x]:
                    pass
                elif i in range(0, len(location_array[0])) and j in range(0, len(location_array)):
                    movement.append([j, i])

        choices = []
        eat_tile = []
        move = []
        # checks to see what is in the tiles nearbye and takes note of where the food and empty tiles are
        for points in movement:
            if location_array[points[0]][points[1]] is None:
                choices.append(points)
            elif location_array[points[0]][points[1]].subtype == 'food':
                eat_tile.append(points)

        if len(eat_tile) >= 1 and self.hunger <= when_eat:
            # Animal 1 has a long reach therefore, when eating food, can eat adjacent tile without moving to it
            move = random.choice(eat_tile)
            self.hunger += location_array[move[0]][move[1]].value
            location_array[move[0]][move[1]] = None
            self.turn += 1
            self.no_move = 0
        elif len(choices) > 0:
            # checks to see if there are empty tiles otherwise doesn't move anywhere
            move = random.choice(choices)
            location_array[y][x], location_array[move[0]][move[1]] = location_array[move[0]][move[1]],  location_array[y][x]
            self.current = move
            self.turn += 1
            self.no_move = 0
        elif len(move) == 0:
            self.no_move += 1
            self.turn += 1
        return location_array
class animal_2(animal_master): # carnivore animal eats both animal 1 and 3
    def movement(self, location_array, when_eat):
        '''
            Movement of animal_2 encompasses both moving and eating
            Priorities of moving and eating are as follow:
            1. If hunger is below a certain threshold, look for and eat food or animal 1/3 to eat
            2. Move to a random tile around current position that is two blocks away
        '''
        x = self.current[1]
        y = self.current[0]
        # splits current location in to easy to type variables
        movement = []

        # adds tiles in side arena boundary that is 2 tiles away from the current position
        for j in range(y-2, y+3):
            for i in range(x-2, x+3):
                if [j,i] == [y, x]:
                    pass
                elif i in range(0, len(location_array[0])) and j in range(0, len(location_array)):
                    if math.sqrt((j-y)**2 + (i-x)**2) > 1.5:
                        movement.append([j, i])

        choices = []
        eat_tile = []
        move = []

        # Sorts the tiles depending on whether they are empty or contain animal 1/3
        for points in movement:
            if location_array[points[0]][points[1]] is None:
                choices.append(points)
            elif location_array[points[0]][points[1]].subtype == 'animal_1' or location_array[points[0]][points[1]].subtype == 'animal_3':
                eat_tile.append(points)

        # Checks to see that animal 2 is hungery and that there is food near by
        if len(eat_tile) >= 1 and self.hunger <= when_eat:
            move = random.choice(eat_tile)
            self.hunger += location_array[move[0]][move[1]].hunger + 2
            location_array[move[0]][move[1]] = None
            location_array[y][x], location_array[move[0]][move[1]] = location_array[move[0]][move[1]], location_array[y][x]
            self.current = move
            self.no_move = 0
            self.turn += 1

        # Checks to see if there are empty tiles around
        elif len(choices) >= 1:
            move = random.choice(choices)
            location_array[y][x], location_array[move[0]][move[1]] = location_array[move[0]][move[1]],  location_array[y][x]
            self.current = move
            self.no_move = 0
            self.turn += 1
        elif len(move) == 0:
            self.no_move += 1
            self.turn += 1
        return location_array
class animal_3(animal_master): #omnivore animal eats animal 1 and food
    def movement(self, location_array, when_eat):
        '''
            Movement of animal_2 encompasses both moving and eating
            Priorities of moving and eating are as follow:
            1. If hunger is below a certain threshold, look for and eat food or animal 1 to eat
            2. Move to a random tile either up, down, left or right from current position
        '''

        #Splits current location into shorter, easier to type variables
        x = self.current[1]
        y = self.current[0]

        movement = []
        # Gets the tiles to the top and bottom of current location
        for j in range(y-1, y+2, 2):
            if j in range(0, len(location_array)):
                movement.append([j, x])

        # Gets the tile to the left and right of current location
        for i in range(x-1, x+2, 2):
            if i in range(0, len(location_array)):
                movement.append([y, i])

        choices = []
        eat_tile = []
        move = []

        # checks location array for what is in close by tiles and sorts them accordingly
        for points in movement:
            if location_array[points[0]][points[1]] is None:
                choices.append(points)
            elif location_array[points[0]][points[1]].subtype == 'animal_1' or location_array[points[0]][points[1]].subtype == 'food':
                eat_tile.append(points)

        # If animal is hungry and nearbye food, then eat
        if len(eat_tile) >= 1 and self.hunger <= when_eat: #short reach, therefore when eating food or animal, move to tile
            move = random.choice(eat_tile)
            if location_array[move[0]][move[1]].subtype == 'animal_1':
                self.hunger += location_array[move[0]][move[1]].hunger + 4
            elif location_array[move[0]][move[1]].type == 'food':
                self.hunger += location_array[move[0]][move[1]].value
            location_array[move[0]][move[1]] = None
            location_array[y][x], location_array[move[0]][move[1]] = location_array[move[0]][move[1]], location_array[y][x]
            self.current = move
            self.turn += 1
        # If not hungry or no nearbye food, move to a empty tile
        elif len(choices) >= 1:
            move = random.choice(choices)
            location_array[y][x], location_array[move[0]][move[1]] = location_array[move[0]][move[1]],  location_array[y][x]
            self.current = move
            self.turn += 1

        # Don't move if no empty adjacent tiles
        elif len(move) == 0:
            self.turn += 1
        return location_array


##To do
'''
- If you have time, try an implement a pathfinding algorithm to nearest food object if hungry
'''