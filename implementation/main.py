import interface as itf
import genetic_operators as go
import statistics as stat

# Global variables (GA parameters)
std_dev_mel = 2             # Standard deviation for the gaussian sampling in the melody mutation
cross_prob_rtm = 0.5        # Probability of crossover in the rhythm evolution
mut_prob_rtm = 0.4          # Probability of mutation in the rhythm evolution
std_dev_rtm = 1             # Standard deviation for the gaussian sampling in the rhythm mutation

ind_len = 8

"""
Converts n_octaves (the number of octaves to consider for the notes) 
into a couple of indexes that indicate the lowest and uppest octaves to consider.
The indexes range from 3 (3rd octave on the piano keyboard) and 5 (5th octave on the piano keyboard).

:param i: number of octaves
:return: tuples of indexes of the first and last octave to consider
"""
def get_octaves(i):
    if (i == 1):
        return 4,4
    elif(i == 2):
        return 4,5
    else:
        return 3,5

if __name__ == "__main__":

    # Initial window: the human user chooses the population size and the number of octaves
    itf.window_initial()
    itf.window.mainloop()

    # Setting of the parameters according to the user's choices
    pop_size = itf.n_mel
    octv_low, octv_up = get_octaves(itf.n_octaves)

    not_first_gen = False   # False if the initial population still has to be created
    gen_count = 0           # Index of the current population, starting from 0 with the initial one,
                            # used for the adaptive mutation and crossover

    # When the melody creation starts, a new population has to be created from scratch
    # Then the GA loops across successive generations until a melody is selected by the user
    while (itf.melody_selected == False):
        if(not_first_gen):
            # The current population just needs to evolve
            cross_prob_mel = go.calc_cross_prob(gen_count)  # adaptive crossover probability
            mut_prob_mel = go.calc_mutation_prob(gen_count) # adaptive mutation probability
            population = go.parent_selection_value(parents=population,
                                pop_size=pop_size,
                                crossover_prob= cross_prob_mel,
                                mutation_prob=mut_prob_mel,
                                std_dev=std_dev_mel)
            gen_count += 1
        else:
            # The initial population needs to be created
            population = go.generate_init_pop_value(pop_size = pop_size, 
                                individual_length = ind_len, 
                                octv_low = octv_low, 
                                octv_up = octv_up)
            not_first_gen = True

        # Create the audio files (phenotypes) from the genotypes
        create = go.create_audio(population)

        # Window with the current population of audio files to be evaluated from the user
        itf.window_mel()
        itf.window.mainloop()

        # Extraction of the user evaluations and update of the fitness vectors
        fitness_vector = itf.fitness
        go.vote_population(population=population, fitnesses=fitness_vector)

        # Record the fitness vector for statistical analysis
        stat.write_stat_mel(fitness_vector)

    # Index of the winner melody
    best_melody_indx = itf.final_melody-1


    # If the user is willing to perform also the rhythm evolution phase
    if (itf.rhythm_yn):

        not_first_gen = False   # False if the rhythm still has to be added
        pop_size = itf.n_rtm

        # When the rhythm evolution starts, a new population of rhythms has to be created
        # Then the GA loops across successive generations until a rhythm is selected by the user
        while (itf.rhythm_selected == False):
            # The current population just needs to evolve
            if(not_first_gen):
                population = go.parent_selection_rhythm(parents=population,
                            pop_size=pop_size,
                            crossover_prob=cross_prob_rtm,
                            mutation_prob = mut_prob_rtm,
                            std_dev= std_dev_rtm)
            else:
                # The initial rhythms must be added
                population = go.add_rhythm(pop = population,
                            best_melody_indx=best_melody_indx,
                            pop_size=pop_size,
                            std=1)
                not_first_gen = True

            # Create the audio files (phenotypes) from the genotypes
            create = go.create_audio(population)
    
            # Window with the current population of audio files to be evaluated from the user
            itf.window_rhythm()
            itf.window.mainloop()

            # Extraction of the user evaluations and update of the fitness vectors
            fitness_vector = itf.fitness_rhythm
            go.vote_population(population=population, fitnesses=fitness_vector)

            # Record the fitness vector for statistical analysis
            stat.write_stat_rtm(fitness_vector)

    # Last window: end of the algorithm
    itf.window_end()
    itf.window.mainloop()
    
    
   
    
