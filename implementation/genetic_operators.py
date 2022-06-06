import numpy as np
import copy
from NoteList import NoteList
import wave


""" Compute dynamic crossover probability based on generation number """
def calc_cross_prob(gen: int = 1):
    if gen > 4:
        prob = 0.3
    else:
        prob = -0.1*gen + 0.7
    return prob

""" Compute dynamic mutation probability based on generation number """
def calc_mutation_prob(gen: int = 1):
    if gen > 4:
        prob = 0.2
    else:
        prob = -0.1*gen + 0.6
    return prob

"""
Generate initial population

Inputs:
-pop_size: number of individuals in the population
-individual_length: how many notes an individual is composed of
-octv_low and octv_up: range of octave values (lowest and highest)
"""
def generate_init_pop_value(pop_size: int = 10, individual_length: int = 16, octv_low: int = 3, octv_up: int = 5):
    population = []
    for i in range(pop_size):
        population.append(NoteList(individual_length=individual_length, octv_low=octv_low, octv_up=octv_up))
    return population

""" Sort the individuals of the population according to their fitness value """
def sort_population_fitness(population):
    sorted_pop = sorted(population, key=lambda notelist: notelist.fitness, reverse=True)
    return sorted_pop

""" Update the fitness values of the population according to the votes given from the user """
def vote_population(population, fitnesses):
    i = 0
    for x in population:
        x.fitness = fitnesses[i]
        i+=1

"""
Generate the new population during the melody evolution phase

Inputs:
-parents: population of parents
-new_population: individuals that currently belong to the new population
-crossover_prob: probability of performing crossover between 2 parents
-mutation_prob: probability of performing mutation of the generated offspring
-std_dev: standard deviation of the Gaussian distribution used in the mutation process
-new_pop_size: number of total individuals that must compose the new population
"""
def generate_offspring_roulette_wheel_value(parents, new_population, crossover_prob: float = 0.8, mutation_prob: float = 0.8, std_dev: float = 1, new_pop_size: int = 10):
    fitness_sum = 0
    for x in parents:
        fitness_sum += x.fitness 

    # Compute cumulative probability
    sum_of_prob = 0
    for x in parents:
        x.reprod_prob = sum_of_prob + (x.fitness/fitness_sum)
        sum_of_prob += x.reprod_prob

    while len(new_population) < new_pop_size:
        offspring1 = NoteList()
        repr_dice = np.random.uniform(0, 1)
        for x in parents:
            if x.reprod_prob > repr_dice:
                offspring1 = copy.deepcopy(x)
                break

        offspring2 = copy.deepcopy(offspring1)
        while offspring1 == offspring2:
            repr_dice = np.random.uniform(0, 1)
            for x in parents:
                if x.reprod_prob > repr_dice:
                    offspring2 = copy.deepcopy(x)
                    break
        
        # Crossover
        offspring1.single_crossover_value(offspring2, crossover_prob)

        # Mutation
        offspring1.mutate_value(mutation_prob, std_dev)

        offspring1.fitness = 1

        # Check current individuals to avoid replicates
        valid = True
        for indiv in new_population:
            val_off1 = offspring1.getval()
            val_indiv = indiv.getval()
            if val_off1 == val_indiv:
                valid = False
        
        if valid:
            new_population.append(offspring1)

    return new_population


"""
Create the next generation during the melody evolution phase

Inputs:
-parents: current population
-pop_size: number of individuals in the population
-crossover_prob: probability of performing crossover between 2 parents
-mutation_prob: probability of performing mutation of the generated offspring
-std_dev: standard deviation of the Gaussian distribution used in the mutation process
"""
def parent_selection_value(parents, pop_size: int = 10, crossover_prob: float = 0.8, mutation_prob: float = 0.8, std_dev: float = 1):

    # num of elite = rounded down to 25% of pop size
    # unless pop size = 2 or 3 where just 1 elite is present
    num_of_elite = np.int32(np.floor(pop_size*0.25))
    if num_of_elite == 0 and (pop_size == 2 or pop_size == 3):
        num_of_elite = 1

    # Elites are added to the new population
    next_gen = []
    sorted_parents = sort_population_fitness(parents)
    for i in range(num_of_elite):
        elite_indiv = copy.deepcopy(sorted_parents[i])
        elite_indiv.fitness = 1
        next_gen.append(elite_indiv)
    
    # New individuals are generated
    next_gen = generate_offspring_roulette_wheel_value(parents = parents,
                                                    new_population=next_gen,
                                                    crossover_prob = crossover_prob,
                                                    mutation_prob = mutation_prob,
                                                    std_dev = std_dev,
                                                    new_pop_size = pop_size)

    return next_gen

