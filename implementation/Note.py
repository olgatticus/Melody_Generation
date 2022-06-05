from typing import List
import numpy as np

"""
This class represent a note
Attribute explanation:
-value: represent value of the note (A, B, C, D, E, F, G)
-octave: represent the octave of the note
-rhythm: represent rhythm of a single note (1/4, 1/8, 1/16) 
-octv_low and octv_up: represent range of octaves values between lowest and highest
"""
class Note:
    value: int
    octave: int
    rhythm: int 
    octv_low: int
    octv_up: int

    """ Initialization of the note """
    def __init__(self, octv_low: int = 4, octv_up: int = 4):    
        
        # generate note value using zipf law
        while True:
            val = np.random.zipf(1.092)
            #val = np.random.randint(1 , 7)

            mapping = { 1 : 1,  #C
                        6 : 2,  #D
                        3 : 3,  #E
                        5 : 4,  #F
                        2 : 5,  #G
                        4 : 6,  #A
                        7 : 7,  #B
                        }

            if val <= 7:
                self.value = mapping[val]
                break 
        
        # generate octave value using normal distribution
        while True:
            octv = int(np.floor(np.random.normal(4, 1)))
            if octv >= octv_low and octv <= octv_up:
                self.octave = octv
                break

        self.rhythm = 2 # default value
        self.octv_low=octv_low
        self.octv_up=octv_up
        
    def __repr__(self):
        return "<Note value:%s octave:%s rhythm:%s>" % (self.value, self.octave, self.rhythm)

    def __str__(self):
        return "<Note value:%s octave:%s rhythm:%s>" % (self.value, self.octave, self.rhythm)

    """ Mutation value """
    def mutate_value(self, mutation_prob: float = 0.8, std_dev: float = 1):
        position = (self.octave-1) * 7 + self.value # mean of the gaussian

        # (pos_max, pos_min) is the range of acceptable values
        pos_max = (self.octv_up-1) * 7 + 7
        pos_min = (self.octv_low-1) * 7 + 1

        mutation_dice = np.random.uniform(0, 1)
        if mutation_dice < mutation_prob:
            pos = position
            while pos == position:
                pos = np.floor(np.random.normal(position, std_dev))
                if pos >= pos_min and pos <= pos_max: 
                    octv = np.int32(np.ceil(pos/7))
                    val = np.int32(pos - (octv-1)*7)

                    # check note to avoid duplicates
                    if pos != position: 
                        self.value = val
                        self.octave = octv
                        
                # stay inside the loop if the position is not valid        
                else:
                    pos = position 

    """ Assign new rhythm value according to a normal distribution """
    def add_rhythm(self, std: float = 1):
        while True:
            rtm = np.int32(np.random.normal(2, std)) 
            if rtm >= 2 and rtm <=4:
                self.rhythm = rtm
                break
        
    """ Mutation rhythm """ 
    def mutate_rhythm(self, mutation_prob: float = 0.2, std_dev: float = 1):
        mutation_dice = np.random.uniform(0, 1)
        if mutation_dice < mutation_prob:
            while True:
                #rtm = np.int32(np.random.normal(self.rhythm, std_dev))
                rtm = np.int32(np.random.normal(2, std_dev)) 

                # check if the value is acceptable and different from orignal rhythm
                if rtm >= 2 and rtm <=4 and rtm != self.rhythm:
                    self.rhythm = rtm
                    break