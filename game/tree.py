import random

from game.config import TreeSegment


class Tree:
    def __init__(self):
        self.segments: list[TreeSegment] = []
        self.reset()

    def reset(self):
        self.segments = [TreeSegment.EMPTY, TreeSegment.EMPTY]
        for _ in range(5):
            self.segments.append(self._generate_segment())

    def _generate_segment(self) -> TreeSegment:
        return random.choices(
            [TreeSegment.EMPTY, TreeSegment.LEFT_BRANCH, TreeSegment.RIGHT_BRANCH, TreeSegment.ANIMAL],
            weights=[51, 24, 24, 1],
        )[0]

    def cut(self):
        self.segments.pop(0)
        self.segments.append(self._generate_segment())

    def rescue_animal(self) -> bool:
        if self.segments[1] == TreeSegment.ANIMAL:
            self.segments[1] = TreeSegment.EMPTY
            return True
        return False

    def has_animal_next(self) -> bool:
        return self.segments[1] == TreeSegment.ANIMAL
