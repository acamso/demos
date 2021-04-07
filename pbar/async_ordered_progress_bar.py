# *- coding: utf-8 -*-
# async_ordered_progress_bar.py
# 04-06-2021 16:03:16 EDT
# (c) 2021 acamso

"""Async ordered progress bar.

This is a demonstration on how to implement an async, ordered progress bar with TQDM + asyncio. 
"asyncio.as_completed" is needed to run async tasks with TQDM , which results in an unordered result. 
If you're looking for an ordered result, you simply need to wrap each task in a coroutine with the 
corresponding index and sort the result.

Video: https://youtu.be/oJC7RcjbEPc
"""

import asyncio
from typing import Any, Coroutine, Iterable, List, Tuple

from tqdm import tqdm


async def aprogress(tasks: Iterable[Coroutine], **pbar_kws: Any) -> List[Any]:
    """Runs async tasks with a progress bar and returns an ordered result."""

    if not tasks:
        return []

    async def tup(idx: int, task: Coroutine) -> Tuple[int, Any]:
        """Returns the index and result of a task."""
        return idx, await task

    _tasks = [tup(i, t) for i, t in enumerate(tasks)]
    pbar = tqdm(asyncio.as_completed(_tasks), total=len(_tasks), **pbar_kws)
    res = [await t for t in pbar]
    return [r[1] for r in sorted(res, key=lambda r: r[0])]


if __name__ == "__main__":

    import random

    async def test(idx: int) -> Tuple[int, int]:
        sleep = random.randint(0, 5)
        await asyncio.sleep(sleep)
        return idx, sleep

    _tasks = [test(i) for i in range(10)]
    _res = asyncio.run(aprogress(_tasks, desc="pbar test"))
    print(_res)
