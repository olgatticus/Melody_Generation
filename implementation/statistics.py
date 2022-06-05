from datetime import datetime
#from nbformat import write
import os

# Path of the file for the melody statistics
path_mel_ = None
# Path of the file for the rhythm statistics
path_rtm_ = None

"""
For each execution of the GA, store in a file the statistics related to the melody evolution:
- the name of the file depends on the current date and hour
- each line corresponds to a generation, and contains the average fitness and maximal fitness
    of the individuals, according to the user evaluation

:param fv: fitness vector corresponding to the evaluations of a generation
"""
def write_stat_mel(fv):
    global path_mel_
    if path_mel_ == None:
        now = datetime.now()
        current_time = now.strftime("%d%H%M%S")
        path_mel_ = "./stat/mel/" + current_time + ".txt"
    with open(path_mel_, 'a') as f:
        f.write("{}\t{}\n".format((sum(fv)/len(fv)), max(fv)))
    
"""
For each execution of the GA, store in a file the statistics related to the rhythm evolution:
- the name of the file depends on the current date and hour
- each line corresponds to a generation, and contains the average fitness and maximal fitness
    of the individuals, according to the user evaluation

:param fv: fitness vector corresponding to the evaluations of a generation
"""
def write_stat_rtm(fv):
    global path_rtm_
    if path_rtm_ == None:
        now = datetime.now()
        current_time = now.strftime("%d%H%M%S")
        path_rtm_ = "./stat/rtm/" + current_time + ".txt"
    with open(path_rtm_, 'a') as f:
        f.write("{}\t{}\n".format((sum(fv)/len(fv)), max(fv)))


"""
Compute the mean value of the total number of generations across all the executions in the stat folder
It takes into account also the last generation

:param path: path of the folder containing the execution statistics
:return: mean number of generations considering all the executions
"""
def mean_length(path):
    list_files = os.listdir(path)
    num_files = len(list_files)
    sum_len_file = 0
    for file_path in list_files:
        f = open(path + file_path, "r")
        lines = f.readlines()
        sum_len_file += len(lines)
    f.close()
    mean_len = sum_len_file/num_files
    return mean_len

path_mel = "./stat/mel/"
path_rtm = "./stat/rtm/"


"""
Compute the mean value of the raw gain of the average values (as the difference between the avg rates 
between the penultimate generation and the first generation) across all the executions in the stat folder

:param path: path of the folder containing the execution statistics
:return: mean value of the raw gain of the average values
"""
def mean_raw_gain_on_mean(path):
    list_files = os.listdir(path)
    count = 0
    sum_raw_gains = 0.0
    for file_path in list_files:
        f = open(path + file_path, "r")
        lines = f.readlines()
        num_lines = len(lines)
        if num_lines > 2:
            count += 1
            line_0 = lines[0].strip().split()[0]
            line_last  = lines[-2].strip().split()[0]
            raw_gain = float(line_last) - float(line_0)
            sum_raw_gains += raw_gain

    f.close()
    mean_gain = sum_raw_gains/count

    return mean_gain

"""
Compute the mean value of the raw gain of the max values (as the difference between the max rates 
between the penultimate generation and the first generation) across all the executions in the stat folder

:param path: path of the folder containing the execution statistics
:return: mean value of the raw gain of the max values
"""
def mean_raw_gain_on_max(path):
    list_files = os.listdir(path)
    count = 0
    sum_raw_gains = 0.0
    for file_path in list_files:
        f = open(path + file_path, "r")
        lines = f.readlines()
        num_lines = len(lines)
        if num_lines > 2:
            count += 1
            line_0 = lines[0].strip().split()[1]
            line_last  = lines[-2].strip().split()[1]
            raw_gain = float(line_last) - float(line_0)
            sum_raw_gains += raw_gain

    f.close()
    mean_gain = sum_raw_gains/count

    return mean_gain

"""
Compute the mean value of the average gain of the average values (as the difference between the avg rates 
between the penultimate generation and the first generation, divided by the number of generations -1)
across all the executions in the stat folder

:param path: path of the folder containing the execution statistics
:return: mean value of the average gain of the average values
"""
def mean_avg_gain_on_mean(path):
    list_files = os.listdir(path)
    count = 0
    sum_avg_gains = 0.0
    for file_path in list_files:
        f = open(path + file_path, "r")
        lines = f.readlines()
        num_lines = len(lines)
        if num_lines > 2:
            count += 1
            line_0 = lines[0].strip().split()[0]
            line_last  = lines[-2].strip().split()[0]
            avg_gain = (float(line_last) - float(line_0))/(num_lines - 1)
            sum_avg_gains += avg_gain

    f.close()
    mean_gain = sum_avg_gains/count

    return mean_gain

