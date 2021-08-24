# *- coding: utf-8 -*-
# craps_simulator.py
# 08-23-2021 21:18:06 EDT
# (c) 2021 acamso

"""Craps simulator.

This is a demonstration on how to build a craps simulator with Python.

Video #1 - Rolling The Dice: _
Craps: https://en.wikipedia.org/wiki/Craps
"""

from __future__ import annotations

import itertools
import random
from collections import Counter
from typing import List, Optional, Tuple


class Player:
    def __init__(self, num: int) -> None:
        self.num: int = num

    @staticmethod
    def roll(dice: List[Die]) -> int:
        """Rolls the dice and returns a number between 2-12."""
        return sum(die.roll() for die in dice)


class Die:
    def __init__(self) -> None:
        self.num: Optional[int] = None

    def roll(self) -> int:
        """Rolls the dice and returns a number between 1-6."""
        self.num = random.randint(1, 6)
        return self.num


def simulate(num_players: int, num_rolls: int) -> List[Tuple[int, int]]:
    """Simulates a complete game of Craps."""

    # create players
    players = [Player(num=num + 1) for num in range(num_players)]
    _players = itertools.cycle(players)

    # create dice
    dice = [Die(), Die()]

    # roll dice
    results = []
    for _ in range(num_rolls):
        player = next(_players)
        res = player.roll(dice)
        results.append(res)
        print(f"Player #{player.num} rolled a {res}")

    # test
    counter = Counter(results).items()  # dict_items([(5, 11132), (6, 13797)]
    sorted_counter = sorted(counter, key=lambda x: x[1], reverse=True)  # [(7, 16631), (6, 13797)]
    test_dice_result_probability(sorted_counter)

    return sorted_counter


def test_dice_result_probability(sorted_counter: List[Tuple[int, int]]) -> None:
    """Tests the accuracy of dice result probability."""
    most_common = [x[0] for x in sorted_counter]  # [7, 8, 6, 9, 5, 10, 4, 3, 11, 12, 2]
    assert most_common[0] == 7
    assert most_common[1] in (6, 8)
    assert most_common[2] in (6, 8)
    assert most_common[3] in (5, 9)
    assert most_common[4] in (5, 9)
    assert most_common[5] in (4, 10)
    assert most_common[6] in (4, 10)
    assert most_common[7] in (3, 11)
    assert most_common[8] in (3, 11)
    assert most_common[9] in (2, 12)
    assert most_common[10] in (2, 12)


if __name__ == "__main__":

    # cli will go here
    _num_players = 1
    _num_rolls = 100000

    # simulate
    print(simulate(_num_players, _num_rolls))
