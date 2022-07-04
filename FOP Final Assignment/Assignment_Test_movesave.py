import numpy
import Assignment
import random
import os

# Changeable variables
fieldsize = [20,20]
n_food = 35 #plants (Green)
chance_xxx = 20
chance_spread = 5
starting_hunger = random.randint(10, 15)
when_eat = 10
width, height = 750, 750
max_it = 100
max_animal_total = 50
directory =  r'C:\Users\diamo\OneDrive\Desktop\Programming Assignment\Simulation_Results'
file_start_name = 'test.csv'

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
            location_array = numpy.ndarray((fieldsize[0], fieldsize[1]), dtype=object)

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