"""
Compute the mean value of the average gain of the max values (as the difference between the max rates 
between the penultimate generation and the first generation, divided by the number of generations -1)
across all the executions in the stat folder

:param path: path of the folder containing the execution statistics
:return: mean value of the average gain of the max values
"""
def mean_avg_gain_on_max(path):
    list_files = os.listdir(path)
    count = 0
    sum_avg_gains = 0.0
    for file_path in list_files:
        f = open(path + file_path, "r")
        lines = f.readlines()
        num_lines = len(lines)
        if num_lines > 2:
            count += 1
            line_0 = lines[0].strip().split()[1]
            line_last  = lines[-2].strip().split()[1]
            avg_gain = (float(line_last) - float(line_0))/(num_lines - 1)
            sum_avg_gains += avg_gain

    f.close()
    mean_gain = sum_avg_gains/count

    return mean_gain


"""
Compute the mean value of the average rates in the first generation across all the executions in the stat folder

:param path: path of the folder containing the execution statistics
:return:  mean value of the average rates in the first generation
"""
def mean_first_gen_mean(path):
    list_files = os.listdir(path)
    sum_first_mean = 0.0
    num_files = len(list_files)
    for file_path in list_files:
        f = open(path + file_path, "r")
        lines = f.readlines()
        mean_0 = lines[0].strip().split()[0]
        sum_first_mean += float(mean_0)

    f.close()
    mean_gain = sum_first_mean/num_files

    return mean_gain


"""
Compute the mean value of the max rates in the first generation across all the executions in the stat folder

:param path: path of the folder containing the execution statistics
:return:  mean value of the max rates in the first generation
"""
def mean_first_gen_max(path):
    list_files = os.listdir(path)
    sum_first_mean = 0.0
    num_files = len(list_files)
    for file_path in list_files:
        f = open(path + file_path, "r")
        lines = f.readlines()
        mean_0 = lines[0].strip().split()[1]
        sum_first_mean += float(mean_0)

    f.close()
    mean_gain = sum_first_mean/num_files

    return mean_gain


"""
Compute the mean value of the average rates in the last (penultimate) generation across 
all the executions in the stat folder

:param path: path of the folder containing the execution statistics
:return:  mean value of the average rates in the last (penultimate) generation
"""
def mean_last_gen_mean(path):
    list_files = os.listdir(path)
    sum_first_mean = 0.0
    num_files = len(list_files)
    for file_path in list_files:
        f = open(path + file_path, "r")
        lines = f.readlines()
        mean_0 = lines[-2].strip().split()[0]
        sum_first_mean += float(mean_0)

    f.close()
    mean_gain = sum_first_mean/num_files

    return mean_gain


"""
Compute the mean value of the max rates in the last (penultimate) generation across 
all the executions in the stat folder

:param path: path of the folder containing the execution statistics
:return:  mean value of the max rates in the last (penultimate) generation
"""
def mean_last_gen_max(path):
    list_files = os.listdir(path)
    sum_first_mean = 0.0
    num_files = len(list_files)
    for file_path in list_files:
        f = open(path + file_path, "r")
        lines = f.readlines()
        mean_0 = lines[-2].strip().split()[1]
        sum_first_mean += float(mean_0)

    f.close()
    mean_gain = sum_first_mean/num_files

    return mean_gain


if __name__ == "__main__":

    
    mean_len_mel = mean_length(path_mel)
    mean_len_rtm = mean_length(path_rtm)

    print("Mean number of generations for mel: ", round(mean_len_mel, 2))
    print("Mean number of generations for rtm: ", round(mean_len_rtm, 2))

    
    mean_raw_mean_mel = mean_raw_gain_on_mean(path_mel)
    mean_raw_max_mel = mean_raw_gain_on_max(path_mel)

    print("Mean raw gain on mean (for mel): ", round(mean_raw_mean_mel, 2))
    print("Mean raw gain on max (for mel): ", round(mean_raw_max_mel, 2))

    mean_avg_mean_mel = mean_avg_gain_on_mean(path_mel)
    mean_avg_max_mel = mean_avg_gain_on_max(path_mel)

    print("Mean avg gain on mean (for mel): ", round(mean_avg_mean_mel, 2))
    print("Mean avg gain on max (for mel): ", round(mean_avg_max_mel, 2))

    mean_first_mean = mean_first_gen_mean(path_mel)
    mean_first_max = mean_first_gen_max(path_mel)

    print("Mean of avg in first gen (for mel): ", round(mean_first_mean, 2))
    print("Mean of max in first gen (for mel): ", round(mean_first_max, 2))

    mean_last_mean = mean_last_gen_mean(path_mel)
    mean_last_max = mean_last_gen_max(path_mel)

    print("Mean of avg in last gen (for mel): ", round(mean_last_mean, 2))
    print("Mean of max in last gen (for mel): ", round(mean_last_max, 2))