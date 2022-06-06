from typing import List
import numpy as np

from Note import Note

"""
This class represents a melody composed by a list of notes

Attribute explanation:
-noteList: list of n Notes
-individual_length: how long is the list
-fitness: "goodness" of the melody, range between [1, 10] (1 = bad, 10 = good)
-reprod_prob: probability of reproduction
"""
class NoteList:
    noteList: List[Note]
    individual_length: int 
    fitness: int 
    reprod_prob: float

    """ Initialization of NoteList """
    def __init__(self, individual_length: int = 0, octv_low: int = 4, octv_up: int = 4):
        self.individual_length = individual_length
        self.fitness = 1
        self.reprod_prob = 0.5
        self.noteList = []
        for i in range(self.individual_length):
            self.noteList.append(Note(octv_low=octv_low, octv_up=octv_up))

    def __repr__(self):
        to_ret = "<Notelist length:%s, fitness:%s>" % (self.individual_length, self.fitness) + "\n"
        for x in self.noteList:
            to_ret += repr(x) + "\n"
        return to_ret

    def __str__(self):
        to_ret = "<Notelist length:%s, fitness:%s>" % (self.individual_length, self.fitness) + "\n"
        for x in self.noteList:
            to_ret += repr(x) + "\n"
        return to_ret

    def append(self, object: Note) -> None: #Will raise an exception if you try to append a non Note object
        if not isinstance(object, Note):
            raise TypeError("Can only append Note")
        self.noteList.append(object)

    """ Assign new rhythm value for every Note in NoteList """
    def add_rhythm(self, std: float = 1):
        for x in self.noteList:
            x.add_rhythm(std)

    """ Invoke mutation operator for value for every Note in NoteList """
    def mutate_value(self, mutation_prob: float=0.8, std_dev: float = 1):
        for x in self.noteList:
            Note.mutate_value(x, mutation_prob, std_dev)

    """ Invoke mutation operator for rhythm for every Note in NoteList """
    def mutate_rhythm(self, mutation_prob: float=0.8, std_dev: float = 1):
        for x in self.noteList:
            Note.mutate_rhythm(x, mutation_prob, std_dev)

    """ Value crossover between two NoteList instances """
    def single_crossover_value(self, pa2, crossover_prob: float = 0.8):
        crossover_dice = np.random.uniform(0, 1)
        offspring1 = self.noteList
        if crossover_dice < crossover_prob:
            position = np.random.randint(0, self.individual_length-1) #split point

            side_prob = np.random.randint(0,1)
            if side_prob == 0:
                offspring1 = np.concatenate((self.noteList[:position], pa2.noteList[position:]))
            else:
                offspring1 = np.concatenate((pa2.noteList[:position], self.noteList[position:]))
            
        self.noteList = offspring1

    """ Rhythm crossover between two NoteList instances """
    def single_crossover_rhythm(self, pa2, crossover_prob: float = 0.8):
        parent1 = []
        parent2 = []
        crossover_dice = np.random.uniform(0, 1)
        if crossover_dice < crossover_prob:
            position = np.random.randint(0, self.individual_length-1) #split point

            for x in self.noteList:
                parent1.append(x.rhythm)
            
            for x in pa2.noteList:
                parent2.append(x.rhythm)

            side_prob = np.random.randint(0,1)
            if side_prob == 0:
                offspring1 = np.concatenate((parent1[:position], parent2[position:]))
            else:
                offspring1 = np.concatenate((parent2[:position], parent1[position:]))
            
            

            # assign new rhythm values to notes
            i = 0
            for x in self.noteList:
                x.rhythm = int(offspring1[i])
                i += 1
    
    """ Update fitness values using user's scores """
    def vote_individual(self, fitness: int):
        if fitness >= 1 and fitness <=10:
            self.fitness = fitness
        else:
            raise TypeError("Fitness value not valid")
        return 1

    """
    For each Note in the Notelist return a tuple containing:
    - value of the Note
    - octave of the Note
    - rhythm of the Note
    """
    def getval(self):
        sounds = []
        for i in self.noteList:
            sound = [i.value, i.octave, i.rhythm]
            sounds.append(sound)
        return sounds
