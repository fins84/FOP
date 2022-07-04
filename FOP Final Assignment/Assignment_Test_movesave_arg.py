import numpy
import Assignment
import random
import os
import sys

# Changeable variables
fieldsize = [sys.argv[1],sys.argv[2]]
n_food = sys.argv[3] #plants (Green)
chance_xxx = sys.argv[4]
chance_spread = sys.argv[5]
starting_hunger = random.randint(sys.argv[6], sys.argv[7])
when_eat = sys.argv[8]
max_it = sys.argv[9]
max_animal_total = sys.argv[10]
directory =  sys.argv[11]
file_start_name = sys.argv[12]

for an_1 in range(0,max_animal_total+1):
    for an_2 in range(0, max_animal_total - an_1 +1):
        for an_3 in range(0,max_animal_total - an_1 - an_1 + 1):
            print(an_1, an_2, an_3)
            filenames = (file_start_name + '-'+str(an_1) + '-' + str(an_2) + '-'+str(an_3))
            print(filenames)
            filename = open(os.path.join(directory,filenames), 'w')
            n_animal_1 = an_1  # Herbivore
            n_animal_2 = an_2  # Carnivore
            n_animal_3 = an_3  # Omnivore

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
            Assignment.savework(filename, Assignment.objar2numar(location_array, fieldsize), counter )
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
                        elif x.type == 'food' and x.turn == counter:
                            x.spread(location_array, chance_spread)
                            x.update_turn()
                            x.increase_value()
                counter +=1
                total = 0
                animal_n_list = Assignment.getancount(location_array)
                print(animal_n_list)
                brat = 0
                Assignment.savework(filename, Assignment.objar2numar(location_array, fieldsize), counter)

                if animal_n_list['Animal_1'] == 0 and animal_n_list['Animal_2'] == 0 and animal_n_list['Animal_3'] == 0:
                    break


            filename.close()
