import random
from abc import ABC, abstractclassmethod


class BaseStrategy(ABC):
    @abstractclassmethod
    def __call__(self, history, **kwargs):
        guess = ...
        return guess


class InefficientStrategy(BaseStrategy):
    def __init__(self, word_file_path):
        with open(word_file_path) as f:
            self.word_list = f.read().splitlines()

        self.pruned_word_list = self.word_list
        self.conditions = None

    def prune_word_list(self, word_list, history):
        conditions = self.history_to_conditions(history)
        # if nothing new is learnt, do not prune
        # otherwise prune possible words
        if conditions != self.conditions:
            self.conditions = conditions
            exists = conditions.get("exists", [])
            not_exists = conditions.get("not_exists", [])

            pruned_word_list = []
            for word in word_list:
                if all([letter in word for letter in exists]) and all([letter not in word for letter in not_exists]):
                    pruned_word_list.append(word)
            self.pruned_word_list = pruned_word_list

    def history_to_conditions(self, history):
        """Translates history into conditions which can be applied to prune possible word list

        Args:
            history (list): [(guess0, feedback0), (guess1, feedback1), ...]
        """
        exists = set()
        not_exists = set()
        for step in history:  # for each step
            for i, letter in enumerate(step[0]):  # for each letter in the word
                if step[1][i] > -1:  # letter is not gray
                    exists.add(letter)
                else:
                    not_exists.add(letter)
        # Remove letters which accidently went to not_exists
        not_exists = not_exists - exists

        conditions = {"exists": exists, "not_exists": not_exists}

        return conditions

    def __call__(self, history):
        if len(history) == 0:
            self.pruned_word_list = self.word_list
            self.conditions = None

        self.prune_word_list(self.pruned_word_list, history)
        guess = random.choice(self.pruned_word_list)
        return guess
