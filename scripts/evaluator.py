def _check(target, guess):
    """Checks if target and guess match and returns appropriate feedback. In feedback, 1 means green, 0 means amber, -1 means gray.

    Args:
        target (str): target word
        guess (str): guessed word

    Returns:
        tuple: `(is_correct, feedback)`
    """
    is_correct = False
    feedback = []
    # check for character-wise exact match
    for i, letter in enumerate(guess):
        if letter == target[i]:
            feedback.append(1)
        else:
            feedback.append(-1)

    if sum(feedback) == len(feedback):
        is_correct = True
    else:
        matched_target = feedback.copy()
        # check for non-positional match with unmatched characters in targets
        for i, letter in enumerate(guess):
            if feedback[i] == 1:
                continue
            for j, target_letter in enumerate(target):
                if matched_target[j] > -1:
                    continue
                if letter == target_letter:
                    matched_target[j] = 0
                    feedback[i] = 0
                    break

    return is_correct, feedback


def play(target, strategy, max_iter=100):
    """Runs a game of wordle using the provided strategy

    Args:
        target (str): target word
        strategy (Callable): function: [(guess0, feedback0), ...] -> next guess
        max_iter (int, optional): maximum number of times the word is guessed. Defaults to 100.

    Returns:
        tuple: `(win, history)` where win is an indicator and history is a list of (guess, feedback)
    """
    win = False
    history = []
    for i in range(max_iter):
        guess = strategy(history)
        is_correct, feedback = _check(target, guess)
        history.append((guess, feedback))

        if is_correct:
            win = True
            break

    return win, history


def evaluator(wordle_generator, strategy, metric_callbacks, num_eval=1000, pre_logging_callbacks=None, post_logging_callbacks=None, **kwargs):
    """Evaluates the given strategy for the given wordle generator

    Args:
        wordle_generator (Generator[str, None, None]): generator which provides a new wordle when its `__next__` method is called
        strategy (Callable): function: [(guess0, feedback0), ...] -> next guess
        metric_callbacks (list): list of callbacks which compute aggregate metrics from information of multiple rounds of game
        num_eval (int, optional): number of round of game. Defaults to 1000.
        pre_logging_callbacks (list, optional): list of callbacks which are called before game is started. These are intended to store pre-game conditions which might be required by `metric_callbacks`. Defaults to None.
        post_logging_callbacks (_type_, optional): list of callbacks which are called after game is played. These are intended to store post-game conditions which might be required by `metric_callbacks`. Defaults to None.

    Returns:
        dict: dictionary containing all the metrics returned by `metric_callbacks`
    """
    eval_history = []
    for i in range(num_eval):
        # Store state before play
        state_dict = {}
        if pre_logging_callbacks is not None:
            for cb in pre_logging_callbacks:
                state_dict = {**state_dict, **cb(state_dict)}

        # generate wordle
        word = wordle_generator.__next__()
        # play with the strategy provided
        win, history = play(word, strategy, **kwargs)

        state_dict = {**state_dict, **
                      {"word": word, "win": win, "history": history}}

        # Run callback function to store and compute relevant information
        if post_logging_callbacks is not None:
            for cb in post_logging_callbacks:
                state_dict = {**state_dict, **cb(state_dict)}

        eval_history.append(state_dict)

    result = {}
    for cb in metric_callbacks:
        result = {**result, **cb(eval_history)}

    return result
