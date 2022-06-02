import random


def simple_wordle_generator(word_file_path, seed=0, k=100000):
    """Returns a generator which creates wordle by uniformly sampling words from a file

    Args:
        word_file_path (str): path of the file which has a k(=5) lettered word in each line
        seed (int, optional): random seed to use for shuffling. Defaults to 0.
        k (int, optional): max number of wordles that can be generated. Defaults to 100000.

    Yields:
        str: k(=5) lettered word
    """
    random.seed(seed)
    with open(word_file_path) as f:
        word_list = f.read().splitlines()

    sampled_words = random.choices(word_list, k=k)

    for word in sampled_words:
        yield word
