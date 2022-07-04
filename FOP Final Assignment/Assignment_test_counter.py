import numpy
import Assignment
import random
import os
import csv
import sys

# Changeable variables
fieldsize = [25,25]
n_food = 50
chance_xxx = 20 #chance for reproduction
chance_spread = 5 #chance for food to spread
starting_hunger = random.randint(12, 18) #starting hunger value for animals
when_eat = 10 #when the animals prioritise eating
max_it = 500
max_animal_total = 45
repeat_x = 15
filename = 'test.csv'
directory = r'C:\Users\diamo\OneDrive\Desktop\Programming Assignment\Simulation_Results'

filename = open(os.path.join(directory, filename), 'a', newline='')
file = csv.writer(filename)

for an_1 in range(0, max_animal_total+1):
    for an_2 in range(0, max_animal_total - an_1 +1):
        an_3 = max_animal_total - an_1 - an_2

        n_animal_1 = an_1  # Herbivore
        n_animal_2 = an_2  # Carnivore
        n_animal_3 = an_3  # Omnivore

        counter_r = []
        repeat = 0
        while repeat != repeat_x:

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
            while counter != max_it:
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
                brat = 0
                if animal_n_list['Animal_1'] == 0 and animal_n_list['Animal_2'] == 0 and animal_n_list['Animal_3'] == 0:
                    break
            if counter != max_it:
                repeat += 1
                counter_r.append(counter)
        save_to = [str(an_1) + '-' + str(an_2) + '-' + str(an_3)]
        for val in counter_r:
            save_to.append(val)
        print(save_to)
        file.writerow(save_to)



filename.close()
