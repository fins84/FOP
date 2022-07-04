import numpy
import Assignment
import matplotlib.pyplot as plot
import pygame
import random
import sys
# Changeable variables
fieldsize = [sys.argv[1],sys.argv[2]]
n_food = sys.argv[3] #plants (Green)
n_animal_1 = sys.argv[4] #Herbivore (Yellow)
n_animal_2 = sys.argv[5] #Carnivore (Orange)
n_animal_3 = sys.argv[6] #Omnivore (Magenta)
chance_xxx = sys.argv[7]
chance_spread = sys.argv[8]
starting_hunger = random.randint(sys.argv[9], sys.argv[10])
when_eat = sys.argv[11]
width, height = sys.argv[13], sys.argv[14]
filename = open(sys.argv[15],'w')
max_it = sys.argv[16]

# Don't touch this
location_array = numpy.ndarray((fieldsize[0],fieldsize[1]), dtype=object)

# Setting up all the starting animals and food
Assignment.genfood(n_food, location_array, fieldsize)
Assignment.genanimal(n_animal_1, location_array, fieldsize, Assignment.animal_1, 'animal_1', starting_hunger)
Assignment.genanimal(n_animal_2, location_array, fieldsize, Assignment.animal_2, 'animal_2', starting_hunger)
Assignment.genanimal(n_animal_3, location_array, fieldsize, Assignment.animal_3, 'animal_3', starting_hunger)

# This is where the array is iterated through and all the animals and food interact with eachother
# It also displays and saves the output as it goes (numbers and through the GUI in pygame window)
counter = 0
pygame.init()
screen = pygame.display.set_mode((width, height))
background = pygame.Surface((width, height))
Assignment.savework(filename, Assignment.objar2numar(location_array, fieldsize), counter)
while counter != max_it:
    print(Assignment.objar2numar(location_array, fieldsize))
    for y in location_array:
        for x in y:
            if x is None:
                pass
            elif x.type == 'animal' and x.turn == counter:
                x.movement(location_array, when_eat)
                x.update_self(location_array)
                x.procreate(location_array, chance_xxx)
                Assignment.display(width, height, fieldsize, x, background)
            elif x.type == 'food' and x.turn == counter:
                x.spread(location_array, chance_spread)
                x.update_turn()
                x.increase_value()
                Assignment.display(width, height, fieldsize, x, background)
    screen.blit(background, (0, 0))
    pygame.display.flip()
    background.fill((0, 0, 0, 0))
    pygame.time.wait(250)
    pygame.display.flip()
    counter +=1
    total = 0
    animal_n_list = Assignment.getancount(location_array)
    print(animal_n_list)
    brat = 0
    Assignment.savework(filename, Assignment.objar2numar(location_array, fieldsize), counter)
    if animal_n_list['Animal_1'] == 0 and animal_n_list['Animal_2'] == 0 and animal_n_list['Animal_3'] == 0:
        break


filename.close()
display = True
while display:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            display = False

# In case pygame not working, use this:
'''
while counter != 0:
    print(Assignment.objar2numar(location_array, fieldsize))
    plot.imshow(Assignment.objar2numar(location_array, fieldsize))
    plot.show()
    for y in location_array:
        for x in y:
            if x == None:
                pass
            elif x.type == 'animal' and x.turn == counter:
                x.movement(location_array, when_eat)
                x.update_self(location_array)
                x.procreate(location_array, chance_xxx)
            elif x.type == 'food' and x.turn == counter:
                x.spread(location_array, chance_spread)
                x.update_turn()
                x.increase_value()

    #print(location_array)
    counter +=1
'''