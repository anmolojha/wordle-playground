import time
import numpy as np


def log_start_time(*args, **kwargs):
    return {"start_time": time.time()}


def log_end_time(*args, **kwargs):
    return {"end_time": time.time()}


def calculate_avg_time_taken(eval_history):
    time_taken = []
    for eval in eval_history:
        time_taken.append(eval["end_time"] - eval["start_time"])
    return {"avg_time": np.mean(time_taken)}


def calculate_avg_num_of_guesses(eval_history):
    num_guesses = []
    for eval in eval_history:
        num_guesses.append(len(eval["history"]))
    return {"avg_guesses": np.mean(num_guesses)}


def print_target_and_guesses(eval_history):
    for eval in eval_history:
        target = eval["word"]
        guesses = [step[0] for step in eval["history"]]
        print("TARGET:", target, "GUESSES:", guesses)
    return {}
