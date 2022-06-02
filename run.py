import os

from scripts.generator import simple_wordle_generator
from scripts.evaluator import evaluator
from scripts.strategy import InefficientStrategy
from scripts.utils import log_start_time, log_end_time, calculate_avg_time_taken, calculate_avg_num_of_guesses, print_target_and_guesses

if __name__ == "__main__":
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    word_file_path = os.path.join(ROOT_DIR, "data/nltk/5_lettered_words.txt")

    wordle_generator = simple_wordle_generator(word_file_path=word_file_path)
    strategy = InefficientStrategy(word_file_path=word_file_path)
    pre_logging_callbacks = [log_start_time]
    post_logging_callbacks = [log_end_time]
    metric_callbacks = [calculate_avg_time_taken,
                        calculate_avg_num_of_guesses, print_target_and_guesses]

    num_evals = 10

    results = evaluator(wordle_generator=wordle_generator, strategy=strategy, metric_callbacks=metric_callbacks,
                        num_eval=num_evals, pre_logging_callbacks=pre_logging_callbacks, post_logging_callbacks=post_logging_callbacks)

    print(results)
