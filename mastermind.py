import random
from enum import Enum
from itertools import permutations
from collections import namedtuple, Counter
from typing import Iterable, Sequence, Tuple, MutableSequence, Optional, MutableMapping
import colorama

CODE_LEN = 4
MAX_TRIES = 12

Colors = Enum("Colors", "RED GREEN BLUE YELLOW WHITE GREY PINK CYAN")
Score = namedtuple("Score", "num_correct num_almost_correct")
Code = Sequence[Colors]
Clue = Tuple[Code, Score]


def create_code() -> Code:
    colors = list(Colors)
    random.shuffle(colors)
    return colors[:CODE_LEN]


def format_code(code: Code) -> str:
    color_lookup = {
        Colors.RED: colorama.Style.BRIGHT + colorama.Fore.RED,
        Colors.GREEN: colorama.Style.BRIGHT + colorama.Fore.GREEN,
        Colors.BLUE: colorama.Style.BRIGHT + colorama.Fore.BLUE,
        Colors.YELLOW: colorama.Style.BRIGHT + colorama.Fore.YELLOW,
        Colors.WHITE: colorama.Style.BRIGHT + colorama.Fore.WHITE,
        Colors.GREY: colorama.Style.NORMAL + colorama.Fore.WHITE,
        Colors.PINK: colorama.Style.BRIGHT + colorama.Fore.MAGENTA,
        Colors.CYAN: colorama.Style.BRIGHT + colorama.Fore.CYAN,
    }
    s = ""
    for color in code:
        s += color_lookup[color] + "●"
    s += colorama.Style.RESET_ALL
    return s


def format_clue(clue: Score) -> str:
    return (
        colorama.Style.BRIGHT
        + colorama.Fore.RED
        + str(clue.num_correct)
        + " "
        + colorama.Fore.WHITE
        + str(clue.num_almost_correct)
        + colorama.Style.RESET_ALL
    )


def score_guess(guess: Code, answer: Code) -> Score:
    num_correct_colors_in_correct_loc = [g == a for g, a in zip(guess, answer)].count(True)
    num_correct_colors_in_wrong_loc = [g in answer for g in guess].count(True) - num_correct_colors_in_correct_loc
    return Score(num_correct_colors_in_correct_loc, num_correct_colors_in_wrong_loc)


def all_possible_solutions() -> Iterable[Code]:
    return permutations(Colors, CODE_LEN)


def solution_matches_clues(guess: Code, clues: Sequence[Clue]) -> bool:
    for clue, score in clues:
        if score != score_guess(guess, clue):
            return False
    return True


def solve(answer: Code) -> Optional[Code]:
    clues: MutableSequence[Clue] = []

    guess_num = 1
    for solution in all_possible_solutions():
        if solution_matches_clues(solution, clues):
            score = score_guess(solution, answer)
            print(f"Guess #{guess_num}: {format_code(solution)}  Clue: {format_clue(score)}")
            if score.num_correct == CODE_LEN:
                return solution
            clues.append((solution, score))
            guess_num += 1
        if len(clues) == MAX_TRIES:
            break

    print("Couldn't find an answer :(")
    return None


for number, code in enumerate(all_possible_solutions(), start=1):
    # code = create_code()
    print(f"Game number {number}, Selected code is {format_code(code)}")
    answer = solve(code)