""" Add rhythm to the best melody in order to create initial rhythm population """
def add_rhythm(pop, best_melody_indx, pop_size: int = 5, std: float = 1):
    new_pop = []
    best_melody = copy.deepcopy(pop[best_melody_indx])
    for x in range(pop_size):
        indv = copy.deepcopy(best_melody)
        indv.add_rhythm(std)
        new_pop.append(indv)
    return new_pop

"""
Generate the new population during the rhythm evolution phase

Inputs:
-parents: population of parents
-new_population: individuals that currently belong to the new population
-crossover_prob: probability of performing crossover between 2 parents
-mutation_prob: probability of performing mutation of the generated offspring
-std_dev: standard deviation of the Gaussian distribution used in the mutation process
-new_pop_size: number of total individuals that must compose the new population
"""
def generate_offspring_roulette_wheel_rhythm(parents, new_population, crossover_prob: float = 0.8, mutation_prob: float = 0.8, std_dev: float = 1, new_pop_size: int = 5):
    fitness_sum = 0
    for x in parents:
        fitness_sum += x.fitness 

    # Compute cumulative probability
    sum_of_prob = 0
    for x in parents:
        x.reprod_prob = sum_of_prob + (x.fitness/fitness_sum)
        sum_of_prob += x.reprod_prob

    while len(new_population) < new_pop_size:
        offspring1 = NoteList()
        repr_dice = np.random.uniform(0, 1)
        for x in parents:
            if x.reprod_prob > repr_dice:
                offspring1 = copy.deepcopy(x)
                break

        offspring2 = copy.deepcopy(offspring1)
        while offspring1 == offspring2:
            repr_dice = np.random.uniform(0, 1)
            for x in parents:
                if x.reprod_prob > repr_dice:
                    offspring2 = copy.deepcopy(x)
                    break
        
        # Crossover
        offspring1.single_crossover_rhythm(offspring2, crossover_prob)

        # Mutation
        offspring1.mutate_rhythm(mutation_prob, std_dev)

        offspring1.fitness = 1

        # Check current individual to avoid replicate
        valid = True
        for indiv in new_population:
            val_off1 = offspring1.getval()
            val_indiv = indiv.getval()
            if val_off1 == val_indiv:
                valid = False

        offspring1.fitness = 1

        if valid:
            new_population.append(offspring1)

    return new_population

"""
Create the next generation during the rhythm evolution phase

Inputs:
-parents: current population
-pop_size: number of individuals in the population
-crossover_prob: probability of performing crossover between 2 parents
-mutation_prob: probability of performing mutation of the generated offspring
-std_dev: standard deviation of the Gaussian distribution used in the mutation process
"""
def parent_selection_rhythm(parents, pop_size: int = 5, crossover_prob: float = 0.8, mutation_prob: float = 0.8, std_dev: float = 1):
    num_of_elite = np.int32(np.floor(pop_size*0.25))
    if num_of_elite == 0 and (pop_size == 2 or pop_size == 3):
        num_of_elite = 1

    # Elites are added to the new population
    next_gen = []
    sorted_parents = sort_population_fitness(parents)
    for i in range(num_of_elite):
        elite_indiv = copy.deepcopy(sorted_parents[i])
        elite_indiv.fitness = 1
        next_gen.append(elite_indiv)
    
    # New individuals are generated
    next_gen = generate_offspring_roulette_wheel_rhythm(parents = parents,
                                                    new_population=next_gen,
                                                    crossover_prob = crossover_prob,
                                                    mutation_prob = mutation_prob,
                                                    std_dev = std_dev,
                                                    new_pop_size = pop_size)

    return next_gen


""" Generate the .wav file for each melody """
def create_audio(pop):
    data = []
    for j in range(len(pop)):
        sounds = pop[j].getval()
        # i[0] = note value, i[1] = octave, i[2] = rhythm
        for i in (sounds):
            w = wave.open("./audio/genetic_melody_" + str(int(i[0])) + "_" + str(int(i[1])) + "_" + str(int(i[2])) + ".wav","rb")
            data.append([w.getparams(), w.readframes(w.getnframes())])
            w.close()
        
        output = wave.open("./audio/" + str(int(j)) + "indiv.wav", "wb")
        output.setparams(data[0][0])
        for i in range(len(data)):
            output.writeframes(data[i][1])

        output.close()
        data.clear()
    return output
