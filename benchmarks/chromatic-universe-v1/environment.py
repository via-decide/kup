from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
import random
from typing import Final

PALETTE: Final[tuple[str, ...]] = ("RED", "GREEN", "BLUE", "YELLOW")
NO_REACTION: Final[str] = "NO_REACTION"


@dataclass(frozen=True)
class HiddenCombinationRule:
    inputs: tuple[str, str]
    output: str

    def as_record(self) -> dict[str, object]:
        return {
            "ruleType": "single-special-combination",
            "inputs": sorted(self.inputs),
            "output": self.output,
            "defaultOutcome": NO_REACTION,
            "commutative": True,
        }


class ChromaticEnvironment:
    """Harness-owned world state. The KEY never receives this object."""

    def __init__(self, seed: int):
        rng = random.Random(seed)
        pairs = list(combinations(PALETTE, 2))
        chosen_pair = pairs[rng.randrange(len(pairs))]
        output_candidates = [color for color in PALETTE if color not in chosen_pair]
        output = output_candidates[rng.randrange(len(output_candidates))]
        self.__hidden_rule = HiddenCombinationRule(chosen_pair, output)

    @property
    def palette(self) -> tuple[str, ...]:
        return PALETTE

    def combine(self, left: str, right: str) -> str:
        if left not in PALETTE or right not in PALETTE:
            raise ValueError("unknown color state")
        if left == right:
            raise ValueError("0.0.1 only permits combinations of two distinct base states")
        if frozenset((left, right)) == frozenset(self.__hidden_rule.inputs):
            return self.__hidden_rule.output
        return NO_REACTION

    def ground_truth_record(self) -> dict[str, object]:
        """Evaluator-only access, called after the KEY has submitted a final claim."""
        return self.__hidden_rule.as_record()
